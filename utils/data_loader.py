"""
Data loading and preprocessing module for Ministry of Labour services data.
"""
import pandas as pd
import numpy as np
import re
from typing import Tuple, Dict, Any, Optional


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


def parse_suggested_fee(notes_text: str) -> Dict[str, Any]:
    """
    Extract suggested fee information from Arabic text in notes column.
    
    Args:
        notes_text (str): Text from the notes/suggestions column.
        
    Returns:
        dict: Parsed fee information with keys:
            - base_fee (float): Primary fee amount
            - unit_type (str): Type of fee (flat, per_person, per_month, per_modification, tiered, conditional)
            - secondary_fee (float): Secondary fee for tiered pricing
            - conditions (str): Special conditions
            - confidence (float): Parsing confidence score (0-1)
            - raw_text (str): Original text
    """
    if pd.isna(notes_text) or not str(notes_text).strip():
        return {
            'base_fee': 0.0,
            'unit_type': 'none',
            'secondary_fee': 0.0,
            'conditions': '',
            'confidence': 0.0,
            'raw_text': ''
        }
    
    text = str(notes_text).strip()
    result = {
        'base_fee': 0.0,
        'unit_type': 'flat',
        'secondary_fee': 0.0,
        'conditions': '',
        'confidence': 0.0,
        'raw_text': text
    }
    
    # Arabic number words mapping
    arabic_numbers = {
        'واحد': 1, 'اثنين': 2, 'اثنان': 2, 'ثلاثة': 3, 'ثلاث': 3,
        'أربعة': 4, 'أربع': 4, 'خمسة': 5, 'خمس': 5,
        'ستة': 6, 'سبعة': 7, 'ثمانية': 8, 'تسعة': 9,
        'عشرة': 10, 'عشر': 10, 'عشرون': 20, 'ثلاثون': 30,
        'أربعون': 40, 'خمسون': 50, 'ستون': 60, 'سبعون': 70,
        'ثمانون': 80, 'تسعون': 90, 'مئة': 100, 'مائة': 100,
        'ألف': 1000, 'الف': 1000
    }
    
    # Replace Arabic number words with digits
    text_normalized = text
    for word, num in arabic_numbers.items():
        text_normalized = text_normalized.replace(word, str(num))
    
    # Extract all numbers from text
    numbers = re.findall(r'\d+', text_normalized)
    numbers = [int(n) for n in numbers]
    
    # Determine fee structure type and extract fees
    if 'لكل شخص' in text or 'عن كل شخص' in text:
        result['unit_type'] = 'per_person'
        result['confidence'] = 0.9
        if numbers:
            result['base_fee'] = float(numbers[0])
    
    elif 'لكل شهر' in text or 'عن كل شهر' in text:
        result['unit_type'] = 'per_month'
        result['confidence'] = 0.9
        if numbers:
            result['base_fee'] = float(numbers[0])
    
    elif 'لكل تعديل' in text or 'عن كل تعديل' in text:
        result['unit_type'] = 'per_modification'
        result['confidence'] = 0.9
        if numbers:
            result['base_fee'] = float(numbers[0])
    
    elif 'لكل مهنة' in text:
        result['unit_type'] = 'tiered'
        result['confidence'] = 0.85
        # Extract two fees for specialized vs non-specialized
        if len(numbers) >= 2:
            result['base_fee'] = float(numbers[0])  # Specialized
            result['secondary_fee'] = float(numbers[1])  # Non-specialized
        elif len(numbers) == 1:
            result['base_fee'] = float(numbers[0])
    
    elif 'في حال' in text or 'حال' in text:
        result['unit_type'] = 'conditional'
        result['confidence'] = 0.8
        if numbers:
            result['base_fee'] = float(numbers[0])
        
        # Extract condition
        if 'شركة خاصة' in text:
            result['conditions'] = 'private_company_only'
        elif 'فصل تأديبي' in text or 'التأديبي' in text:
            result['conditions'] = 'disciplinary_termination'
        elif 'حكومية' in text:
            result['conditions'] = 'government_entities'
    
    else:
        # Default flat fee
        result['unit_type'] = 'flat'
        if numbers:
            result['base_fee'] = float(numbers[0])
            result['confidence'] = 0.7
        else:
            result['confidence'] = 0.0
    
    # Validate reasonable fee range (0-10000 QAR)
    if result['base_fee'] > 10000:
        result['confidence'] *= 0.5
    
    return result


