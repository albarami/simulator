"""
Ministry of Labour - Fee Strategy & Revenue Optimizer Dashboard

A comprehensive Streamlit dashboard for analyzing service fees and simulating revenue scenarios.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import prepare_dashboard_data
from utils.analytics import (
    calculate_revenue_impact,
    identify_top_opportunities,
    forecast_requests,
    calculate_category_performance,
    calculate_pareto_analysis,
    get_service_quadrant
)
from utils.simulator import RevenueSimulator
from utils.visualizations import (
    create_kpi_card,
    plot_revenue_trend,
    plot_top_services,
    plot_category_distribution,
    plot_fee_status,
    plot_revenue_comparison,
    plot_quadrant_analysis,
    plot_pareto_chart,
    plot_forecast,
    plot_opportunities_chart
)


# Page configuration
st.set_page_config(
    page_title="Ministry of Labour - Fee Strategy Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    h1 {
        color: #667eea;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
    }
    h2 {
        color: #764ba2;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load and cache data (original data only)."""
    return prepare_dashboard_data("Book1.xlsx")


@st.cache_resource
def get_simulator(_df):
    """Initialize and cache simulator."""
    return RevenueSimulator(_df)


def get_active_data(original_df, summary):
    """
    Get the active dataframe (either original or scenario-modified).
    
    Args:
        original_df: Original dataframe
        summary: Original summary
        
    Returns:
        tuple: (active_df, active_summary, is_scenario_active)
    """
    if 'active_scenario' in st.session_state and st.session_state.active_scenario is not None:
        scenario = st.session_state.active_scenario
        modified_df = scenario['dataframe'].copy()
        
        # Recalculate summary for scenario
        from utils.data_loader import get_data_summary
        modified_summary = get_data_summary(modified_df)
        
        return modified_df, modified_summary, True
    
    return original_df.copy(), summary, False


