# 🏛️ Ministry of Labour - Fee Strategy & Revenue Optimizer Dashboard

A comprehensive Streamlit dashboard for analyzing service fees, simulating revenue scenarios, and making data-driven decisions for the Ministry of Labour services.

## 📊 Features

### 1. **Executive Summary**
- Real-time KPIs (Total Services, Requests, Revenue, Fee Coverage)
- Key insights and quick actions
- Trend visualizations and top services analysis

### 2. **Revenue Simulator**
- **Single Service Mode**: Simulate fee changes for individual services with demand elasticity
- **Category Mode**: Apply fees to entire service categories
- **Multi-Service Mode**: Customize fees for multiple services simultaneously

### 3. **Top Opportunities**
- Identify high-volume services without fees
- Calculate potential revenue gains
- Visual ranking of opportunities

### 4. **Trend Analysis & Forecasting**
- Historical request trends (2022-2025)
- Category performance analysis
- Machine learning-based forecasting for future years
- Growth rate analysis

### 5. **Service Comparison**
- **Pareto Analysis**: Identify services that generate 80% of requests
- **Quadrant Analysis**: Classify services by volume and revenue
- Strategic recommendations per quadrant

### 6. **Scenario Planning**
- Pre-built strategies (Conservative, Moderate, Aggressive)
- Target revenue optimizer
- Compare multiple scenarios side-by-side
- Export scenarios to Excel

### 7. **Portfolio Analysis**
- Complete service catalog with advanced filters
- Fee status distribution
- Growth metrics and trends

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Run Dashboard

```bash
# Launch the dashboard
streamlit run dashboard.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
D:\simulation\
├── dashboard.py              # Main Streamlit application
├── Book1.xlsx               # Source data (Ministry services)
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── utils/
    ├── __init__.py
    ├── data_loader.py      # Data loading and preprocessing
    ├── analytics.py        # Analytics and calculations
    ├── simulator.py        # Revenue simulation engine
    └── visualizations.py   # Plotly chart functions
```

## 📊 Data Structure

The dashboard expects an Excel file (`Book1.xlsx`) with the following columns:

1. **اسم الخدمة** - Service Name
2. **2022** - Requests in 2022
3. **2023** - Requests in 2023
4. **2024** - Requests in 2024
5. **2025** - Requests in 2025
6. **اجمالي العدد** - Total Requests
7. **الرسوم الحالية** - Current Fees
8. **ملاحظات و مقترح الرسوم** - Notes and Suggested Fees

## 🎯 Use Cases

### For Strategic Planning
- Identify which services to prioritize for fee implementation
- Compare different fee strategies (conservative vs aggressive)
- Forecast future demand and revenue

### For Revenue Optimization
- Find quick wins (high-volume services without fees)
- Optimize fees to meet target revenue goals
- Understand demand elasticity impact

### For Decision Making
- Visualize trade-offs between different scenarios
- Export scenarios for stakeholder review
- Track performance metrics over time

## 💡 Tips for Best Results

1. **Start with Executive Summary** to understand current state
2. **Explore Top Opportunities** to identify quick wins
3. **Use Revenue Simulator** to test specific ideas
4. **Compare Scenarios** to evaluate different strategies
5. **Check Portfolio Analysis** for comprehensive view

## 🎨 Dashboard Highlights

- **Interactive Visualizations**: All charts are interactive with hover details
- **Real-Time Calculations**: Instant feedback on fee changes
- **Multi-Language Support**: Arabic service names supported
- **Export Capabilities**: Save scenarios to Excel for sharing
- **Responsive Design**: Works on desktop and tablet

## 📈 Key Insights from Current Data

- **54 services** across 9 categories
- **3+ million total requests** (2022-2025)
- **68% of services** currently have no fees
- **Significant growth** from 2022 to 2025

## 🔧 Technical Details

- **Framework**: Streamlit 1.31.0
- **Data Analysis**: Pandas, NumPy
- **Visualizations**: Plotly
- **Forecasting**: Scikit-learn (Linear Regression)
- **Language**: Python 3.11+

## 📝 Notes

- Empty cells in year columns indicate no requests for that year
- Demand elasticity default is -0.1 (conservative estimate)
- All monetary values are in Qatari Riyals (QAR)
- Forecasts are based on historical trends using linear regression

## 🆘 Troubleshooting

**Dashboard won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that `Book1.xlsx` is in the same directory

**Data not loading:**
- Verify Excel file name and location
- Ensure Excel file follows the expected structure

**Charts not displaying:**
- Clear browser cache
- Try a different browser
- Check console for JavaScript errors

## 📧 Support

For questions or issues, refer to the Streamlit documentation: https://docs.streamlit.io

---

**Version**: 1.0  
**Last Updated**: November 2025  
**Built for**: Ministry of Labour - State of Qatar