def extract_historical_fee_changes(notes_text: str) -> Dict[str, Any]:
    """
    Parse historical fee change information from notes.
    
    Args:
        notes_text (str): Text from the notes column.
        
    Returns:
        dict: Historical fee change info with keys:
            - has_change (bool): Whether a fee change was found
            - original_fee (float): Original fee amount
            - new_fee (float): New fee amount after change
            - change_date (str): Date/period of change if mentioned
            - change_description (str): Description of change
    """
    if pd.isna(notes_text) or not str(notes_text).strip():
        return {
            'has_change': False,
            'original_fee': 0.0,
            'new_fee': 0.0,
            'change_date': '',
            'change_description': ''
        }
    
    text = str(notes_text).strip()
    result = {
        'has_change': False,
        'original_fee': 0.0,
        'new_fee': 0.0,
        'change_date': '',
        'change_description': text
    }
    
    # Look for historical change patterns
    if 'كانت' in text and 'تم تعديل' in text:
        result['has_change'] = True
        
        # Extract numbers
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2:
            result['original_fee'] = float(numbers[0])
            result['new_fee'] = float(numbers[1])
        
        # Extract date if mentioned
        if 'شهر' in text:
            month_match = re.search(r'شهر\s*(\d+)', text)
            if month_match:
                result['change_date'] = f"Month {month_match.group(1)}"
    
    elif 'تم الغاء' in text or 'الغاء' in text:
        result['has_change'] = True
        result['change_description'] = 'Fee cancelled'
        # Extract original fee if mentioned
        numbers = re.findall(r'\d+', text)
        if numbers:
            result['original_fee'] = float(numbers[0])
            result['new_fee'] = 0.0
    
    return result


def categorize_fee_structure(parsed_fee: Dict[str, Any]) -> str:
    """
    Categorize fee structure type from parsed fee data.
    
    Args:
        parsed_fee (dict): Parsed fee information from parse_suggested_fee.
        
    Returns:
        str: Fee structure category.
    """
    return parsed_fee.get('unit_type', 'flat')


def identify_special_conditions(notes_text: str) -> str:
    """
    Extract special conditions from notes text.
    
    Args:
        notes_text (str): Text from notes column.
        
    Returns:
        str: Description of special conditions.
    """
    if pd.isna(notes_text) or not str(notes_text).strip():
        return ''
    
    text = str(notes_text).strip()
    conditions = []
    
    if 'حكومية' in text or 'شبه حكومية' in text:
        conditions.append('For government/semi-government entities')
    
    if 'شركة خاصة' in text:
        conditions.append('For private companies')
    
    if 'فصل تأديبي' in text or 'التأديبي' in text:
        conditions.append('For disciplinary termination')
    
    if 'مهنة تخصصية' in text:
        conditions.append('Different rates for specialized vs non-specialized professions')
    
    if 'يوجد رسوم تحصل من' in text:
        if 'الداخلية' in text:
            conditions.append('Fees collected by Internal Affairs Ministry')
    
    return '; '.join(conditions) if conditions else ''


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
    
    # Parse suggested fees from notes column
    notes_column = 'ملاحظات و مقترح الرسوم'
    if notes_column in df_copy.columns:
        parsed_fees = df_copy[notes_column].apply(parse_suggested_fee)
        
        df_copy['Suggested_Fee_Numeric'] = parsed_fees.apply(lambda x: x['base_fee'])
        df_copy['Suggested_Fee_Secondary'] = parsed_fees.apply(lambda x: x['secondary_fee'])
        df_copy['Fee_Structure_Type'] = parsed_fees.apply(lambda x: x['unit_type'])
        df_copy['Fee_Suggestion_Confidence'] = parsed_fees.apply(lambda x: x['confidence'])
        df_copy['Fee_Conditions'] = parsed_fees.apply(lambda x: x['conditions'])
        
        # Calculate suggested revenue potential (use base fee for estimates)
        df_copy['Suggested_Revenue_Potential'] = (
            df_copy['اجمالي العدد'] * df_copy['Suggested_Fee_Numeric']
        )
        
        # Calculate revenue gap (potential gain from implementing suggestion)
        df_copy['Revenue_Gap'] = (
            df_copy['Suggested_Revenue_Potential'] - df_copy['Current_Annual_Revenue']
        )
        
        # Parse historical fee changes
        historical_changes = df_copy[notes_column].apply(extract_historical_fee_changes)
        df_copy['Has_Historical_Change'] = historical_changes.apply(lambda x: x['has_change'])
        df_copy['Historical_Original_Fee'] = historical_changes.apply(lambda x: x['original_fee'])
        df_copy['Historical_New_Fee'] = historical_changes.apply(lambda x: x['new_fee'])
        df_copy['Historical_Change_Date'] = historical_changes.apply(lambda x: x['change_date'])
        
        # Extract special conditions
        df_copy['Special_Conditions'] = df_copy[notes_column].apply(identify_special_conditions)
    else:
        # Add empty columns if notes column doesn't exist
        df_copy['Suggested_Fee_Numeric'] = 0.0
        df_copy['Suggested_Fee_Secondary'] = 0.0
        df_copy['Fee_Structure_Type'] = 'none'
        df_copy['Fee_Suggestion_Confidence'] = 0.0
        df_copy['Fee_Conditions'] = ''
        df_copy['Suggested_Revenue_Potential'] = 0.0
        df_copy['Revenue_Gap'] = 0.0
        df_copy['Has_Historical_Change'] = False
        df_copy['Historical_Original_Fee'] = 0.0
        df_copy['Historical_New_Fee'] = 0.0
        df_copy['Historical_Change_Date'] = ''
        df_copy['Special_Conditions'] = ''
    
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

