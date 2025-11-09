"""
Visualization functions for the Ministry of Labour dashboard.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List


def create_kpi_card(title: str, value: str, delta: str = None, icon: str = "📊") -> str:
    """
    Create HTML for a KPI card.
    
    Args:
        title (str): KPI title.
        value (str): KPI value.
        delta (str): Change indicator (optional).
        icon (str): Emoji icon.
        
    Returns:
        str: HTML string.
    """
    delta_html = f'<p style="color: white; margin: 0; font-size: 12px; opacity: 0.9;">{delta}</p>' if delta else ''
    
    html = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px; border-radius: 10px; text-align: center; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="color: white; margin: 0; font-size: 14px; font-weight: 600;">{icon} {title}</h3>
        <h1 style="color: white; margin: 10px 0; font-size: 32px; font-weight: bold;">{value}</h1>
        {delta_html}
    </div>
    """
    return html


def plot_revenue_trend(df: pd.DataFrame) -> go.Figure:
    """
    Create a line chart showing request trends over years.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        
    Returns:
        plotly.graph_objects.Figure: Trend chart.
    """
    years = [2022, 2023, 2024, 2025]
    year_totals = [df[year].sum() for year in years]
    years = [str(y) for y in years]  # Convert to strings for display
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=year_totals,
        mode='lines+markers',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10),
        fill='tonexty',
        name='Total Requests'
    ))
    
    fig.update_layout(
        title='Total Service Requests Trend (2022-2025)',
        xaxis_title='Year',
        yaxis_title='Number of Requests',
        template='plotly_white',
        hovermode='x unified',
        height=400
    )
    
    return fig


