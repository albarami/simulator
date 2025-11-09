"""
Tests for data parsing functions in utils/data_loader.py.
"""
import pytest
import pandas as pd
from utils.data_loader import (
    parse_suggested_fee,
    extract_historical_fee_changes,
    identify_special_conditions
)


class TestParseSuggestedFee:
    """Test parse_suggested_fee function."""
    
    def test_parse_per_person_fee(self):
        """Test parsing per-person fee suggestions."""
        text = "عشرة ريال عن كل شخص"
        result = parse_suggested_fee(text)
        
        assert result['base_fee'] == 10.0
        assert result['unit_type'] == 'per_person'
        assert result['confidence'] > 0.8
    
    def test_parse_per_month_fee(self):
        """Test parsing per-month fee suggestions."""
        text = "مئة ريال عن كل شهر"
        result = parse_suggested_fee(text)
        
        assert result['base_fee'] == 100.0
        assert result['unit_type'] == 'per_month'
        assert result['confidence'] > 0.8
    
    def test_parse_tiered_fee(self):
        """Test parsing tiered fee suggestions."""
        text = "خمسة ريال لكل مهنة تخصصية , اثنين ريال لكل مهنة غير تخصصية"
        result = parse_suggested_fee(text)
        
        assert result['base_fee'] == 5.0
        assert result['secondary_fee'] == 2.0
        assert result['unit_type'] == 'tiered'
        assert result['confidence'] > 0.8
    
    def test_parse_conditional_fee(self):
        """Test parsing conditional fee suggestions."""
        text = "مئة ريال في حال الجهة الجديدة شركة خاصة"
        result = parse_suggested_fee(text)
        
        assert result['base_fee'] == 100.0
        assert result['unit_type'] == 'conditional'
        assert result['conditions'] == 'private_company_only'
    
    def test_parse_flat_fee(self):
        """Test parsing simple flat fee."""
        text = "ستون ريال في حال الفصل التأديبي"
        result = parse_suggested_fee(text)
        
        assert result['base_fee'] == 60.0
        assert 'conditional' in result['unit_type']
    
    def test_parse_empty_text(self):
        """Test parsing empty or None text."""
        result = parse_suggested_fee(None)
        
        assert result['base_fee'] == 0.0
        assert result['unit_type'] == 'none'
        assert result['confidence'] == 0.0
    
    def test_parse_numeric_only(self):
        """Test parsing text with only numbers."""
        text = "100"
        result = parse_suggested_fee(text)
        
        assert result['base_fee'] == 100.0
        assert result['unit_type'] == 'flat'


class TestExtractHistoricalFeeChanges:
    """Test extract_historical_fee_changes function."""
    
    def test_extract_fee_change(self):
        """Test extracting historical fee change."""
        text = "كانت 500 و تم تعديل القيمة الى 100 ببداية شهر 9"
        result = extract_historical_fee_changes(text)
        
        assert result['has_change'] == True
        assert result['original_fee'] == 500.0
        assert result['new_fee'] == 100.0
        assert 'Month 9' in result['change_date']
    
    def test_extract_fee_cancellation(self):
        """Test extracting fee cancellation."""
        text = "تم الغاء الرسوم"
        result = extract_historical_fee_changes(text)
        
        assert result['has_change'] == True
        assert 'cancel' in result['change_description'].lower()
    
    def test_no_historical_change(self):
        """Test text with no historical change."""
        text = "خدمة جديدة بدون رسوم"
        result = extract_historical_fee_changes(text)
        
        assert result['has_change'] == False


class TestIdentifySpecialConditions:
    """Test identify_special_conditions function."""
    
    def test_government_entities(self):
        """Test identifying government entity condition."""
        text = "الخدمة لجهات حكومية و شبه حكومية"
        result = identify_special_conditions(text)
        
        assert 'government' in result.lower()
    
    def test_private_companies(self):
        """Test identifying private company condition."""
        text = "مئة ريال في حال الجهة الجديدة شركة خاصة"
        result = identify_special_conditions(text)
        
        assert 'private' in result.lower()
    
    def test_specialized_professions(self):
        """Test identifying specialized profession rates."""
        text = "خمسة ريال لكل مهنة تخصصية"
        result = identify_special_conditions(text)
        
        assert 'specialized' in result.lower() or 'profession' in result.lower()
    
    def test_no_conditions(self):
        """Test text with no special conditions."""
        text = "عشرة ريال فقط"
        result = identify_special_conditions(text)
        
        assert result == ''


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

