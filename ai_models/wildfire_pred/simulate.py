"""
Wildfire Prediction Simulation

Main script that orchestrates weather simulation and fire spread prediction.
Generates visualizable output for ParaView integration.
"""

import numpy as np
from typing import Tuple
import json
from datetime import datetime

from weather_sim import WeatherSimulator
from fire_model import FireSpreadModel, FireSpreadParameters


def run_integrated_simulation(
    days: int = 10,
    grid_size: Tuple[int, int] = (100, 100),
    cell_size_m: float = 10.0,
    ignition_point: Tuple[int, int] = (50, 50),
) -> dict:
    """
    Run integrated weather and fire spread simulation.
    
    Args:
        days: Number of days to simulate
        grid_size: (rows, cols) for fire simulation grid
        cell_size_m: Physical size of each cell
        ignition_point: (row, col) where fire starts
        
    Returns:
        Dictionary with simulation results and metadata
    """
    print(f"🔥 GeoVision Wildfire Prediction Simulation")
    print(f"📅 Duration: {days} days")
    print(f"🗺️  Grid: {grid_size[0]}x{grid_size[1]} cells @ {cell_size_m}m each")
    print(f"🔴 Ignition: {ignition_point}")
    print("-" * 60)

    # Initialize simulators
    weather_sim = WeatherSimulator(
        initial_temp=25.0,
        initial_humidity=40.0,
        initial_wind=15.0,
    )

    fire_model = FireSpreadModel(
        grid_size=grid_size,
        cell_size_m=cell_size_m,
        params=FireSpreadParameters(
            base_spread_rate=12.0,
            wind_factor=0.6,
            slope_factor=0.3,
        ),
    )

    # Set up terrain (elevation profile)
    x = np.linspace(0, 100, grid_size[1])
    y = np.linspace(0, 100, grid_size[0])
    xx, yy = np.meshgrid(x, y)
    elevation = 500 + 50 * np.sin(xx / 30) * np.cos(yy / 30)
    fire_model.set_terrain(elevation)

    # Set initial fuel moisture
    fuel_moisture = np.random.uniform(30, 60, grid_size)
    fire_model.set_fuel_moisture(fuel_moisture)

    # Start fire at ignition point
    fire_model.ignite_cell(ignition_point[0], ignition_point[1])

    # Generate weather and simulate
    weather_sequence = weather_sim.simulate_period(days)

    print("\n⛅ Weather Forecast:")
    for day, weather in enumerate(weather_sequence[:3], 1):
        print(f"  Day {day}: {weather.weather_state.value} | "
              f"T={weather.temperature:.0f}°C | "
              f"H={weather.humidity:.0f}% | "
              f"W={weather.wind_speed:.0f}km/h")
    if days > 3:
        print(f"  ... ({days - 3} more days)")

    # Run fire simulation
    print("\n🔥 Running Fire Spread Simulation...")
    fire_model.simulate(weather_sequence, time_steps_per_day=1440)

    # Gather results
    results = {
        "metadata": {
            "simulation_date": datetime.now().isoformat(),
            "duration_days": days,
            "grid_size": grid_size,
            "cell_size_m": cell_size_m,
            "ignition_point": ignition_point,
        },
        "weather": [
            {
                "day": w.day,
                "temperature": round(w.temperature, 2),
                "humidity": round(w.humidity, 2),
                "wind_speed": round(w.wind_speed, 2),
                "weather_state": w.weather_state.value,
            }
            for w in weather_sequence
        ],
        "fire": {
            "total_burned_area_m2": round(fire_model.get_burn_area(), 2),
            "total_burned_area_hectares": round(fire_model.get_burn_area() / 10000, 2),
            "currently_burning_area_m2": round(fire_model.get_burning_area(), 2),
            "grid_final_state": fire_model.grid.tolist(),
            "burn_history_length": len(fire_model.burn_history),
        },
        "risk_map": fire_model.get_risk_map().tolist(),
    }

    # Print summary
    print("\n📊 Simulation Results:")
    print(f"  Total Burned Area: {results['fire']['total_burned_area_hectares']:.2f} hectares")
    print(f"  Grid Cells Burned: {np.sum(fire_model.grid == 2)} / {np.prod(grid_size)}")
    print(f"  Peak Fire Extent Day: {weather_sequence.index(max(weather_sequence, key=lambda w: w.wind_speed)) + 1}")

    return results


def export_results(results: dict, output_file: str = "wildfire_sim_results.json"):
    """
    Export simulation results to JSON for ParaView/visualization.
    
    Args:
        results: Results dictionary from simulation
        output_file: Output filename
    """
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to: {output_file}")


def print_fire_summary(results: dict):
    """Print formatted simulation summary."""
    print("\n" + "=" * 60)
    print("🔥 WILDFIRE SIMULATION SUMMARY 🔥")
    print("=" * 60)
    print(f"Simulation Date: {results['metadata']['simulation_date']}")
    print(f"Duration: {results['metadata']['duration_days']} days")
    print(f"Ignition Point: {results['metadata']['ignition_point']}")
    print()
    print("📈 Fire Statistics:")
    print(f"  Total Burned Area: {results['fire']['total_burned_area_hectares']:.2f} hectares")
    print(f"  Currently Burning: {results['fire']['currently_burning_area_m2']:.0f} m²")
    print()
    print("⛅ Peak Weather Conditions:")
    max_wind_day = max(results['weather'], key=lambda x: x['wind_speed'])
    print(f"  Highest Wind: Day {max_wind_day['day']} - {max_wind_day['wind_speed']:.0f} km/h")
    print(f"  Weather: {max_wind_day['weather_state']}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Run simulation
    results = run_integrated_simulation(
        days=10,
        grid_size=(100, 100),
        cell_size_m=10.0,
        ignition_point=(50, 50),
    )

    # Export and display results
    export_results(results, "wildfire_sim_results.json")
    print_fire_summary(results)
