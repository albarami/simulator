# 🏛️ Ministry of Labour - Fee Strategy & Revenue Optimizer Dashboard

A comprehensive Streamlit dashboard for analyzing service fees, simulating revenue scenarios, and making data-driven decisions for the Ministry of Labour services in Qatar.

![Dashboard Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Dashboard Features](#dashboard-features)
- [How to Use](#how-to-use)
- [Apply Scenario Feature](#apply-scenario-feature)
- [Deployment](#deployment)
- [Data Structure](#data-structure)
- [Tips & Best Practices](#tips--best-practices)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This dashboard helps the Ministry of Labour analyze and optimize service fees by:

- **Analyzing** 54 services with historical data (2022-2025)
- **Simulating** "what-if" scenarios for fee changes
- **Forecasting** future demand using machine learning
- **Identifying** high-impact revenue opportunities
- **Comparing** multiple fee strategies side-by-side
- **Applying** scenarios across all analytics in real-time

### Key Statistics
- 📊 **54 services** across 9 categories
- 📈 **3+ million requests** tracked (2022-2025)
- 💰 **68% services** currently without fees
- 🎯 **Smart recommendations** for fee optimization

---

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/albarami/simulator.git
cd simulator
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the dashboard:**
```bash
streamlit run dashboard.py
```

4. **Open in browser:**
The dashboard will automatically open at `http://localhost:8501`

---

## 📊 Dashboard Features

### 1. 📈 **Executive Summary**

Your command center for high-level insights.

**What you see:**
- Total services, requests, and current revenue
- Fee coverage percentage
- **NEW:** Services with suggested fees and untapped revenue potential
- **NEW:** High confidence suggestions and quick wins available
- Year-over-year growth trends
- Top 10 services by volume
- Category distribution charts

**How to use:**
- Start here to understand the current state
- Check KPI cards for quick metrics
- **NEW:** View untapped revenue from documented fee suggestions
- Review trends to see growth patterns
- Identify which categories dominate requests

**Best for:** Getting an overview before diving into details

---

### 2. 🎯 **Revenue Simulator** (Enhanced)

Test "what-if" scenarios before implementing changes.

**NEW: Suggested Fee Integration**
- When selecting a service, if a fee suggestion exists, it's automatically shown
- View suggested fee amount, type, and confidence score
- See full suggestion details from notes
- One-click "Use Suggested Fee" button pre-populates the slider
- Makes it easy to test documented recommendations

#### **Mode 1: Single Service**

**Step-by-step:**
1. Select a service from the dropdown
2. Current status shows: requests, current fee, revenue, category
3. Use slider to set new fee (0-200 QAR)
4. Adjust demand elasticity (-1.0 to 0.0)
   - `-0.1` = Conservative (10% price increase = 1% demand decrease)
   - `-0.5` = Aggressive (10% price increase = 5% demand decrease)
5. View instant impact on revenue and requests
6. Click **"✅ Apply This Scenario"** to see impact across all tabs

**Example:**
```
Service: تجديد ترخيص عمل عام
Current Fee: 0 QAR
New Fee: 10 QAR
Requests: 681,475
→ Impact: +6,814,750 QAR annual revenue
```

#### **Mode 2: Service Category**

**Step-by-step:**
1. Select a category (e.g., "Work Permits & Recruitment")
2. Set fee to apply to all services in category
3. Choose: Apply to all services OR only services without fees
4. View total category impact
5. Click **"✅ Apply This Scenario"**

**Use case:** Implement consistent pricing across similar services

#### **Mode 3: Multiple Services**

**Step-by-step:**
1. Select multiple services using the multiselect dropdown
2. Set individual fees for each service
3. Click **"Calculate Total Impact"** to see combined effect
4. Review metrics (revenue increase, services modified)
5. Click **"✅ Apply This Scenario"**

**Use case:** Test custom fee combinations for specific services

---

### 3. 💰 **Top Opportunities**

Find quick wins - high-volume services without fees.

**How to use:**
1. Set suggested fee using slider (1-100 QAR)
2. Choose number of opportunities to display (5-20)
3. Review chart showing potential revenue gain
4. Examine detailed table with service names, requests, and potential revenue
5. Note the total potential revenue at the bottom

**Strategy tips:**
- Start with 5-10 QAR for low-risk testing
- Focus on services with 10,000+ requests
- Prioritize services in high-demand categories

**Example output:**
```
Top Opportunity: تجديد ترخيص عمل عام
- Current Fee: 0 QAR
- Requests: 681,475
- With 10 QAR fee → +6.8M QAR/year
```

---

### 4. 💡 **Quick Wins with Suggested Fees** ✨ NEW

Discover high-impact opportunities with **documented fee suggestions** from operational data.

**What makes this different:**
- Uses **actual fee suggestions** extracted from the notes column
- Parses Arabic text to identify specific fee recommendations
- Shows different fee structures (flat, per-person, per-month, tiered, conditional)
- Includes confidence scores for each suggestion
- Displays special conditions (government vs private pricing, etc.)

**Key Features:**

#### **KPI Dashboard**
- Services with suggestions count and percentage
- Total untapped revenue potential
- Quick wins count (high volume + no fee + has suggestion)
- High confidence suggestions available

#### **Top Quick Wins Table**
Each quick win shows:
- Service name and category
- Current fee vs suggested fee
- Total requests and revenue potential
- Fee structure type (e.g., "per person", "per month")
- Confidence score
- **Full original suggestion text** from notes
- Special conditions if any

**Example Quick Win:**
```
Service: تغيير جهة عمل (داخل سوق العمل القطري)
- Requests: 305,575
- Current Fee: 0 QAR
- Suggested Fee: 100 QAR (conditional)
- Fee Type: Conditional (for private companies)
- Potential Revenue: 30,557,500 QAR
- Confidence: 80%
- Note: "مئة ريال في حال الجهة الجديدة شركة خاصة"
```

#### **Visualizations**
1. **Revenue Gap Waterfall** - Shows cumulative revenue potential
2. **Current vs Suggested Fees** - Side-by-side bar chart comparison
3. **Fee Structure Distribution** - Pie chart of suggestion types

#### **Batch Actions**
One-click implementation of multiple suggestions:
- **Apply Top 5 Suggestions** - Implement the 5 highest-impact suggestions
- **Conservative (50%)** - Apply 50% of all suggested fees
- **Aggressive (100%)** - Apply 100% of all suggested fees

Each batch action creates a scenario you can review across all dashboard sections.

#### **Export Functionality**
Download complete quick wins report as CSV including:
- Service details
- Current and suggested fees
- Revenue calculations
- Fee structure types
- Original suggestion notes

**Real Impact Example:**
From analyzing the data, top 4 quick wins alone offer **~53 Million QAR** potential:
1. تغيير جهة عمل (305K requests) → 100 QAR = 30.5M QAR
2. تعديل موافقة استقدام (225K requests) → 3 QAR = 675K QAR
3. طلب عمل إعارة (213K requests) → 100 QAR = 21.3M QAR
4. اصدار موافقة استقدام (189K requests) → 2-5 QAR = 378K-945K QAR

**How to Use:**
1. Review KPIs to see total opportunity size
2. Adjust minimum volume threshold to filter results
3. Expand each service to see full details and original suggestion
4. Click "Apply to Simulator" to test individual suggestions
5. Use batch actions to implement multiple suggestions at once
6. Export report for stakeholder review

**Best for:** Making data-driven decisions based on documented operational knowledge

---

### 5. 📊 **Trend Analysis & Forecasting**

Understand historical patterns and predict future demand.

**Features:**

#### **Overall Trends**
- Line chart showing total requests 2022-2025
- Identify growth or decline patterns
- Spot seasonal variations

#### **Category Performance**
- Compare categories by: service count, total requests, revenue
- See which categories have fee coverage
- Identify underperforming categories

#### **Service Forecast**
**How to use:**
1. Select any service from dropdown
2. View historical data (2022-2025)
3. See ML-predicted forecasts for 2026-2027
4. Use forecasts to plan capacity and revenue projections

**Example:**
```
Service: تصديق عقود عمل
2024: 452,306 requests
2025: 567,003 requests
Forecast 2026: 682,000 requests (predicted)
```

---

### 5. 🔍 **Service Comparison**

Analyze service portfolio using proven business frameworks.

#### **Pareto Analysis (80/20 Rule)**

**What it shows:**
- Bar chart: Individual service volumes
- Line chart: Cumulative percentage
- Green line: 80% threshold

**Insight:**
"20% of services generate 80% of requests - focus fee strategy here"

**How to read:**
- Services ranked by volume (left to right)
- First few services = highest impact opportunities
- Services below 80% line = lower priority

#### **Portfolio Quadrant Analysis**

Services categorized into 4 strategic groups:

| Quadrant | Volume | Revenue | Strategy |
|----------|--------|---------|----------|
| 🟢 **High/High** | High | High | Maintain & Optimize |
| 🟡 **High/Low** | High | Low | **Quick Win - Add Fees** |
| 🔵 **Low/High** | Low | High | Premium Services |
| 🔴 **Low/Low** | Low | Low | Review Need |

**How to use:**
1. View scatter plot with services positioned by volume & revenue
2. Focus on 🟡 High Volume/Low Revenue = biggest opportunities
3. Check quadrant summary cards for counts
4. Use strategies suggested for each quadrant

---

### 6. 🎭 **Scenario Planning**

Create and compare comprehensive fee strategies.

#### **Quick Scenarios**

Three pre-built strategies ready to test:

**💼 Conservative Strategy**
- High volume services (50K+ requests): 20 QAR
- Medium volume: 10 QAR
- Low volume: 5 QAR
- **Best for:** Risk-averse approach, minimal disruption

**⚡ Moderate Strategy**
- High volume services (30K+ requests): 50 QAR
- Medium volume: 20 QAR
- Low volume: 10 QAR
- **Best for:** Balanced revenue growth

**🚀 Aggressive Strategy**
- High volume services (20K+ requests): 100 QAR
- Medium volume: 50 QAR
- Low volume: 20 QAR
- **Best for:** Maximum revenue generation

**How to use:**
1. Click any strategy button
2. Review scenario details and services modified
3. Click **"✅ Apply"** button to activate
4. Navigate to other tabs to see full impact

#### **Target Revenue Optimizer**

Automatically calculate fees to reach revenue goals.

**Step-by-step:**
1. Set target annual revenue (e.g., 10,000,000 QAR)
2. Set maximum allowed fee per service (e.g., 100 QAR)
3. Click **"🎯 Optimize"**
4. System automatically assigns fees to reach target
5. Review which services get fees
6. Click **"✅ Apply"** if satisfied

**How it works:**
- Prioritizes high-volume services
- Stays within max fee limit
- Optimizes to reach target with minimal services modified

#### **Scenario Comparison**

Compare all created scenarios side-by-side:
- See total revenue for each
- Compare revenue increase percentages
- Review number of services modified
- Export scenarios to Excel for reports

---

### 7. 📉 **Portfolio Analysis**

Complete service catalog with advanced filtering.

**Filters available:**
- **Category filter:** Select specific categories
- **Fee status:** All / With Fees / Without Fees
- **Minimum requests:** Filter by volume threshold

**Table columns:**
- Service name
- Category
- Yearly requests (2022-2025)
- Total requests
- Current fee
- Current annual revenue

**How to use:**
1. Set filters to narrow down services
2. Review complete data in table
3. Sort by clicking column headers
4. Use for detailed analysis and reporting

---

## ✨ Apply Scenario Feature

### **What is it?**

The Apply Scenario feature lets you test fee changes in the simulator, then **apply them across the entire dashboard** to see the full impact on all analytics, charts, and reports.

### **How it works:**

#### **Step 1: Create Scenario**
- Use Revenue Simulator or Scenario Planning
- Set fees for one or more services
- Review calculated impact

#### **Step 2: Apply Scenario**
- Click **"✅ Apply This Scenario"** button
- Green banner appears at top of dashboard
- Banner shows:
  - Scenario name
  - Revenue impact (+X QAR, Y%)
  - Number of services modified
  - **"🔄 Reset to Original Data"** button

#### **Step 3: Explore Impact**
Navigate to any tab and see updated data:
- ✅ Executive Summary: Updated KPIs and metrics
- ✅ Top Opportunities: Recalculated with new fees
- ✅ Trend Analysis: Adjusted revenue projections
- ✅ Service Comparison: Updated Pareto and quadrants
- ✅ Portfolio Analysis: Modified fee values in table

#### **Step 4: Reset When Done**
- Click **"🔄 Reset to Original Data"** in green banner
- Dashboard returns to original state
- Ready to test another scenario

### **Use Cases:**

**Stakeholder Presentations:**
```
1. Apply "Moderate Strategy"
2. Navigate through all tabs showing impact
3. Present comprehensive analysis with one scenario active
4. Reset and show "Aggressive Strategy" for comparison
```

**Decision Making:**
```
1. Test multiple scenarios
2. Apply each one to see full dashboard impact
3. Compare metrics across tabs
4. Choose best strategy based on comprehensive view
```

**What-If Analysis:**
```
1. "What if we only add fees to high-volume services?"
2. Apply scenario → Check Executive Summary
3. "How does this affect revenue distribution?"
4. Check Portfolio Analysis with scenario active
```

---

## 🌐 Deployment

### **Deploy to Streamlit Cloud (Free)**

1. **Go to:** https://streamlit.io/cloud
2. **Sign in** with GitHub
3. **Click** "New app"
4. **Fill in:**
   - Repository: `albarami/simulator`
   - Branch: `main`
   - Main file: `dashboard.py`
   - App URL: Choose custom name (e.g., `mol-fee-optimizer`)
5. **Click** "Deploy!"
6. **Wait** 2-5 minutes
7. **Done!** Get your public URL: `https://[your-app].streamlit.app`

### **Auto-Updates**

When you push changes to GitHub:
```bash
git add .
git commit -m "Update dashboard"
git push origin main
```
Streamlit Cloud automatically redeploys! 🎉

---

## 📁 Data Structure

### **Input File: Book1.xlsx**

Required columns:

| Column Name (Arabic) | Data Type | Description |
|---------------------|-----------|-------------|
| اسم الخدمة | Text | Service name |
| 2022 | Number | Requests in 2022 |
| 2023 | Number | Requests in 2023 |
| 2024 | Number | Requests in 2024 |
| 2025 | Number | Requests in 2025 |
| اجمالي العدد | Number | Total requests |
| الرسوم الحالية | Text | Current fees (can be "لا يوجد" or number) |
| ملاحظات و مقترح الرسوم | Text | **Notes and suggested fees** ⭐ NEW |

**Empty cells:** Treated as zero requests (no data for that year)

#### **✨ NEW: Enhanced Notes Column (ملاحظات و مقترح الرسوم)**

This column now powers the Quick Wins feature by automatically parsing Arabic text to extract:

**Supported fee structures:**
- **Flat fees:** "مئة ريال" → 100 QAR
- **Per-person pricing:** "عشرة ريال عن كل شخص" → 10 QAR per person
- **Per-month pricing:** "مئة ريال عن كل شهر" → 100 QAR per month
- **Per-modification:** "ثلاث ريال عن كل تعديل" → 3 QAR per modification
- **Tiered pricing:** "خمسة ريال لكل مهنة تخصصية, اثنين ريال لكل مهنة غير تخصصية" → 5/2 QAR
- **Conditional pricing:** "مئة ريال في حال الجهة الجديدة شركة خاصة" → 100 QAR for private companies

**Historical changes:**
- Detects phrases like "كانت 500 و تم تعديل القيمة الى 100" to track fee evolution
- Useful for understanding past pricing decisions and their impacts

**Special conditions:**
- Automatically identifies government vs private pricing
- Flags services for specific entity types
- Notes disciplinary vs regular pricing variations

### **Updating Data**

To update with new data:
1. Replace `Book1.xlsx` with new file (keep same structure)
2. Restart dashboard or refresh browser
3. Data automatically reloads

---

## 💡 Tips & Best Practices

### **For Analysts**

1. **Start broad, then narrow:**
   - Begin with Executive Summary
   - Identify trends in Trend Analysis
   - Focus on opportunities in Top Opportunities
   - Drill down in Portfolio Analysis

2. **Use Apply Scenario for presentations:**
   - Prepare 2-3 scenarios beforehand
   - Apply during presentation to show live impact
   - Switch between scenarios for comparison

3. **Combine insights:**
   - Use Pareto to find top 20% services
   - Check their categories in Portfolio Analysis
   - Create category-based scenario in Simulator

### **For Decision Makers**

1. **Test before implementing:**
   - Use conservative elasticity (-0.1) for safer estimates
   - Start with Quick Opportunities (5-10 QAR)
   - Review impact across all tabs with Apply Scenario

2. **Consider categories:**
   - Group similar services with consistent pricing
   - Use Service Category mode in simulator
   - Check category performance in Trend Analysis

3. **Monitor forecasts:**
   - Check predicted demand for 2026-2027
   - Plan fees based on expected growth
   - Adjust strategies for declining services

### **For Presentations**

1. **Story flow:**
   - Executive Summary: "Here's where we are"
   - Top Opportunities: "Here's the potential"
   - Revenue Simulator: "Here's what happens if..."
   - Apply Scenario: "Let's see the full impact"
   - Scenario Planning: "Compare strategies"

2. **Use visuals:**
   - Charts are interactive (hover for details)
   - Zoom in on important sections
   - Export scenarios to Excel for reports

---

## 🔧 Troubleshooting

### **Dashboard won't start**

**Problem:** Error loading data
**Solution:**
```bash
# Ensure Book1.xlsx is in the same directory
ls Book1.xlsx

# Reinstall dependencies
pip install -r requirements.txt

# Try running again
streamlit run dashboard.py
```

### **Charts not displaying**

**Problem:** Blank visualization areas
**Solution:**
- Clear browser cache (Ctrl+F5 or Cmd+Shift+R)
- Try different browser (Chrome recommended)
- Check browser console for errors (F12)

### **Scenario not applying**

**Problem:** Clicked Apply but no banner appears
**Solution:**
- Wait 2-3 seconds for page refresh
- Check if button was clicked (should show success message)
- Navigate to different tab and back

### **Slow performance**

**Problem:** Dashboard loading slowly
**Solution:**
- Reduce number of services in multi-service mode
- Filter data in Portfolio Analysis
- Clear browser cache
- Restart Streamlit server

### **Excel file errors**

**Problem:** "Error loading data" message
**Solution:**
- Ensure Excel file has correct column names (Arabic)
- Check for missing columns
- Verify Excel file is not corrupted
- Ensure file is not open in Excel (close it)

---

## 📚 Technical Details

### **Architecture**

```
dashboard.py           # Main Streamlit application
├── utils/
│   ├── data_loader.py    # Data loading & preprocessing
│   ├── analytics.py      # Analytics functions
│   ├── simulator.py      # Scenario simulation engine
│   └── visualizations.py # Plotly chart generation
├── Book1.xlsx         # Source data
└── requirements.txt   # Python dependencies
```

### **Key Technologies**

- **Streamlit 1.31.0** - Web framework
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **Scikit-learn** - ML forecasting (Linear Regression)
- **NumPy** - Numerical computations

### **Features**

- 🔄 Real-time calculations
- 💾 Session state management for scenarios
- 📊 9 categories of services
- 🎯 Demand elasticity modeling
- 🔮 ML-based forecasting
- 📈 Pareto analysis
- 🎨 Responsive design

---

## 📞 Support

### **Common Questions**

**Q: Can I use my own Excel file?**
A: Yes! Just ensure it has the same column structure (see Data Structure section)

**Q: How many scenarios can I create?**
A: Unlimited! Create, compare, and apply as many as needed.

**Q: Can I export results?**
A: Yes! Use the Export button in Scenario Planning to save scenarios to Excel.

**Q: Is the data secure?**
A: If deployed on Streamlit Cloud, the repository is public. For sensitive data, use a private repository or deploy on private infrastructure.

**Q: Can I add more services?**
A: Yes! Add rows to the Excel file with the same column structure.

---

## 🎓 Learning Resources

### **Streamlit Documentation**
- https://docs.streamlit.io

### **Dashboard Concepts**
- **Pareto Analysis**: 80/20 rule for prioritization
- **Demand Elasticity**: How price changes affect demand
- **Portfolio Analysis**: BCG Matrix-style categorization

### **For Developers**

Want to customize? Check these files:
- `dashboard.py` - Modify UI and layout
- `utils/visualizations.py` - Customize charts
- `utils/simulator.py` - Adjust simulation logic
- `utils/analytics.py` - Add new analytics

---

## 📄 License

This project is developed for the Ministry of Labour - State of Qatar.

---

## 🌟 Version History

**v1.0** (November 2025)
- ✅ Initial release
- ✅ 7 dashboard sections
- ✅ Apply Scenario feature
- ✅ ML-based forecasting
- ✅ 54 services tracked
- ✅ GitHub deployment

---

## 👥 Credits

**Developed by:** AI Assistant with User Collaboration
**For:** Ministry of Labour - State of Qatar
**Repository:** https://github.com/albarami/simulator

---

## 🚀 Get Started Now!

```bash
# Clone and run
git clone https://github.com/albarami/simulator.git
cd simulator
pip install -r requirements.txt
streamlit run dashboard.py
```

**Open your browser and start optimizing! 🎯**
