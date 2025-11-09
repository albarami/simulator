"""
Tests for suggestions analytics functions in utils/analytics.py.
"""
import pytest
import pandas as pd
import numpy as np
from utils.analytics import (
    analyze_suggested_fees,
    identify_quick_wins,
    calculate_suggestion_implementation_impact,
    compare_current_vs_suggested
)


@pytest.fixture
def sample_df():
    """Create sample dataframe for testing."""
    data = {
        'اسم الخدمة': [
            'Service 1', 'Service 2', 'Service 3', 'Service 4', 'Service 5'
        ],
        'Category': ['Category A', 'Category B', 'Category A', 'Category C', 'Category B'],
        'اجمالي العدد': [50000, 30000, 15000, 10000, 5000],
        'Current_Fee_Numeric': [0, 10, 0, 20, 0],
        'Current_Annual_Revenue': [0, 300000, 0, 200000, 0],
        'Suggested_Fee_Numeric': [100, 50, 20, 0, 10],
        'Suggested_Fee_Secondary': [0, 0, 0, 0, 0],
        'Fee_Structure_Type': ['per_person', 'flat', 'per_month', 'none', 'conditional'],
        'Fee_Suggestion_Confidence': [0.9, 0.85, 0.75, 0.0, 0.8],
        'Fee_Conditions': ['', '', '', '', 'private_company_only'],
        'Suggested_Revenue_Potential': [5000000, 1500000, 300000, 0, 50000],
        'Revenue_Gap': [5000000, 1200000, 300000, 0, 50000],
        'Has_Historical_Change': [False, True, False, False, False],
        'Special_Conditions': ['', '', '', '', 'For private companies']
    }
    
    return pd.DataFrame(data)


class TestAnalyzeSuggestedFees:
    """Test analyze_suggested_fees function."""
    
    def test_basic_analysis(self, sample_df):
        """Test basic suggestions analysis."""
        result = analyze_suggested_fees(sample_df)
        
        assert result['total_services_with_suggestions'] == 4
        assert result['total_revenue_gap'] == 6550000
        assert result['quick_wins_count'] == 3  # Services with no fee but with suggestions
        assert result['high_confidence_count'] >= 2
    
    def test_empty_dataframe(self):
        """Test with empty dataframe."""
        empty_df = pd.DataFrame({
            'Suggested_Fee_Numeric': [],
            'Current_Fee_Numeric': [],
            'Revenue_Gap': [],
            'Suggested_Revenue_Potential': [],
            'Current_Annual_Revenue': [],
            'Fee_Structure_Type': [],
            'Fee_Suggestion_Confidence': [],
            'اسم الخدمة': [],
            'اجمالي العدد': []
        })
        
        result = analyze_suggested_fees(empty_df)
        
        assert result['total_services_with_suggestions'] == 0
        assert result['total_revenue_gap'] == 0


class TestIdentifyQuickWins:
    """Test identify_quick_wins function."""
    
    def test_identify_quick_wins(self, sample_df):
        """Test identifying quick wins."""
        result = identify_quick_wins(sample_df, min_requests=10000, top_n=10)
        
        assert len(result) >= 2  # At least 2 services meet criteria
        assert result.iloc[0]['Revenue_Gap'] >= result.iloc[-1]['Revenue_Gap']  # Sorted by revenue gap
    
    def test_high_threshold(self, sample_df):
        """Test with very high volume threshold."""
        result = identify_quick_wins(sample_df, min_requests=100000, top_n=10)
        
        assert len(result) == 0  # No services meet the high threshold
    
    def test_top_n_limit(self, sample_df):
        """Test top_n parameter limits results."""
        result = identify_quick_wins(sample_df, min_requests=1000, top_n=2)
        
        assert len(result) <= 2


class TestCalculateSuggestionImplementationImpact:
    """Test calculate_suggestion_implementation_impact function."""
    
    def test_single_service_implementation(self, sample_df):
        """Test implementation impact for single service."""
        services = ['Service 1']
        result = calculate_suggestion_implementation_impact(sample_df, services)
        
        assert result['total_services'] == 1
        assert result['total_revenue_increase'] == 5000000
        assert result['percent_increase'] > 0
    
    def test_multiple_services_implementation(self, sample_df):
        """Test implementation impact for multiple services."""
        services = ['Service 1', 'Service 3']
        result = calculate_suggestion_implementation_impact(sample_df, services)
        
        assert result['total_services'] == 2
        assert result['total_revenue_increase'] == 5300000  # 5M + 300K
    
    def test_no_services(self, sample_df):
        """Test with no services selected."""
        result = calculate_suggestion_implementation_impact(sample_df, [])
        
        assert result['total_services'] == 0
        assert result['total_revenue_increase'] == 0


class TestCompareCurrentVsSuggested:
    """Test compare_current_vs_suggested function."""
    
    def test_comparison(self, sample_df):
        """Test current vs suggested comparison."""
        result = compare_current_vs_suggested(sample_df)
        
        assert len(result) == 4  # 4 services have suggestions
        assert 'Fee_Change_Pct' in result.columns
        assert 'Revenue_Change_Pct' in result.columns
    
    def test_sorted_by_revenue_gap(self, sample_df):
        """Test results are sorted by revenue gap."""
        result = compare_current_vs_suggested(sample_df)
        
        # Should be sorted descending by Revenue_Gap
        for i in range(len(result) - 1):
            assert result.iloc[i]['Revenue_Gap'] >= result.iloc[i+1]['Revenue_Gap']


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