def show_scenario_banner(scenario, original_summary):
    """
    Display banner when a scenario is active.
    
    Args:
        scenario: Active scenario dictionary
        original_summary: Original data summary for comparison
    """
    revenue_increase = scenario['revenue_increase']
    revenue_pct = scenario['revenue_increase_pct']
    
    banner_html = f"""
    <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                padding: 15px 20px; border-radius: 10px; margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: flex; 
                justify-content: space-between; align-items: center;">
        <div style="color: white;">
            <h3 style="margin: 0; font-size: 18px;">
                📊 Scenario Active: <strong>{scenario['name']}</strong>
            </h3>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">
                Revenue Impact: <strong>+{revenue_increase:,.0f} QAR ({revenue_pct:.1f}%)</strong> | 
                {scenario['num_services_modified']} services modified
            </p>
        </div>
    </div>
    """
    
    st.markdown(banner_html, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Reset to Original Data", type="secondary", use_container_width=True):
            st.session_state.active_scenario = None
            st.rerun()


def main():
    """Main dashboard application."""
    
    # Header
    st.title("🏛️ Ministry of Labour - Fee Strategy & Revenue Optimizer")
    st.markdown("**Comprehensive Decision Support System for Service Fee Management**")
    
    # Load data
    try:
        original_df, original_summary = load_data()
        simulator = get_simulator(original_df)
        
        # Get active data (original or scenario)
        df, summary, is_scenario_active = get_active_data(original_df, original_summary)
        
        # Show scenario banner if active
        if is_scenario_active:
            show_scenario_banner(st.session_state.active_scenario, original_summary)
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please ensure Book1.xlsx is in the same directory as this script.")
        return
    
    # Sidebar navigation
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio(
        "Select Section",
        [
            "📈 Executive Summary",
            "🎯 Revenue Simulator",
            "💰 Top Opportunities",
            "📊 Trend Analysis",
            "🔍 Service Comparison",
            "🎭 Scenario Planning",
            "📉 Portfolio Analysis"
        ]
    )
    
    # === EXECUTIVE SUMMARY ===
    if page == "📈 Executive Summary":
        st.header("📈 Executive Summary")
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(
                create_kpi_card(
                    "Total Services",
                    f"{summary['total_services']}",
                    icon="📋"
                ),
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                create_kpi_card(
                    "Total Requests",
                    f"{summary['total_requests']:,}",
                    f"+{summary['total_requests_2025'] - summary['total_requests_2024']:,} from last year",
                    icon="📊"
                ),
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                create_kpi_card(
                    "Current Revenue",
                    f"{summary['current_total_revenue']:,.0f} QAR",
                    icon="💰"
                ),
                unsafe_allow_html=True
            )
        
        with col4:
            fee_coverage = (summary['services_with_fees'] / summary['total_services'] * 100)
            st.markdown(
                create_kpi_card(
                    "Fee Coverage",
                    f"{fee_coverage:.1f}%",
                    f"{summary['services_without_fees']} services without fees",
                    icon="📌"
                ),
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        # Key Insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Key Insights")
            st.info(f"""
            - **{summary['services_without_fees']} services ({summary['services_without_fees']/summary['total_services']*100:.0f}%)** currently have no fees
            - **{summary['total_requests_2024']:,}** requests in 2024
            - **{summary['services_with_suggestions']}** services have suggested fees
            - Average **{summary['avg_requests_per_service']:,.0f}** requests per service
            """)
        
        with col2:
            st.subheader("💡 Quick Actions")
            if st.button("🔍 Find Top Revenue Opportunities", use_container_width=True):
                st.switch_page
            st.button("🎯 Create Revenue Scenario", use_container_width=True)
            st.button("📊 View Detailed Analytics", use_container_width=True)
        
        # Charts
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(plot_revenue_trend(df), use_container_width=True)
        
        with col2:
            st.plotly_chart(plot_category_distribution(df), use_container_width=True)
        
        # Top services table
        st.subheader("📋 Top 10 Services by Volume")
        top_10 = df.nlargest(10, 'اجمالي العدد')[
            ['اسم الخدمة', 'Category', 'اجمالي العدد', 'Current_Fee_Numeric', 'Current_Annual_Revenue']
        ].copy()
        top_10.columns = ['Service Name', 'Category', 'Total Requests', 'Current Fee (QAR)', 'Annual Revenue (QAR)']
        st.dataframe(top_10, use_container_width=True, hide_index=True)
    
    # === REVENUE SIMULATOR ===
    elif page == "🎯 Revenue Simulator":
        st.header("🎯 Interactive Revenue Simulator")
        st.markdown("Simulate the impact of fee changes on individual services or categories.")
        
        # Simulation mode
        sim_mode = st.radio(
            "Simulation Mode",
            ["Single Service", "Service Category", "Multiple Services"],
            horizontal=True
        )
        
        if sim_mode == "Single Service":
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_service = st.selectbox(
                    "Select Service",
                    options=df['اسم الخدمة'].tolist(),
                    index=0
                )
                
                service_data = df[df['اسم الخدمة'] == selected_service].iloc[0]
                
                st.info(f"""
                **Current Status:**
                - Total Requests: **{int(service_data['اجمالي العدد']):,}**
                - Current Fee: **{service_data['Current_Fee_Numeric']} QAR**
                - Current Annual Revenue: **{service_data['Current_Annual_Revenue']:,.0f} QAR**
                - Category: **{service_data['Category']}**
                """)
                
                new_fee = st.slider(
                    "Set New Fee (QAR)",
                    min_value=0,
                    max_value=200,
                    value=int(service_data['Current_Fee_Numeric']) if service_data['Current_Fee_Numeric'] > 0 else 10,
                    step=5
                )
                
                elasticity = st.slider(
                    "Demand Elasticity (Impact on demand)",
                    min_value=-1.0,
                    max_value=0.0,
                    value=-0.1,
                    step=0.05,
                    help="How much demand decreases when fees increase. -0.1 means 10% fee increase = 1% demand decrease"
                )
            
            with col2:
                st.subheader("📊 Impact Analysis")
                
                impact = calculate_revenue_impact(df, selected_service, new_fee, elasticity)
                
                st.metric(
                    "New Annual Revenue",
                    f"{impact['new_revenue']:,.0f} QAR",
                    f"{impact['revenue_increase']:,.0f} QAR ({impact['revenue_increase_pct']:.1f}%)"
                )
                
                st.metric(
                    "Adjusted Requests",
                    f"{impact['adjusted_requests']:,}",
                    f"{impact['adjusted_requests'] - impact['current_requests']:,}"
                )
                
                # Visual comparison
                comparison_data = pd.DataFrame({
                    'Scenario': ['Current', 'New'],
                    'Revenue': [impact['current_revenue'], impact['new_revenue']],
                    'Requests': [impact['current_requests'], impact['adjusted_requests']]
                })
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name='Revenue (QAR)',
                    x=comparison_data['Scenario'],
                    y=comparison_data['Revenue'],
                    marker_color='#667eea'
                ))
                
                fig.update_layout(
                    title='Revenue Comparison',
                    template='plotly_white',
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Apply Scenario Button
                st.markdown("---")
                if st.button("✅ Apply This Scenario", type="primary", use_container_width=True, key="apply_single"):
                    # Create scenario and apply it
                    fee_changes = {selected_service: new_fee}
                    scenario = simulator.create_scenario(
                        f"Single Service: {selected_service[:30]}",
                        fee_changes,
                        f"Apply {new_fee} QAR fee to {selected_service}"
                    )
                    st.session_state.active_scenario = scenario
                    st.success("✅ Scenario applied! Check other tabs to see the impact.")
                    st.rerun()
        
        elif sim_mode == "Service Category":
            col1, col2 = st.columns([2, 1])
            
            with col1:
                categories = df['Category'].unique().tolist()
                selected_category = st.selectbox("Select Category", categories)
                
                category_services = df[df['Category'] == selected_category]
                st.info(f"**{len(category_services)}** services in this category")
                
                new_fee = st.slider(
                    "Apply Fee to All Services in Category (QAR)",
                    min_value=0,
                    max_value=100,
                    value=10,
                    step=5
                )
                
                only_no_fee = st.checkbox("Apply only to services without current fees", value=True)
            
            with col2:
                st.subheader("📊 Category Impact")
                
                scenario = simulator.apply_category_fee(
                    f"Category_{selected_category}",
                    selected_category,
                    new_fee,
                    only_no_fee
                )
                
                st.metric(
                    "Total Revenue Increase",
                    f"{scenario['revenue_increase']:,.0f} QAR",
                    f"+{scenario['revenue_increase_pct']:.1f}%"
                )
                
                st.metric(
                    "Services Modified",
                    f"{scenario['num_services_modified']}"
                )
                
                st.metric(
                    "New Total Revenue",
                    f"{scenario['total_revenue']:,.0f} QAR"
                )
                
                # Apply Scenario Button
                st.markdown("---")
                if st.button("✅ Apply This Scenario", type="primary", use_container_width=True, key="apply_category"):
                    st.session_state.active_scenario = scenario
                    st.success("✅ Scenario applied! Check other tabs to see the impact.")
                    st.rerun()
        
        else:  # Multiple Services
            st.subheader("Select Multiple Services")
            
            selected_services = st.multiselect(
                "Choose services to modify",
                options=df['اسم الخدمة'].tolist(),
                default=[]
            )
            
            if selected_services:
                st.subheader("Set Fees")
                
                fee_changes = {}
                cols = st.columns(3)
                
                for idx, service in enumerate(selected_services):
                    with cols[idx % 3]:
                        current_fee = df[df['اسم الخدمة'] == service]['Current_Fee_Numeric'].iloc[0]
                        fee = st.number_input(
                            f"{service[:30]}...",
                            min_value=0,
                            max_value=200,
                            value=int(current_fee) if current_fee > 0 else 10,
                            step=5,
                            key=f"fee_{idx}"
                        )
                        fee_changes[service] = fee
                
                # Store scenario in session state for display
                if 'multi_service_scenario' not in st.session_state:
                    st.session_state.multi_service_scenario = None
                
                col_calc, col_apply = st.columns(2)
                
                with col_calc:
                    if st.button("Calculate Total Impact", type="secondary", use_container_width=True):
                        scenario = simulator.create_scenario(
                            "Custom_Multi_Service",
                            fee_changes,
                            "Custom multi-service scenario"
                        )
                        st.session_state.multi_service_scenario = scenario
                        st.rerun()
                
                # Show results if calculated
                if st.session_state.multi_service_scenario:
                    scenario = st.session_state.multi_service_scenario
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Revenue Increase",
                            f"{scenario['revenue_increase']:,.0f} QAR",
                            f"+{scenario['revenue_increase_pct']:.1f}%"
                        )
                    
                    with col2:
                        st.metric(
                            "Services Modified",
                            f"{scenario['num_services_modified']}"
                        )
                    
                    with col3:
                        st.metric(
                            "New Total Revenue",
                            f"{scenario['total_revenue']:,.0f} QAR"
                        )
                    
                    # Apply button
                    col_apply_btn, col_clear_btn = st.columns(2)
                    with col_apply_btn:
                        if st.button("✅ Apply This Scenario", type="primary", use_container_width=True, key="apply_multi"):
                            st.session_state.active_scenario = scenario
                            st.session_state.multi_service_scenario = None
                            st.success("✅ Scenario applied! Check other tabs to see the impact.")
                            st.rerun()
    
    # === TOP OPPORTUNITIES ===
    elif page == "💰 Top Opportunities":
        st.header("💰 Top Revenue Opportunities")
        st.markdown("Identify high-impact services where adding fees could generate significant revenue.")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            suggested_fee = st.slider(
                "Suggested Fee (QAR)",
                min_value=1,
                max_value=100,
                value=10,
                step=1
            )
            
            top_n = st.slider(
                "Number of Opportunities",
                min_value=5,
                max_value=20,
                value=10,
                step=1
            )
        
        with col2:
            opportunities = identify_top_opportunities(df, suggested_fee, top_n)
            
            st.plotly_chart(plot_opportunities_chart(opportunities), use_container_width=True)
        
        st.subheader("📋 Detailed Opportunities")
        
        display_df = opportunities.copy()
        display_df.columns = [
            'Service Name', 'Total Requests', 'Current Fee', 
            'Revenue Gain', 'Potential Revenue', 'Category'
        ]
        display_df['Current Fee'] = display_df['Current Fee'].apply(lambda x: f"{x:.0f} QAR")
        display_df['Revenue Gain'] = display_df['Revenue Gain'].apply(lambda x: f"{x:,.0f} QAR")
        display_df['Potential Revenue'] = display_df['Potential Revenue'].apply(lambda x: f"{x:,.0f} QAR")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Summary
        total_potential = opportunities['Revenue_Gain'].sum()
        st.success(f"**Total Potential Revenue from Top {top_n} Opportunities: {total_potential:,.0f} QAR**")
    
    # === TREND ANALYSIS ===
    elif page == "📊 Trend Analysis":
        st.header("📊 Trend Analysis & Forecasting")
        
        # Overall trends
        st.subheader("📈 Overall Request Trends")
        st.plotly_chart(plot_revenue_trend(df), use_container_width=True)
        
        # Category performance
        st.subheader("📊 Performance by Category")
        category_perf = calculate_category_performance(df)
        
        display_perf = category_perf.copy()
        display_perf.columns = [
            'Category', 'Service Count', 'Total Requests', 'Total Revenue',
            'Avg Requests/Service', 'Services with Fees', 'Fee Coverage %'
        ]
        display_perf['Total Revenue'] = display_perf['Total Revenue'].apply(lambda x: f"{x:,.0f} QAR")
        
        st.dataframe(display_perf, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(plot_top_services(df, 15), use_container_width=True)
        
        with col2:
            st.plotly_chart(plot_fee_status(df), use_container_width=True)
        
        # Individual service forecast
        st.subheader("🔮 Service Forecast")
        
        selected_service_forecast = st.selectbox(
            "Select Service for Forecast",
            options=df['اسم الخدمة'].tolist(),
            key="forecast_service"
        )
        
        service_data = df[df['اسم الخدمة'] == selected_service_forecast].iloc[0]
        
        historical = {
            '2022': int(service_data[2022]),
            '2023': int(service_data[2023]),
            '2024': int(service_data[2024]),
            '2025': int(service_data[2025])
        }
        
        forecast = forecast_requests(df, selected_service_forecast, years_ahead=2)
        
        st.plotly_chart(plot_forecast(historical, forecast), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Forecast 2026", f"{int(forecast[0]):,} requests")
        with col2:
            st.metric("Forecast 2027", f"{int(forecast[1]):,} requests")
    
    # === SERVICE COMPARISON ===
    elif page == "🔍 Service Comparison":
        st.header("🔍 Service Comparison & Analysis")
        
        # Pareto Analysis
        st.subheader("📉 Pareto Analysis (80/20 Rule)")
        pareto_df = calculate_pareto_analysis(df)
        st.plotly_chart(plot_pareto_chart(pareto_df), use_container_width=True)
        
        # Find 80% threshold
        services_for_80 = len(pareto_df[pareto_df['Cumulative_Pct'] <= 80])
        pct_services_for_80 = (services_for_80 / len(df) * 100)
        
        st.info(f"""
        **Pareto Insight:** 
        - **{services_for_80} services ({pct_services_for_80:.1f}%)** account for **80%** of all requests
        - Focus fee strategy on these high-volume services for maximum impact
        """)
        
        # Quadrant Analysis
        st.subheader("📊 Portfolio Quadrant Analysis")
        df_quadrant = get_service_quadrant(df)
        st.plotly_chart(plot_quadrant_analysis(df_quadrant), use_container_width=True)
        
        # Quadrant summary
        quadrant_summary = df_quadrant.groupby('Quadrant').agg({
            'اسم الخدمة': 'count',
            'اجمالي العدد': 'sum',
            'Current_Annual_Revenue': 'sum'
        }).reset_index()
        
        st.subheader("📋 Quadrant Summary")
        
        cols = st.columns(4)
        quadrants_info = {
            "High Volume, High Revenue": {"emoji": "🟢", "action": "Maintain & Optimize"},
            "High Volume, Low Revenue": {"emoji": "🟡", "action": "Quick Win - Add Fees"},
            "Low Volume, High Revenue": {"emoji": "🔵", "action": "Premium Services"},
            "Low Volume, Low Revenue": {"emoji": "🔴", "action": "Review Need"}
        }
        
        for idx, (_, row) in enumerate(quadrant_summary.iterrows()):
            with cols[idx]:
                info = quadrants_info.get(row['Quadrant'], {"emoji": "⚪", "action": "Review"})
                st.metric(
                    f"{info['emoji']} {row['Quadrant'].split(',')[0]}",
                    f"{int(row['اسم الخدمة'])} services"
                )
                st.caption(info['action'])
    
    # === SCENARIO PLANNING ===
    elif page == "🎭 Scenario Planning":
        st.header("🎭 Scenario Planning & Comparison")
        st.markdown("Create and compare different fee strategies to find the optimal approach.")
        
        # Pre-built scenarios
        st.subheader("🎯 Quick Scenarios")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💼 Conservative Strategy", use_container_width=True):
                scenario = simulator.apply_tiered_fee_strategy(
                    "Conservative",
                    high_volume_threshold=50000,
                    high_volume_fee=20,
                    medium_volume_fee=10,
                    low_volume_fee=5
                )
                st.session_state['last_scenario'] = scenario
                st.rerun()
        
        with col2:
            if st.button("⚡ Moderate Strategy", use_container_width=True):
                scenario = simulator.apply_tiered_fee_strategy(
                    "Moderate",
                    high_volume_threshold=30000,
                    high_volume_fee=50,
                    medium_volume_fee=20,
                    low_volume_fee=10
                )
                st.session_state['last_scenario'] = scenario
                st.rerun()
        
        with col3:
            if st.button("🚀 Aggressive Strategy", use_container_width=True):
                scenario = simulator.apply_tiered_fee_strategy(
                    "Aggressive",
                    high_volume_threshold=20000,
                    high_volume_fee=100,
                    medium_volume_fee=50,
                    low_volume_fee=20
                )
                st.session_state['last_scenario'] = scenario
                st.rerun()
        
        # Target revenue optimizer
        st.markdown("---")
        st.subheader("🎯 Target Revenue Optimizer")
        
        current_revenue = df['Current_Annual_Revenue'].sum()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            target_revenue = st.number_input(
                "Set Target Annual Revenue (QAR)",
                min_value=int(current_revenue),
                max_value=int(current_revenue * 5),
                value=int(current_revenue * 1.5),
                step=100000
            )
            
            max_fee = st.slider(
                "Maximum Allowed Fee (QAR)",
                min_value=10,
                max_value=200,
                value=100,
                step=10
            )
        
        with col2:
            if st.button("🎯 Optimize", type="primary", use_container_width=True):
                scenario = simulator.optimize_for_target_revenue(
                    "Target_Optimized",
                    target_revenue,
                    max_fee
                )
                st.session_state['last_scenario'] = scenario
                
                if scenario['revenue_increase'] > 0:
                    st.success(f"Target achieved! +{scenario['revenue_increase']:,.0f} QAR")
                else:
                    st.info("Target already met with current fees")
        
        # Display last scenario
        if 'last_scenario' in st.session_state:
            scenario = st.session_state['last_scenario']
            
            st.markdown("---")
            st.subheader(f"📊 Scenario: {scenario['name']}")
            
            if scenario['description']:
                st.info(scenario['description'])
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Revenue", f"{scenario['total_revenue']:,.0f} QAR")
            
            with col2:
                st.metric(
                    "Revenue Increase",
                    f"{scenario['revenue_increase']:,.0f} QAR",
                    f"+{scenario['revenue_increase_pct']:.1f}%"
                )
            
            with col3:
                st.metric("Services Modified", f"{scenario['num_services_modified']}")
            
            with col4:
                col_export, col_apply = st.columns(2)
                with col_export:
                    if st.button("💾 Export", use_container_width=True):
                        filename = f"scenario_{scenario['name']}.xlsx"
                        simulator.export_scenario(scenario['name'], filename)
                        st.success(f"Exported!")
                with col_apply:
                    if st.button("✅ Apply", type="primary", use_container_width=True):
                        st.session_state.active_scenario = scenario
                        st.success("Applied!")
                        st.rerun()
            
            # Services modified table
            if scenario['services_modified']:
                st.subheader("📋 Modified Services")
                
                services_df = pd.DataFrame(scenario['services_modified'])
                services_df.columns = ['Service', 'Original Fee', 'New Fee', 'Requests', 'Revenue Change']
                services_df['Original Fee'] = services_df['Original Fee'].apply(lambda x: f"{x:.0f} QAR")
                services_df['New Fee'] = services_df['New Fee'].apply(lambda x: f"{x:.0f} QAR")
                services_df['Revenue Change'] = services_df['Revenue Change'].apply(lambda x: f"{x:,.0f} QAR")
                
                st.dataframe(services_df, use_container_width=True, hide_index=True)
        
        # Compare all scenarios
        if simulator.scenarios:
            st.markdown("---")
            st.subheader("📊 Scenario Comparison")
            
            comparison_df = simulator.compare_scenarios()
            
            comparison_df['Total Revenue'] = comparison_df['Total Revenue'].apply(lambda x: f"{x:,.0f} QAR")
            comparison_df['Revenue Increase'] = comparison_df['Revenue Increase'].apply(lambda x: f"{x:,.0f} QAR")
            comparison_df['Increase %'] = comparison_df['Increase %'].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    # === PORTFOLIO ANALYSIS ===
    elif page == "📉 Portfolio Analysis":
        st.header("📉 Complete Portfolio Analysis")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📊 Service Distribution")
            st.plotly_chart(plot_category_distribution(df), use_container_width=True)
        
        with col2:
            st.subheader("💰 Fee Status")
            st.plotly_chart(plot_fee_status(df), use_container_width=True)
        
        with col3:
            st.subheader("📈 Growth Metrics")
            growth_2024 = ((df[2024].sum() - df[2023].sum()) / df[2023].sum() * 100)
            st.metric("YoY Growth (2023-2024)", f"{growth_2024:.1f}%")
            
            avg_growth = df[df['Growth_Rate_2023_2024'] != 0]['Growth_Rate_2023_2024'].mean()
            st.metric("Avg Service Growth", f"{avg_growth:.1f}%")
            
            services_growing = (df['Growth_Rate_2023_2024'] > 0).sum()
            st.metric("Growing Services", f"{services_growing}/{len(df)}")
        
        # Full data table with filters
        st.subheader("📋 Complete Service Catalog")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_category = st.multiselect(
                "Filter by Category",
                options=['All'] + df['Category'].unique().tolist(),
                default=['All']
            )
        
        with col2:
            filter_fee_status = st.selectbox(
                "Fee Status",
                options=['All', 'With Fees', 'Without Fees']
            )
        
        with col3:
            min_requests = st.number_input(
                "Minimum Requests",
                min_value=0,
                value=0,
                step=100
            )
        
        # Apply filters
        filtered_df = df.copy()
        
        if 'All' not in filter_category:
            filtered_df = filtered_df[filtered_df['Category'].isin(filter_category)]
        
        if filter_fee_status == 'With Fees':
            filtered_df = filtered_df[filtered_df['Has_Current_Fee'] == True]
        elif filter_fee_status == 'Without Fees':
            filtered_df = filtered_df[filtered_df['Has_Current_Fee'] == False]
        
        filtered_df = filtered_df[filtered_df['اجمالي العدد'] >= min_requests]
        
        # Display table
        display_cols = [
            'اسم الخدمة', 'Category', 2022, 2023, 2024, 2025,
            'اجمالي العدد', 'Current_Fee_Numeric', 'Current_Annual_Revenue'
        ]
        
        display_table = filtered_df[display_cols].copy()
        display_table.columns = [
            'Service Name', 'Category', '2022', '2023', '2024', '2025',
            'Total', 'Fee (QAR)', 'Revenue (QAR)'
        ]
        
        st.dataframe(
            display_table.style.format({
                'Fee (QAR)': '{:.0f}',
                'Revenue (QAR)': '{:,.0f}'
            }),
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        st.info(f"Showing {len(filtered_df)} of {len(df)} services")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        <p>Ministry of Labour - Fee Strategy Dashboard v1.0</p>
        <p>For decision support and revenue optimization</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

