"""
Data loading and preprocessing module for Ministry of Labour services data.
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any


def load_services_data(file_path: str = "Book1.xlsx") -> pd.DataFrame:
    """
    Load and preprocess the Ministry of Labour services data from Excel.
    
    Args:
        file_path (str): Path to the Excel file.
        
    Returns:
        pd.DataFrame: Cleaned and processed services data.
    """
    # Read Excel file
    df = pd.read_excel(file_path)
    
    # Clean column names (remove trailing spaces)
    df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
    
    # Year columns are integers in the Excel file
    year_columns = [2022, 2023, 2024, 2025]
    
    # Fill NaN values in year columns with 0
    for col in year_columns:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)
    
    # Fill NaN in total column
    if 'اجمالي العدد' in df.columns:
        df['اجمالي العدد'] = df['اجمالي العدد'].fillna(0).astype(int)
    
    return df


def extract_current_fee(fee_text: str) -> float:
    """
    Extract numeric fee value from the current fee column.
    
    Args:
        fee_text (str): Fee text from the data.
        
    Returns:
        float: Numeric fee value (0 if no fee).
    """
    if pd.isna(fee_text):
        return 0.0
    
    fee_str = str(fee_text).strip()
    
    # Check for "لا يوجد" (no fee)
    if "لا يوجد" in fee_str or "الغاء" in fee_str:
        return 0.0
    
    # Extract numeric values
    try:
        # Try to find numbers in the string
        numbers = [int(s) for s in fee_str.split() if s.isdigit()]
        if numbers:
            return float(numbers[0])
    except:
        pass
    
    return 0.0


def categorize_services(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add service categories based on service names and characteristics.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        
    Returns:
        pd.DataFrame: Dataframe with added category column.
    """
    df_copy = df.copy()
    
    def get_category(service_name: str) -> str:
        """Categorize service based on name."""
        service_name = str(service_name).lower()
        
        if "استقدام" in service_name or "موافقة" in service_name:
            return "Work Permits & Recruitment"
        elif "ترخيص" in service_name or "تجديد" in service_name:
            return "License Renewal"
        elif "عقد" in service_name or "تصديق" in service_name:
            return "Contract Certification"
        elif "شهادة" in service_name:
            return "Certificates"
        elif "سجل" in service_name or "منشأة" in service_name:
            return "Establishment Registration"
        elif "تغيير" in service_name or "نقل" in service_name:
            return "Employment Changes"
        elif "اعارة" in service_name:
            return "Work Loans"
        elif "انهاء" in service_name:
            return "Contract Termination"
        else:
            return "Other Services"
    
    df_copy['Category'] = df_copy['اسم الخدمة'].apply(get_category)
    
    return df_copy


def add_calculated_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add calculated fields for analysis.
    
    Args:
        df (pd.DataFrame): Services dataframe.
        
    Returns:
        pd.DataFrame: Dataframe with calculated fields.
    """
    df_copy = df.copy()
    
    # Extract numeric current fee
    df_copy['Current_Fee_Numeric'] = df_copy['الرسوم الحالية'].apply(extract_current_fee)
    
    # Calculate current annual revenue
    df_copy['Current_Annual_Revenue'] = (
        df_copy['اجمالي العدد'] * df_copy['Current_Fee_Numeric']
    )
    
    # Calculate average requests per year (only for years with data)
    year_columns = [2022, 2023, 2024, 2025]
    df_copy['Years_Active'] = (df_copy[year_columns] > 0).sum(axis=1)
    df_copy['Avg_Requests_Per_Year'] = df_copy.apply(
        lambda row: row['اجمالي العدد'] / row['Years_Active'] if row['Years_Active'] > 0 else 0,
        axis=1
    )
    
    # Calculate growth rate (2024 vs 2023)
    df_copy['Growth_Rate_2023_2024'] = df_copy.apply(
        lambda row: ((row[2024] - row[2023]) / row[2023] * 100) 
        if row[2023] > 0 else 0,
        axis=1
    )
    
    # Has fee indicator
    df_copy['Has_Current_Fee'] = df_copy['Current_Fee_Numeric'] > 0
    
    # Has suggested fee indicator
    df_copy['Has_Suggested_Fee'] = df_copy['ملاحظات و مقترح الرسوم'].notna()
    
    return df_copy


def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate summary statistics for the dashboard.
    
    Args:
        df (pd.DataFrame): Processed services dataframe.
        
    Returns:
        dict: Summary statistics.
    """
    summary = {
        'total_services': len(df),
        'total_requests': int(df['اجمالي العدد'].sum()),
        'services_with_fees': int(df['Has_Current_Fee'].sum()),
        'services_without_fees': int((~df['Has_Current_Fee']).sum()),
        'current_total_revenue': float(df['Current_Annual_Revenue'].sum()),
        'avg_requests_per_service': float(df['اجمالي العدد'].mean()),
        'services_with_suggestions': int(df['Has_Suggested_Fee'].sum()),
        'total_requests_2024': int(df[2024].sum()),
        'total_requests_2025': int(df[2025].sum()),
    }
    
    return summary


def prepare_dashboard_data(file_path: str = "Book1.xlsx") -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Main function to prepare all data for the dashboard.
    
    Args:
        file_path (str): Path to the Excel file.
        
    Returns:
        tuple: (processed_dataframe, summary_dict)
    """
    # Load data
    df = load_services_data(file_path)
    
    # Categorize services
    df = categorize_services(df)
    
    # Add calculated fields
    df = add_calculated_fields(df)
    
    # Generate summary
    summary = get_data_summary(df)
    
    return df, summary

