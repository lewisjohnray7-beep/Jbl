# GeoVision AI Digital Twin

A comprehensive geospatial AI platform for terrain analysis, flood simulation, wildfire prediction, infrastructure mapping, and digital twin city visualization using ParaView.

## 🎯 Project Overview

This capstone project integrates advanced 3D visualization (ParaView), geospatial data processing, physics-based simulations, and machine learning to create an AI-ready digital twin platform capable of analyzing and predicting natural disasters at scale.

## 📦 Core Modules

1. **Terrain Analysis** - DEM processing, slope/aspect calculation, viewshed analysis
2. **LiDAR Processing** - Point cloud classification and mesh generation
3. **Satellite Data Visualization** - Multi-spectral imagery and change detection
4. **Drone Imagery Integration** - Orthomosaics and textured 3D models
5. **Flood Simulation** - Physics-based water flow and risk prediction
6. **Wildfire Prediction** - Fire spread simulation and risk forecasting ⭐ **Starting here**
7. **Infrastructure Mapping** - Roads, buildings, utilities visualization
8. **Utility Networks** - Network topology and flow analysis
9. **Digital Twin City** - Real-time 4D city model with sensor integration
10. **AI Dataset Generation** - Synthetic data from simulations

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Visualization** | ParaView, VTK, ParaView Web |
| **Geospatial** | GDAL, PostGIS, Geopandas, QGIS |
| **Point Clouds** | PDAL, PCL, Laspy |
| **Simulations** | PyDEM, HydroSHEDS, CA-based models |
| **ML/AI** | TensorFlow, PyTorch, Detectron2 |
| **Backend** | FastAPI, Python 3.10+ |
| **Frontend** | React, Three.js, Cesium.js |
| **Data** | DVC, PostgreSQL, S3 |
| **DevOps** | Docker, GitHub Actions |

## 📁 Project Structure

```
Jbl/
├── ai_models/                    # ML/AI models
│   ├── wildfire_pred/           # Wildfire prediction module
│   ├── flood_sim/
│   └── terrain_analysis/
├── data_pipeline/               # Geospatial data processing
│   ├── loaders/
│   ├── processors/
│   └── cache/
├── paraview/                    # ParaView integration
│   ├── plugins/
│   ├── catalyst_scripts/
│   └── renderers/
├── api/                         # FastAPI backend
├── web_client/                  # React frontend
├── simulations/                 # Physics-based simulations
├── tests/
├── docker/
├── docs/
└── requirements.txt
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- ParaView 5.11+ (optional for visualization)
- Docker & Docker Compose
- Git

### Installation

```bash
git clone https://github.com/lewisjohnray7-beep/Jbl.git
cd Jbl
pip install -r requirements.txt
```

### Run Wildfire Prediction Module

```bash
python ai_models/wildfire_pred/simulate.py
```

## 📊 Development Roadmap

- **Phase 1** (Weeks 1-2): Foundation & ParaView integration
- **Phase 2** (Weeks 3-6): Core modules implementation
- **Phase 3** (Weeks 7-9): AI/ML integration and deployment
- **Phase 4** (Week 10): Backend API development
- **Phase 5** (Weeks 11-12): Frontend & cloud deployment

## 📝 License

MIT

## 👨‍💻 Author

Lewis John Ray
