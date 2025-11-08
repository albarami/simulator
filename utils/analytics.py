"""
Analytics and calculations module for Ministry of Labour dashboard.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.linear_model import LinearRegression


def calculate_revenue_impact(
    df: pd.DataFrame, 
    service_name: str, 
    new_fee: float,
    elasticity: float = 0.0
) -> Dict[str, float]:
    """
    Calculate revenue impact of applying a new fee to a service.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        service_name (str): Name of the service.
        new_fee (float): Proposed fee amount.
        elasticity (float): Demand elasticity (-1.0 to 0.0, default 0 = no change).
        
    Returns:
        dict: Revenue impact metrics.
    """
    service_data = df[df['اسم الخدمة'] == service_name].iloc[0]
    
    # Calculate demand adjustment based on elasticity
    # If elasticity = -0.1, a 100% price increase causes 10% demand decrease
    current_fee = service_data['Current_Fee_Numeric']
    total_requests = service_data['اجمالي العدد']
    
    if current_fee > 0:
        price_change_pct = ((new_fee - current_fee) / current_fee)
    else:
        price_change_pct = 1.0 if new_fee > 0 else 0.0
    
    demand_change_pct = elasticity * price_change_pct
    adjusted_requests = total_requests * (1 + demand_change_pct)
    adjusted_requests = max(0, adjusted_requests)  # Cannot be negative
    
    # Calculate revenues
    current_revenue = total_requests * current_fee
    new_revenue = adjusted_requests * new_fee
    revenue_increase = new_revenue - current_revenue
    
    return {
        'service_name': service_name,
        'current_fee': current_fee,
        'new_fee': new_fee,
        'current_requests': int(total_requests),
        'adjusted_requests': int(adjusted_requests),
        'current_revenue': current_revenue,
        'new_revenue': new_revenue,
        'revenue_increase': revenue_increase,
        'revenue_increase_pct': (revenue_increase / current_revenue * 100) if current_revenue > 0 else 0,
    }


def identify_top_opportunities(
    df: pd.DataFrame, 
    suggested_fee: float = 10.0,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Identify top revenue opportunities (high volume services with no/low fees).
    
    Args:
        df (pd.DataFrame): Services dataframe.
        suggested_fee (float): Default suggested fee for services without fees.
        top_n (int): Number of top opportunities to return.
        
    Returns:
        pd.DataFrame: Top opportunities ranked by potential revenue.
    """
    # Filter services with no current fee or low fee
    opportunities = df[df['Current_Fee_Numeric'] <= 20].copy()
    
    # Calculate potential revenue with suggested fee
    opportunities['Potential_Revenue'] = opportunities['اجمالي العدد'] * suggested_fee
    opportunities['Revenue_Gain'] = (
        opportunities['Potential_Revenue'] - opportunities['Current_Annual_Revenue']
    )
    
    # Sort by revenue gain
    opportunities = opportunities.sort_values('Revenue_Gain', ascending=False)
    
    # Select relevant columns
    result = opportunities[[
        'اسم الخدمة', 
        'اجمالي العدد',
        'Current_Fee_Numeric',
        'Revenue_Gain',
        'Potential_Revenue',
        'Category'
    ]].head(top_n)
    
    return result


def forecast_requests(df: pd.DataFrame, service_name: str, years_ahead: int = 2) -> List[float]:
    """
    Forecast future requests for a service using linear regression.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        service_name (str): Name of the service.
        years_ahead (int): Number of years to forecast.
        
    Returns:
        list: Forecasted request counts.
    """
    service_data = df[df['اسم الخدمة'] == service_name].iloc[0]
    
    # Get historical data
    years = [2022, 2023, 2024, 2025]
    requests = [service_data[2022], service_data[2023], 
                service_data[2024], service_data[2025]]
    
    # Filter out years with zero requests for better forecasting
    valid_data = [(y, r) for y, r in zip(years, requests) if r > 0]
    
    if len(valid_data) < 2:
        # Not enough data, return current average
        avg = service_data['Avg_Requests_Per_Year']
        return [avg] * years_ahead
    
    # Prepare data for regression
    X = np.array([y for y, r in valid_data]).reshape(-1, 1)
    y = np.array([r for y, r in valid_data])
    
    # Fit linear regression
    model = LinearRegression()
    model.fit(X, y)
    
    # Forecast future years
    future_years = np.array([2025 + i + 1 for i in range(years_ahead)]).reshape(-1, 1)
    forecasts = model.predict(future_years)
    
    # Ensure non-negative forecasts
    forecasts = np.maximum(forecasts, 0)
    
    return forecasts.tolist()