def plot_top_services(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Create a horizontal bar chart of top services by requests.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        top_n (int): Number of top services to show.
        
    Returns:
        plotly.graph_objects.Figure: Bar chart.
    """
    top_services = df.nlargest(top_n, 'اجمالي العدد')
    
    fig = go.Figure(go.Bar(
        y=top_services['اسم الخدمة'],
        x=top_services['اجمالي العدد'],
        orientation='h',
        marker=dict(
            color=top_services['اجمالي العدد'],
            colorscale='Viridis',
            showscale=False
        ),
        text=top_services['اجمالي العدد'],
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f'Top {top_n} Services by Request Volume',
        xaxis_title='Total Requests',
        yaxis_title='',
        template='plotly_white',
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def plot_category_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Create a pie chart showing request distribution by category.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        
    Returns:
        plotly.graph_objects.Figure: Pie chart.
    """
    category_totals = df.groupby('Category')['اجمالي العدد'].sum().reset_index()
    
    fig = go.Figure(go.Pie(
        labels=category_totals['Category'],
        values=category_totals['اجمالي العدد'],
        hole=0.4,
        marker=dict(colors=px.colors.qualitative.Set3)
    ))
    
    fig.update_layout(
        title='Request Distribution by Service Category',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_fee_status(df: pd.DataFrame) -> go.Figure:
    """
    Create a stacked bar chart showing fee status by category.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        
    Returns:
        plotly.graph_objects.Figure: Stacked bar chart.
    """
    fee_status = df.groupby(['Category', 'Has_Current_Fee']).size().unstack(fill_value=0)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='No Fee',
        y=fee_status.index,
        x=fee_status[False] if False in fee_status.columns else [0] * len(fee_status),
        orientation='h',
        marker=dict(color='#ff6b6b')
    ))
    
    fig.add_trace(go.Bar(
        name='Has Fee',
        y=fee_status.index,
        x=fee_status[True] if True in fee_status.columns else [0] * len(fee_status),
        orientation='h',
        marker=dict(color='#51cf66')
    ))
    
    fig.update_layout(
        title='Fee Status by Category',
        xaxis_title='Number of Services',
        yaxis_title='',
        barmode='stack',
        template='plotly_white',
        height=400,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig


def plot_revenue_comparison(baseline: float, scenarios: pd.DataFrame) -> go.Figure:
    """
    Create a bar chart comparing revenue across scenarios.
    
    Args:
        baseline (float): Baseline revenue.
        scenarios (pd.DataFrame): Scenarios comparison dataframe.
        
    Returns:
        plotly.graph_objects.Figure: Bar chart.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=scenarios['Scenario'],
        y=scenarios['Total Revenue'],
        marker=dict(
            color=scenarios['Total Revenue'],
            colorscale='Blues',
            showscale=False
        ),
        text=[f"{val:,.0f}" for val in scenarios['Total Revenue']],
        textposition='outside'
    ))
    
    # Add baseline reference line
    fig.add_hline(
        y=baseline,
        line_dash="dash",
        line_color="red",
        annotation_text="Current Baseline",
        annotation_position="right"
    )
    
    fig.update_layout(
        title='Revenue Comparison Across Scenarios',
        xaxis_title='Scenario',
        yaxis_title='Total Annual Revenue (QAR)',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_quadrant_analysis(df: pd.DataFrame) -> go.Figure:
    """
    Create a scatter plot showing volume vs revenue quadrants.
    
    Args:
        df (pd.DataFrame): Services dataframe with quadrant info.
        
    Returns:
        plotly.graph_objects.Figure: Scatter plot.
    """
    fig = px.scatter(
        df,
        x='اجمالي العدد',
        y='Current_Annual_Revenue',
        color='Quadrant',
        hover_data=['اسم الخدمة', 'Category'],
        size='اجمالي العدد',
        color_discrete_map={
            'High Volume, High Revenue': '#51cf66',
            'High Volume, Low Revenue': '#ffd43b',
            'Low Volume, High Revenue': '#74c0fc',
            'Low Volume, Low Revenue': '#ff6b6b'
        }
    )
    
    # Add median lines
    median_requests = df['اجمالي العدد'].median()
    median_revenue = df['Current_Annual_Revenue'].median()
    
    fig.add_vline(x=median_requests, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_hline(y=median_revenue, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title='Service Portfolio Analysis (Volume vs Revenue)',
        xaxis_title='Total Requests',
        yaxis_title='Current Annual Revenue (QAR)',
        template='plotly_white',
        height=500
    )
    
    return fig


def plot_pareto_chart(pareto_df: pd.DataFrame) -> go.Figure:
    """
    Create a Pareto chart showing cumulative request distribution.
    
    Args:
        pareto_df (pd.DataFrame): Pareto analysis dataframe.
        
    Returns:
        plotly.graph_objects.Figure: Pareto chart.
    """
    top_20 = pareto_df.head(20)
    
    fig = go.Figure()
    
    # Bar chart for individual values
    fig.add_trace(go.Bar(
        x=list(range(1, len(top_20) + 1)),
        y=top_20['اجمالي العدد'],
        name='Requests',
        marker=dict(color='#667eea'),
        yaxis='y'
    ))
    
    # Line chart for cumulative percentage
    fig.add_trace(go.Scatter(
        x=list(range(1, len(top_20) + 1)),
        y=top_20['Cumulative_Pct'],
        name='Cumulative %',
        line=dict(color='#ff6b6b', width=3),
        mode='lines+markers',
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Pareto Analysis: Top 20 Services (80/20 Rule)',
        xaxis_title='Service Rank',
        yaxis=dict(title='Number of Requests'),
        yaxis2=dict(
            title='Cumulative Percentage (%)',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        template='plotly_white',
        height=400,
        hovermode='x unified'
    )
    
    # Add 80% reference line on secondary axis
    fig.add_shape(
        type="line",
        xref="paper",
        yref="y2",
        x0=0,
        x1=1,
        y0=80,
        y1=80,
        line=dict(color="green", width=2, dash="dash")
    )
    
    # Add annotation for 80% line
    fig.add_annotation(
        xref="paper",
        yref="y2",
        x=0.95,
        y=80,
        text="80%",
        showarrow=False,
        font=dict(color="green", size=12),
        yshift=10
    )
    
    return fig


def plot_forecast(historical_data: dict, forecast_data: List[float]) -> go.Figure:
    """
    Create a forecast chart showing historical and predicted values.
    
    Args:
        historical_data (dict): Dictionary of year: value pairs.
        forecast_data (list): List of forecasted values.
        
    Returns:
        plotly.graph_objects.Figure: Forecast chart.
    """
    fig = go.Figure()
    
    # Historical data
    hist_years = list(historical_data.keys())
    hist_values = list(historical_data.values())
    
    fig.add_trace(go.Scatter(
        x=hist_years,
        y=hist_values,
        mode='lines+markers',
        name='Historical',
        line=dict(color='#667eea', width=3),
        marker=dict(size=10)
    ))
    
    # Forecast data
    forecast_years = [int(hist_years[-1]) + i + 1 for i in range(len(forecast_data))]
    
    fig.add_trace(go.Scatter(
        x=forecast_years,
        y=forecast_data,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#ff6b6b', width=3, dash='dash'),
        marker=dict(size=10)
    ))
    
    # Connect last historical point to first forecast point
    fig.add_trace(go.Scatter(
        x=[hist_years[-1], forecast_years[0]],
        y=[hist_values[-1], forecast_data[0]],
        mode='lines',
        line=dict(color='gray', width=2, dash='dot'),
        showlegend=False
    ))
    
    fig.update_layout(
        title='Request Forecast (Next 2 Years)',
        xaxis_title='Year',
        yaxis_title='Number of Requests',
        template='plotly_white',
        height=400,
        hovermode='x unified'
    )
    
    return fig


def plot_opportunities_chart(opportunities_df: pd.DataFrame) -> go.Figure:
    """
    Create a chart showing top revenue opportunities.
    
    Args:
        opportunities_df (pd.DataFrame): Opportunities dataframe.
        
    Returns:
        plotly.graph_objects.Figure: Bar chart.
    """
    fig = go.Figure(go.Bar(
        y=opportunities_df['اسم الخدمة'],
        x=opportunities_df['Revenue_Gain'],
        orientation='h',
        marker=dict(
            color=opportunities_df['Revenue_Gain'],
            colorscale='Reds',
            showscale=False
        ),
        text=[f"{val:,.0f} QAR" for val in opportunities_df['Revenue_Gain']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Top Revenue Opportunities',
        xaxis_title='Potential Revenue Gain (QAR)',
        yaxis_title='',
        template='plotly_white',
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def plot_current_vs_suggested_fees(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Create a grouped bar chart comparing current and suggested fees.
    
    Args:
        df (pd.DataFrame): Services dataframe with suggestion fields.
        top_n (int): Number of services to show.
        
    Returns:
        plotly.graph_objects.Figure: Comparison bar chart.
    """
    # Filter services with suggestions and sort by revenue gap
    comparison_df = df[df['Suggested_Fee_Numeric'] > 0].copy()
    comparison_df = comparison_df.sort_values('Revenue_Gap', ascending=False).head(top_n)
    
    fig = go.Figure()
    
    # Add current fees
    fig.add_trace(go.Bar(
        name='Current Fee',
        x=comparison_df['اسم الخدمة'],
        y=comparison_df['Current_Fee_Numeric'],
        marker=dict(color='#ff6b6b'),
        text=comparison_df['Current_Fee_Numeric'].apply(lambda x: f"{x:.0f}"),
        textposition='outside'
    ))
    
    # Add suggested fees
    fig.add_trace(go.Bar(
        name='Suggested Fee',
        x=comparison_df['اسم الخدمة'],
        y=comparison_df['Suggested_Fee_Numeric'],
        marker=dict(color='#51cf66'),
        text=comparison_df['Suggested_Fee_Numeric'].apply(lambda x: f"{x:.0f}"),
        textposition='outside'
    ))
    
    fig.update_layout(
        title=f'Current vs Suggested Fees - Top {top_n} Opportunities',
        xaxis_title='Service',
        yaxis_title='Fee (QAR)',
        barmode='group',
        template='plotly_white',
        height=500,
        xaxis={'tickangle': -45},
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig


def plot_quick_wins_dashboard(quick_wins_df: pd.DataFrame) -> go.Figure:
    """
    Create a bubble chart visualization for quick wins.
    
    Args:
        quick_wins_df (pd.DataFrame): Quick wins dataframe from identify_quick_wins.
        
    Returns:
        plotly.graph_objects.Figure: Bubble chart.
    """
    fig = px.scatter(
        quick_wins_df,
        x='Current_Fee_Numeric',
        y='Suggested_Fee_Numeric',
        size='اجمالي العدد',
        color='Revenue_Gap',
        hover_data=['اسم الخدمة', 'Fee_Structure_Type'],
        color_continuous_scale='Reds',
        size_max=60
    )
    
    # Add diagonal line (y=x) to show where current = suggested
    max_fee = max(quick_wins_df['Suggested_Fee_Numeric'].max(), 
                   quick_wins_df['Current_Fee_Numeric'].max())
    fig.add_trace(go.Scatter(
        x=[0, max_fee],
        y=[0, max_fee],
        mode='lines',
        line=dict(dash='dash', color='gray', width=1),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title='Quick Wins Analysis: Current vs Suggested Fees',
        xaxis_title='Current Fee (QAR)',
        yaxis_title='Suggested Fee (QAR)',
        template='plotly_white',
        height=500
    )
    
    return fig


def plot_revenue_gap_waterfall(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Create a waterfall chart showing revenue opportunities from suggestions.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        top_n (int): Number of top opportunities to show.
        
    Returns:
        plotly.graph_objects.Figure: Waterfall chart.
    """
    # Get top services by revenue gap
    top_services = df[df['Revenue_Gap'] > 0].nlargest(top_n, 'Revenue_Gap').copy()
    
    # Prepare data for waterfall
    services = top_services['اسم الخدمة'].tolist()
    gaps = top_services['Revenue_Gap'].tolist()
    
    # Add total
    services.append('Total Potential')
    gaps.append(sum(gaps))
    
    # Create waterfall
    fig = go.Figure(go.Waterfall(
        name='Revenue Gap',
        orientation='v',
        measure=['relative'] * top_n + ['total'],
        x=services,
        y=gaps,
        text=[f"{g:,.0f}" for g in gaps],
        textposition='outside',
        connector={'line': {'color': 'rgb(63, 63, 63)'}},
        increasing={'marker': {'color': '#51cf66'}},
        totals={'marker': {'color': '#667eea'}}
    ))
    
    fig.update_layout(
        title=f'Revenue Opportunity Waterfall - Top {top_n} Services',
        xaxis_title='Service',
        yaxis_title='Revenue Gain (QAR)',
        template='plotly_white',
        height=500,
        xaxis={'tickangle': -45}
    )
    
    return fig


def plot_fee_structure_distribution(df: pd.DataFrame) -> go.Figure:
    """
    Create a pie chart showing distribution of fee structure types.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        
    Returns:
        plotly.graph_objects.Figure: Pie chart.
    """
    # Filter services with suggestions
    suggestions_df = df[df['Suggested_Fee_Numeric'] > 0].copy()
    
    # Count by fee structure type
    structure_counts = suggestions_df['Fee_Structure_Type'].value_counts()
    
    fig = go.Figure(go.Pie(
        labels=structure_counts.index,
        values=structure_counts.values,
        hole=0.4,
        marker=dict(colors=px.colors.qualitative.Set2)
    ))
    
    fig.update_layout(
        title='Distribution of Suggested Fee Structures',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_historical_fee_timeline(df: pd.DataFrame) -> go.Figure:
    """
    Create a timeline showing historical fee changes.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        
    Returns:
        plotly.graph_objects.Figure: Timeline chart.
    """
    # Filter services with historical changes
    historical_df = df[df['Has_Historical_Change'] == True].copy()
    
    if len(historical_df) == 0:
        # Return empty chart with message
        fig = go.Figure()
        fig.add_annotation(
            text="No historical fee changes found in data",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14)
        )
        fig.update_layout(
            title='Historical Fee Changes Timeline',
            template='plotly_white',
            height=400
        )
        return fig
    
    fig = go.Figure()
    
    for idx, row in historical_df.iterrows():
        service_name = row['اسم الخدمة'][:30] + '...'
        
        # Add line showing fee change
        fig.add_trace(go.Scatter(
            x=['Original', 'Changed'],
            y=[row['Historical_Original_Fee'], row['Historical_New_Fee']],
            mode='lines+markers',
            name=service_name,
            line=dict(width=2),
            marker=dict(size=10)
        ))
    
    fig.update_layout(
        title='Historical Fee Changes',
        xaxis_title='',
        yaxis_title='Fee (QAR)',
        template='plotly_white',
        height=500,
        hovermode='closest'
    )
    
    return fig


def plot_suggestion_implementation_roadmap(df: pd.DataFrame, priority_services: List[str]) -> go.Figure:
    """
    Create a priority matrix for implementing suggestions.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        priority_services (list): List of service names in priority order.
        
    Returns:
        plotly.graph_objects.Figure: Priority matrix/roadmap.
    """
    # Filter to priority services
    roadmap_df = df[df['اسم الخدمة'].isin(priority_services)].copy()
    
    # Calculate implementation ease score (inverse of complexity)
    # Simple heuristic: flat fees are easier than complex structures
    ease_scores = {
        'flat': 5,
        'per_person': 4,
        'per_month': 4,
        'per_modification': 3,
        'tiered': 2,
        'conditional': 2,
        'none': 0
    }
    
    roadmap_df['Implementation_Ease'] = roadmap_df['Fee_Structure_Type'].map(ease_scores)
    roadmap_df['Revenue_Impact'] = roadmap_df['Revenue_Gap'] / 1000  # Scale for visualization
    
    fig = px.scatter(
        roadmap_df,
        x='Implementation_Ease',
        y='Revenue_Impact',
        size='اجمالي العدد',
        color='Fee_Structure_Type',
        hover_data=['اسم الخدمة', 'Suggested_Fee_Numeric'],
        text='اسم الخدمة'
    )
    
    # Add quadrant lines
    avg_ease = roadmap_df['Implementation_Ease'].mean()
    avg_impact = roadmap_df['Revenue_Impact'].mean()
    
    fig.add_hline(y=avg_impact, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=avg_ease, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    fig.add_annotation(x=4.5, y=roadmap_df['Revenue_Impact'].max() * 0.9,
                       text="Quick Wins", showarrow=False, font=dict(size=12, color="green"))
    fig.add_annotation(x=1.5, y=roadmap_df['Revenue_Impact'].max() * 0.9,
                       text="Major Projects", showarrow=False, font=dict(size=12, color="orange"))
    
    fig.update_layout(
        title='Suggestion Implementation Priority Matrix',
        xaxis_title='Implementation Ease (Higher = Easier)',
        yaxis_title='Revenue Impact (thousands QAR)',
        template='plotly_white',
        height=500
    )
    
    return fig
