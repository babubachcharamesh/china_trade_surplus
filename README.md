# 🇨🇳 China Trade Explorer (1950–2025)

> **A comprehensive, interactive dashboard visualizing the evolution of China's global trade dominance.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)

## 🌟 Overview
Measurements of Exports, Imports, and Trade Balance from 1950 to present day, with projections up to 2025 and beyond. This application leverages **Streamlit** for a responsive web interface and **Plotly/Altair** for state-of-the-art interactive visualizations.

## ✨ Key Features

### 📊 Interactive Dashboard
- **Real-time Metrics**: Instant view of highest surplus, peak exports, and average growth.
- **Dual-Axis Charts**: Compare Exports vs. Imports over time with trade balance overlays.
- **3D Exploration**: A unique 3D scatter plot visualizing the correlation between trade volume and time.

### 🔍 Deep Dive Visualization
- **Customizable Timeframes**: Slider controls to focus on specific economic eras (e.g., Post-2000 accession to WTO).
- **Multi-Metric Filtering**: Toggle between Exports, Imports, and Balance data points.

### 🤖 AI Forecasting
- **Linear Regression Models**: Predictive analytics estimating future trade trends up to 15 years ahead.
- **Dynamic Scenarios**: Adjust forecast horizons instantly.

### 📄 Professional Reporting
- **PDF Generation**: One-click generation of executive-style PDF reports using `ReportLab`.
- **Data Export**: Download processed datasets in CSV or JSON formats for external analysis.

## 🛠️ Technology Stack
- **Core**: `Python 3.12`, `Streamlit`
- **Visualization**: `Plotly`, `Altair`, `Streamlit Echarts`
- **Analysis**: `Pandas`, `NumPy`, `Scikit-Learn`
- **Reporting**: `ReportLab`

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd trade_surplus_China
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # OR with uv
   uv pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run main.py
   # OR with uv
   uv run streamlit run main.py
   ```

4. **Open in Browser**
   Access the dashboard at `http://localhost:8501`.

## 📦 Deployment
This project is configured for seamless deployment on **Streamlit Cloud**.
- `runtime.txt` ensures Python 3.12 environment.
- `requirements.txt` handles all dependency resolution.

## 📝 License
This project is open-source. Visualizations powered by historical data records.

---
*Built with ❤️ using Streamlit*