def calculate_category_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate performance metrics by service category.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        
    Returns:
        pd.DataFrame: Category performance metrics.
    """
    category_stats = df.groupby('Category').agg({
        'اسم الخدمة': 'count',
        'اجمالي العدد': 'sum',
        'Current_Annual_Revenue': 'sum',
        'Avg_Requests_Per_Year': 'mean',
        'Has_Current_Fee': 'sum'
    }).reset_index()
    
    category_stats.columns = [
        'Category', 
        'Service_Count', 
        'Total_Requests', 
        'Total_Revenue',
        'Avg_Requests_Per_Service',
        'Services_With_Fees'
    ]
    
    # Calculate percentage of services with fees
    category_stats['Fee_Coverage_Pct'] = (
        category_stats['Services_With_Fees'] / category_stats['Service_Count'] * 100
    )
    
    # Sort by total requests
    category_stats = category_stats.sort_values('Total_Requests', ascending=False)
    
    return category_stats


def calculate_scenario_comparison(
    df: pd.DataFrame, 
    scenarios: Dict[str, Dict[str, float]]
) -> pd.DataFrame:
    """
    Compare multiple fee scenarios.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        scenarios (dict): Dictionary of scenario names and their fee configurations.
                         Format: {'Scenario1': {'Service1': fee1, 'Service2': fee2, ...}}
        
    Returns:
        pd.DataFrame: Comparison of scenarios.
    """
    results = []
    
    for scenario_name, fee_config in scenarios.items():
        total_revenue = 0
        services_affected = 0
        
        for service_name, new_fee in fee_config.items():
            if service_name in df['اسم الخدمة'].values:
                impact = calculate_revenue_impact(df, service_name, new_fee)
                total_revenue += impact['new_revenue']
                services_affected += 1
        
        # Add revenue from services not in the scenario (keep current fees)
        unaffected_services = df[~df['اسم الخدمة'].isin(fee_config.keys())]
        total_revenue += unaffected_services['Current_Annual_Revenue'].sum()
        
        results.append({
            'Scenario': scenario_name,
            'Total_Revenue': total_revenue,
            'Services_Modified': services_affected,
            'Total_Services': len(df)
        })
    
    # Add baseline scenario
    baseline_revenue = df['Current_Annual_Revenue'].sum()
    results.insert(0, {
        'Scenario': 'Current (Baseline)',
        'Total_Revenue': baseline_revenue,
        'Services_Modified': 0,
        'Total_Services': len(df)
    })
    
    results_df = pd.DataFrame(results)
    results_df['Revenue_vs_Baseline'] = (
        results_df['Total_Revenue'] - baseline_revenue
    )
    results_df['Increase_Pct'] = (
        results_df['Revenue_vs_Baseline'] / baseline_revenue * 100
    )
    
    return results_df


def calculate_pareto_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform Pareto analysis (80/20 rule) on services by request volume.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        
    Returns:
        pd.DataFrame: Services with cumulative percentage.
    """
    pareto_df = df[['اسم الخدمة', 'اجمالي العدد', 'Current_Annual_Revenue']].copy()
    pareto_df = pareto_df.sort_values('اجمالي العدد', ascending=False)
    
    # Calculate cumulative percentage
    total_requests = pareto_df['اجمالي العدد'].sum()
    pareto_df['Cumulative_Requests'] = pareto_df['اجمالي العدد'].cumsum()
    pareto_df['Cumulative_Pct'] = (
        pareto_df['Cumulative_Requests'] / total_requests * 100
    )
    
    # Calculate percentage of services
    pareto_df['Service_Rank'] = range(1, len(pareto_df) + 1)
    pareto_df['Service_Pct'] = pareto_df['Service_Rank'] / len(pareto_df) * 100
    
    return pareto_df


def get_service_quadrant(df: pd.DataFrame) -> pd.DataFrame:
    """
    Categorize services into quadrants based on volume and revenue.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        
    Returns:
        pd.DataFrame: Services with quadrant classification.
    """
    # Calculate medians
    median_requests = df['اجمالي العدد'].median()
    median_revenue = df['Current_Annual_Revenue'].median()
    
    def assign_quadrant(row):
        """Assign quadrant based on volume and revenue."""
        if row['اجمالي العدد'] >= median_requests:
            if row['Current_Annual_Revenue'] >= median_revenue:
                return "High Volume, High Revenue"
            else:
                return "High Volume, Low Revenue"
        else:
            if row['Current_Annual_Revenue'] >= median_revenue:
                return "Low Volume, High Revenue"
            else:
                return "Low Volume, Low Revenue"
    
    df_copy = df.copy()
    df_copy['Quadrant'] = df_copy.apply(assign_quadrant, axis=1)
    
    return df_copy

