"""
Fire Spread Model

Implements a Cellular Automaton-based wildfire spread model using Rothermel-inspired
fire behavior calculations. Integrates weather conditions and terrain to simulate
realistic fire propagation.
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, List
from enum import Enum

from weather_sim import WeatherSnapshot, WeatherState


class CellState(Enum):
    """Cell states in the fire simulation grid."""
    UNBURNED = 0
    BURNING = 1
    BURNED = 2
    WATER = 3  # Non-flammable


@dataclass
class FireSpreadParameters:
    """Parameters for fire spread calculation."""
    base_spread_rate: float = 10.0  # m/min
    wind_factor: float = 0.5  # Multiplier for wind effect
    slope_factor: float = 0.3  # Multiplier for slope effect
    humidity_suppression: float = 0.8  # Suppression at 100% humidity
    temperature_enhancement: float = 1.2  # Enhancement per 10°C above 20°C


class FireSpreadModel:
    """
    Cellular automaton-based fire spread model.
    
    Simulates wildfire propagation using weather conditions, fuel moisture,
    and terrain information.
    """

    def __init__(
        self,
        grid_size: Tuple[int, int] = (100, 100),
        cell_size_m: float = 10.0,
        params: FireSpreadParameters = None,
    ):
        """
        Initialize fire spread model.
        
        Args:
            grid_size: (rows, cols) dimension of simulation grid
            cell_size_m: Physical size of each cell in meters
            params: FireSpreadParameters for tuning fire behavior
        """
        self.grid_size = grid_size
        self.cell_size_m = cell_size_m
        self.params = params or FireSpreadParameters()

        # Initialize grids
        self.grid = np.zeros(grid_size, dtype=np.int8)  # Cell states
        self.fuel_moisture = np.ones(grid_size) * 50.0  # % moisture content
        self.elevation = np.zeros(grid_size)  # Elevation for slope calc
        self.spread_rate = np.zeros(grid_size)  # Spread rate per cell

        # History tracking
        self.burn_history = []

    def set_terrain(self, elevation_grid: np.ndarray):
        """
        Set terrain elevation data.
        
        Args:
            elevation_grid: 2D array of elevations in meters
        """
        if elevation_grid.shape != self.grid_size:
            raise ValueError("Elevation grid must match simulation grid size")
        self.elevation = elevation_grid.copy()

    def set_fuel_moisture(self, moisture_grid: np.ndarray):
        """
        Set initial fuel moisture content.
        
        Args:
            moisture_grid: 2D array of moisture percentages (0-100)
        """
        if moisture_grid.shape != self.grid_size:
            raise ValueError("Moisture grid must match simulation grid size")
        self.fuel_moisture = np.clip(moisture_grid, 0, 100)

    def ignite_cell(self, row: int, col: int):
        """
        Ignite a cell to start fire simulation.
        
        Args:
            row: Grid row index
            col: Grid column index
        """
        if 0 <= row < self.grid_size[0] and 0 <= col < self.grid_size[1]:
            self.grid[row, col] = CellState.BURNING.value

    def _calculate_slope(self, row: int, col: int) -> float:
        """
        Calculate slope factor from elevation data.
        
        Args:
            row: Grid row index
            col: Grid column index
            
        Returns:
            Slope factor (0-1)
        """
        if self.elevation.any() == 0:
            return 1.0

        # Calculate slope using neighbors
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.grid_size[0] and 0 <= nc < self.grid_size[1]:
                    neighbors.append(self.elevation[nr, nc])

        if not neighbors:
            return 1.0

        max_elev = max(neighbors)
        min_elev = min(neighbors)
        slope = (max_elev - min_elev) / (self.cell_size_m * np.sqrt(2))

        # Convert slope to factor (steeper = faster spread)
        return 1.0 + self.params.slope_factor * np.arctan(slope)

    def _calculate_spread_rate(self, weather: WeatherSnapshot, row: int, col: int) -> float:
        """
        Calculate fire spread rate based on weather and terrain.
        
        Args:
            weather: Current weather conditions
            row: Grid row index
            col: Grid column index
            
        Returns:
            Spread rate in m/min
        """
        rate = self.params.base_spread_rate

        # Wind effect (positive correlation with wind speed)
        wind_factor = 1.0 + (self.params.wind_factor * weather.wind_speed / 30.0)
        rate *= wind_factor

        # Humidity suppression (higher humidity = slower spread)
        humidity_suppression = 1.0 - (weather.humidity / 100.0) * self.params.humidity_suppression
        rate *= max(0.1, humidity_suppression)

        # Temperature enhancement
        temp_diff = max(0, weather.temperature - 20.0)
        temp_factor = 1.0 + (self.params.temperature_enhancement * temp_diff / 10.0)
        rate *= temp_factor

        # Slope effect
        slope_factor = self._calculate_slope(row, col)
        rate *= slope_factor

        return rate

    def _should_spread_to(self, to_row: int, to_col: int, spread_probability: float) -> bool:
        """
        Determine if fire should spread to an adjacent cell.
        
        Args:
            to_row: Target cell row
            to_col: Target cell column
            spread_probability: Probability of spread (0-1)
            
        Returns:
            True if fire should spread to target cell
        """
        # Out of bounds
        if not (0 <= to_row < self.grid_size[0] and 0 <= to_col < self.grid_size[1]):
            return False

        # Already burned or water
        if self.grid[to_row, to_col] in [CellState.BURNED.value, CellState.WATER.value]:
            return False

        # Probabilistic spread
        return np.random.random() < spread_probability

    def step(self, weather: WeatherSnapshot):
        """
        Execute one simulation step (1 minute).
        
        Args:
            weather: Current weather conditions
        """
        # Update fuel moisture based on weather
        if weather.weather_state == WeatherState.RAINY or weather.weather_state == WeatherState.STORMY:
            self.fuel_moisture = np.clip(self.fuel_moisture + 5, 0, 100)
        else:
            self.fuel_moisture = np.clip(self.fuel_moisture - 2, 0, 100)

        # Find all burning cells
        burning_cells = np.argwhere(self.grid == CellState.BURNING.value)

        # Spread fire to neighbors
        for row, col in burning_cells:
            spread_rate = self._calculate_spread_rate(weather, row, col)
            # Convert spread rate (m/min) to cell spread probability
            spread_probability = min(1.0, spread_rate / (self.cell_size_m * 10.0))

            # Check all 8 neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    neighbor_row = row + dr
                    neighbor_col = col + dc

                    if self._should_spread_to(neighbor_row, neighbor_col, spread_probability):
                        self.grid[neighbor_row, neighbor_col] = CellState.BURNING.value

            # Cool down burning cell after spread attempt
            self.grid[row, col] = CellState.BURNED.value

        # Record state for history
        self.burn_history.append(self.grid.copy())

    def simulate(self, weather_sequence: List[WeatherSnapshot], time_steps_per_day: int = 1440):
        """
        Simulate fire spread over multiple days with given weather.
        
        Args:
            weather_sequence: List of WeatherSnapshot objects
            time_steps_per_day: Minutes per day to simulate
        """
        for day, weather in enumerate(weather_sequence):
            for _ in range(time_steps_per_day):
                self.step(weather)

    def get_burn_area(self) -> float:
        """Get currently burned area in square meters."""
        burned_cells = np.sum(self.grid == CellState.BURNED.value)
        return burned_cells * (self.cell_size_m ** 2)

    def get_burning_area(self) -> float:
        """Get currently burning area in square meters."""
        burning_cells = np.sum(self.grid == CellState.BURNING.value)
        return burning_cells * (self.cell_size_m ** 2)

    def get_risk_map(self) -> np.ndarray:
        """
        Get fire risk map (0-1 probability).
        
        Returns:
            2D array with fire risk at each cell
        """
        risk = np.zeros(self.grid_size)
        # Higher risk near burning areas
        for row, col in np.argwhere(self.grid == CellState.BURNING.value):
            for dr in range(-3, 4):
                for dc in range(-3, 4):
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.grid_size[0] and 0 <= nc < self.grid_size[1]:
                        distance = np.sqrt(dr**2 + dc**2)
                        risk[nr, nc] = max(risk[nr, nc], 1.0 / (distance + 1.0))
        return np.clip(risk, 0, 1)


if __name__ == "__main__":
    print("Fire spread model module loaded successfully")
