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

