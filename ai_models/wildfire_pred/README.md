# Wildfire Prediction Module

Advanced fire spread simulation combining weather modeling and physics-based cellular automaton.

## 🔥 Features

### Weather Simulation (`weather_sim.py`)
- Realistic weather state generation (Sunny, Cloudy, Rainy, Stormy)
- Temperature, humidity, and wind speed dynamics
- Weather-based fire behavior modulation

### Fire Spread Model (`fire_model.py`)
- **Cellular Automaton** approach for efficient computation
- **Rothermel-inspired** fire behavior calculations
- **Physics-based factors**:
  - Wind speed effect on spread rate
  - Terrain slope influence
  - Fuel moisture content
  - Temperature-dependent burning rate
  - Humidity suppression of fire spread

### Risk Assessment
- Real-time risk map generation
- Burn area tracking
- Fire perimeter analysis

## 📊 Usage

### Basic Simulation
```bash
python simulate.py
```

This runs a 10-day simulation with:
- 100×100 cell grid (10m per cell = 1 km²)
- Terrain elevation profile
- Random initial fuel moisture
- Fire starting at grid center

### Custom Simulation
```python
from weather_sim import WeatherSimulator
from fire_model import FireSpreadModel, FireSpreadParameters
from simulate import run_integrated_simulation

# Run with custom parameters
results = run_integrated_simulation(
    days=14,
    grid_size=(150, 150),
    cell_size_m=5.0,
    ignition_point=(75, 75),
)
```

### Weather-Only Simulation
```python
from weather_sim import run_weather_simulation

weather = run_weather_simulation(days=10, verbose=True)
```

## 📈 Output

Results are exported to `wildfire_sim_results.json`:

```json
{
  "metadata": {
    "simulation_date": "2026-06-19T...",
    "duration_days": 10,
    "grid_size": [100, 100],
    "cell_size_m": 10.0,
    "ignition_point": [50, 50]
  },
  "weather": [...],
  "fire": {
    "total_burned_area_hectares": 45.2,
    "currently_burning_area_m2": 1250.0,
    "grid_final_state": [...],
    "burn_history_length": 14400
  },
  "risk_map": [...]
}
```

## 🔧 Parameters

### WeatherSimulator
- `initial_temp`: Starting temperature (°C)
- `initial_humidity`: Starting humidity (%)
- `initial_wind`: Starting wind speed (km/h)

### FireSpreadModel
- `grid_size`: Simulation grid dimensions
- `cell_size_m`: Physical size per cell (meters)

### FireSpreadParameters
- `base_spread_rate`: 10 m/min (default)
- `wind_factor`: 0.5 multiplier
- `slope_factor`: 0.3 multiplier
- `humidity_suppression`: 0.8 at 100% humidity
- `temperature_enhancement`: 1.2 per 10°C above 20°C

## 📊 Weather State Logic

| Humidity | Wind | State |
|----------|------|-------|
| >85% | >30 km/h | **Stormy** |
| >70% | Any | **Rainy** |
| >50% | Any | **Cloudy** |
| ≤50% | Any | **Sunny** |

## 🚀 Future Enhancements

- [ ] Integration with real weather APIs (NOAA, OpenWeather)
- [ ] Satellite burn detection feedback loop
- [ ] ML model for fire extent prediction
- [ ] ParaView visualization plugin
- [ ] 3D fire simulation
- [ ] Evacuation routing integration
- [ ] Real-time IoT sensor integration

## 📚 References

- Rothermel, R. C. (1972). "A mathematical model for predicting fire spread in wildland fuels"
- Cellular Automata for fire simulation (Green & Vastano, 1992)
- Fuel moisture calculations from NFDRS

## 👨‍💻 Author

GeoVision AI Labs
