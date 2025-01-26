import pytest
from unittest.mock import Mock, patch
from services.range_service import select_range
from http import HTTPStatus

#Tests are valid for berlin venue data

@pytest.fixture
def distance_ranges():
    return [ #Berlin venue data
        {"min": 0, "max": 500, "a": 0, "a": 0},
        {"min": 500, "max": 1000, "a": 100, "a": 0},
        {"min": 1000, "max": 1500, "a": 200, "a": 0},
        {"min": 1500, "max": 2000, "a": 200, "a": 1},
        {"min": 2000, "max": 0, "a": 0, "a": 0}
    ]

class Test_RangeService:
    """Test suite for range service"""

    def test_select_range_range_0(self, distance_ranges):
        """Test selecting first distance range"""
        distance = 300
        result = select_range(distance_ranges, distance)
        assert result == {"min": 0, "max": 500, "a": 0, "a": 0}

    def test_select_range_range_1(self, distance_ranges):
        """Test selecting second distance range"""
        distance = 750
        result = select_range(distance_ranges, distance)
        assert result == {"min": 500, "max": 1000, "a": 100, "a": 0}

    def test_select_range_range_2(self, distance_ranges):
        """Test selecting third valid distance range"""
        distance = 1350
        result = select_range(distance_ranges, distance)
        assert result == {"min": 1000, "max": 1500, "a": 200, "a": 0}

    def test_select_range_range_3(self, distance_ranges):
        """Test selecting last valid distance range"""
        distance = 1875
        result = select_range(distance_ranges, distance)
        assert result == {"min": 1500, "max": 2000, "a": 200, "a": 1}

    def test_select_range_range_4(self, distance_ranges):
        """Test selecting range invalid range"""
        distance = 2200

        with pytest.raises(Exception) as exc_info:
            select_range(distance_ranges, distance)

        assert "Not deliverible for your distance" in str(exc_info.value)
