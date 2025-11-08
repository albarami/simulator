"""
Revenue simulation and scenario planning module.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any


class RevenueSimulator:
    """
    Class for simulating revenue scenarios and fee strategies.
    """
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize the revenue simulator.
        
        Args:
            df (pd.DataFrame): Services dataframe.
        """
        self.df = df.copy()
        self.scenarios = {}
        
    def create_scenario(
        self, 
        scenario_name: str, 
        fee_changes: Dict[str, float],
        description: str = ""
    ) -> Dict[str, Any]:
        """
        Create a new fee scenario.
        
        Args:
            scenario_name (str): Name of the scenario.
            fee_changes (dict): Dictionary mapping service names to new fees.
            description (str): Description of the scenario.
            
        Returns:
            dict: Scenario details and impact.
        """
        scenario_df = self.df.copy()
        total_revenue = 0
        services_modified = []
        
        for service_name, new_fee in fee_changes.items():
            if service_name in scenario_df['اسم الخدمة'].values:
                idx = scenario_df[scenario_df['اسم الخدمة'] == service_name].index[0]
                
                # Store original fee
                original_fee = scenario_df.loc[idx, 'Current_Fee_Numeric']
                
                # Update fee
                scenario_df.loc[idx, 'Current_Fee_Numeric'] = new_fee
                
                # Recalculate revenue
                requests = scenario_df.loc[idx, 'اجمالي العدد']
                scenario_df.loc[idx, 'Current_Annual_Revenue'] = requests * new_fee
                
                services_modified.append({
                    'service': service_name,
                    'original_fee': original_fee,
                    'new_fee': new_fee,
                    'requests': requests,
                    'revenue_change': (new_fee - original_fee) * requests
                })
        
        # Calculate total revenue
        total_revenue = scenario_df['Current_Annual_Revenue'].sum()
        baseline_revenue = self.df['Current_Annual_Revenue'].sum()
        revenue_increase = total_revenue - baseline_revenue
        
        scenario = {
            'name': scenario_name,
            'description': description,
            'dataframe': scenario_df,
            'total_revenue': total_revenue,
            'baseline_revenue': baseline_revenue,
            'revenue_increase': revenue_increase,
            'revenue_increase_pct': (revenue_increase / baseline_revenue * 100) if baseline_revenue > 0 else 0,
            'services_modified': services_modified,
            'num_services_modified': len(services_modified)
        }
        
        self.scenarios[scenario_name] = scenario
        return scenario
    
    def apply_category_fee(
        self, 
        scenario_name: str,
        category: str, 
        fee: float,
        only_no_fee_services: bool = True
    ) -> Dict[str, Any]:
        """
        Apply a fee to all services in a category.
        
        Args:
            scenario_name (str): Name of the scenario.
            category (str): Category name.
            fee (float): Fee to apply.
            only_no_fee_services (bool): Only apply to services without current fees.
            
        Returns:
            dict: Scenario details.
        """
        category_services = self.df[self.df['Category'] == category]
        
        if only_no_fee_services:
            category_services = category_services[category_services['Current_Fee_Numeric'] == 0]
        
        fee_changes = {
            row['اسم الخدمة']: fee 
            for _, row in category_services.iterrows()
        }
        
        description = f"Apply {fee} QAR fee to {category}"
        if only_no_fee_services:
            description += " (services without current fees)"
        
        return self.create_scenario(scenario_name, fee_changes, description)
    
    def apply_tiered_fee_strategy(
        self, 
        scenario_name: str,
        high_volume_threshold: int = 10000,
        high_volume_fee: float = 50.0,
        medium_volume_fee: float = 20.0,
        low_volume_fee: float = 5.0
    ) -> Dict[str, Any]:
        """
        Apply tiered fees based on service volume.
        
        Args:
            scenario_name (str): Name of the scenario.
            high_volume_threshold (int): Threshold for high volume services.
            high_volume_fee (float): Fee for high volume services.
            medium_volume_fee (float): Fee for medium volume services.
            low_volume_fee (float): Fee for low volume services.
            
        Returns:
            dict: Scenario details.
        """
        fee_changes = {}
        
        for _, row in self.df.iterrows():
            if row['Current_Fee_Numeric'] > 0:
                continue  # Skip services that already have fees
            
            service_name = row['اسم الخدمة']
            requests = row['اجمالي العدد']
            
            if requests >= high_volume_threshold:
                fee_changes[service_name] = high_volume_fee
            elif requests >= high_volume_threshold / 4:
                fee_changes[service_name] = medium_volume_fee
            else:
                fee_changes[service_name] = low_volume_fee
        
        description = (
            f"Tiered strategy: {high_volume_fee} QAR (high volume), "
            f"{medium_volume_fee} QAR (medium), {low_volume_fee} QAR (low)"
        )
        
        return self.create_scenario(scenario_name, fee_changes, description)
    
    def optimize_for_target_revenue(
        self,
        scenario_name: str,
        target_revenue: float,
        max_fee: float = 100.0
    ) -> Dict[str, Any]:
        """
        Optimize fees to reach a target revenue.
        
        Args:
            scenario_name (str): Name of the scenario.
            target_revenue (float): Target revenue to achieve.
            max_fee (float): Maximum fee allowed.
            
        Returns:
            dict: Scenario details.
        """
        # Start with baseline revenue
        baseline_revenue = self.df['Current_Annual_Revenue'].sum()
        revenue_gap = target_revenue - baseline_revenue
        
        if revenue_gap <= 0:
            return self.create_scenario(
                scenario_name, 
                {}, 
                f"Target revenue {target_revenue:,.0f} already achieved"
            )
        
        # Get services without fees, sorted by volume
        no_fee_services = self.df[
            self.df['Current_Fee_Numeric'] == 0
        ].sort_values('اجمالي العدد', ascending=False)
        
        fee_changes = {}
        accumulated_revenue = 0
        
        for _, row in no_fee_services.iterrows():
            if accumulated_revenue >= revenue_gap:
                break
            
            service_name = row['اسم الخدمة']
            requests = row['اجمالي العدد']
            
            # Calculate needed fee
            remaining_gap = revenue_gap - accumulated_revenue
            needed_fee = remaining_gap / requests if requests > 0 else 0
            
            # Apply fee (capped at max_fee)
            fee = min(needed_fee, max_fee)
            fee = round(fee)  # Round to whole number
            
            if fee > 0:
                fee_changes[service_name] = fee
                accumulated_revenue += fee * requests
        
        description = (
            f"Optimized to reach target revenue of {target_revenue:,.0f} QAR "
            f"(Gap: {revenue_gap:,.0f} QAR)"
        )
        
        return self.create_scenario(scenario_name, fee_changes, description)
    
    def compare_scenarios(self, scenario_names: List[str] = None) -> pd.DataFrame:
        """
        Compare multiple scenarios.
        
        Args:
            scenario_names (list): List of scenario names to compare. 
                                 If None, compare all scenarios.
        
        Returns:
            pd.DataFrame: Comparison table.
        """
        if scenario_names is None:
            scenario_names = list(self.scenarios.keys())
        
        comparison_data = []
        
        # Add baseline
        baseline_revenue = self.df['Current_Annual_Revenue'].sum()
        comparison_data.append({
            'Scenario': 'Current (Baseline)',
            'Total Revenue': baseline_revenue,
            'Revenue Increase': 0,
            'Increase %': 0,
            'Services Modified': 0
        })
        
        # Add each scenario
        for name in scenario_names:
            if name in self.scenarios:
                scenario = self.scenarios[name]
                comparison_data.append({
                    'Scenario': name,
                    'Total Revenue': scenario['total_revenue'],
                    'Revenue Increase': scenario['revenue_increase'],
                    'Increase %': scenario['revenue_increase_pct'],
                    'Services Modified': scenario['num_services_modified']
                })
        
        return pd.DataFrame(comparison_data)
    
    def get_scenario_details(self, scenario_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a scenario.
        
        Args:
            scenario_name (str): Name of the scenario.
            
        Returns:
            dict: Scenario details.
        """
        if scenario_name not in self.scenarios:
            return None
        
        return self.scenarios[scenario_name]
    
    def export_scenario(self, scenario_name: str, file_path: str):
        """
        Export scenario to Excel file.
        
        Args:
            scenario_name (str): Name of the scenario.
            file_path (str): Path to save the Excel file.
        """
        if scenario_name not in self.scenarios:
            return
        
        scenario = self.scenarios[scenario_name]
        df = scenario['dataframe']
        
        # Select relevant columns for export
        export_df = df[[
            'اسم الخدمة',
            'Category',
            'اجمالي العدد',
            'Current_Fee_Numeric',
            'Current_Annual_Revenue'
        ]].copy()
        
        export_df.columns = [
            'Service Name',
            'Category',
            'Total Requests',
            'Fee (QAR)',
            'Annual Revenue (QAR)'
        ]
        
        export_df.to_excel(file_path, index=False)

