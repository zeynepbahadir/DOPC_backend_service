import pytest
from unittest.mock import Mock, patch
from services.fetch_venue_service import fetch_venue_data
from http import HTTPStatus

#Tests are valid for berlin venue data

@pytest.fixture
def mock_static_response():
    return { #Berlin venue data
        "venue_raw": {
            "location": {
                "coordinates": [13.4050, 52.5200]  
            }
        }
    }

@pytest.fixture
def mock_dynamic_response():
    return { #Berlin venue data
        "venue_raw": {
            "delivery_specs": {
                "order_minimum_no_surcharge": 1000,
                "delivery_pricing": {
                    "base_price": 190,
                    "distance_ranges": [
                        {"min": 0, "max": 500, "a": 0, "a": 0},
                        {"min": 500, "max": 1000, "a": 100, "a": 0},
                        {"min": 1000, "max": 1500, "a": 200, "a": 0},
                        {"min": 1500, "max": 2000, "a": 200, "a": 1},
                        {"min": 2000, "max": 0, "a": 0, "a": 0}
                    ]
                }
            }
        }
    }

def test_fetch_venue_data_success(mock_static_response, mock_dynamic_response):
    """Test successful venue data fetch with mock data"""
    with patch('services.fetch_venue_service.requests.get') as mock_get:
        mock_get.side_effect = [
            Mock(status_code=HTTPStatus.OK, json=lambda: mock_static_response),
            Mock(status_code=HTTPStatus.OK, json=lambda: mock_dynamic_response)
        ]

        static_data, dynamic_data = fetch_venue_data("home-assignment-venue-berlin")

        expected_static_response = mock_static_response["venue_raw"]["location"]["coordinates"]

        order_minimum_no_surcharge = mock_dynamic_response["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
        base_price = mock_dynamic_response["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
        distance_ranges = mock_dynamic_response["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]

        expected_dynamic_response = order_minimum_no_surcharge,base_price,distance_ranges
        
        assert static_data == expected_static_response
        assert dynamic_data == expected_dynamic_response
        assert mock_get.call_count == 2

def test_fetch_venue_data_invalid_slug():
    """Test venue data fetch with invalid slug"""
    with patch('services.fetch_venue_service.requests.get') as mock_get:
        error_response = {"error": "Venue not found"}
        mock_get.return_value = Mock(
            status_code=HTTPStatus.NOT_FOUND,
            json=lambda: error_response
        )

        with pytest.raises(Exception) as exc_info:
            fetch_venue_data("invalid-venue-slug")

        assert "Failed to fetch venue data" in str(exc_info.value)

def test_fetch_venue_data_server_error():
    """Test venue data fetch with server error"""
    with patch('services.fetch_venue_service.requests.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            json=lambda: {"error": "Internal server error"}
        )

        with pytest.raises(Exception) as exc_info:
            fetch_venue_data("home-assignment-venue-berlin")

        assert "Failed to fetch venue data" in str(exc_info.value)

def test_fetch_venue_data_invalid_response():
    """Test venue data fetch with invalid response structure"""
    with patch('services.fetch_venue_service.requests.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=HTTPStatus.OK,
            json=lambda: {"invalid": "response"}
        )

        with pytest.raises(KeyError):
            fetch_venue_data("home-assignment-venue-berlin")

def test_fetch_venue_data_connection_error():
    """Test venue data fetch with connection error"""
    with patch('services.fetch_venue_service.requests.get') as mock_get:
        mock_get.side_effect = ConnectionError("Connection failed")

        with pytest.raises(ConnectionError):
            fetch_venue_data("home-assignment-venue-berlin")

@pytest.mark.parametrize("status_code,error_message", [
    (HTTPStatus.BAD_REQUEST, "Failed to fetch venue data"),
    (HTTPStatus.UNAUTHORIZED, "Failed to fetch venue data"),
    (HTTPStatus.FORBIDDEN, "Failed to fetch venue data"),
    (HTTPStatus.NOT_FOUND, "Failed to fetch venue data"),
    (HTTPStatus.INTERNAL_SERVER_ERROR, "Failed to fetch venue data"),
])
def test_fetch_venue_data_different_status_codes(status_code, error_message):
    """Test venue data fetch with different HTTP status codes"""
    with patch('services.fetch_venue_service.requests.get') as mock_get:
        mock_get.return_value = Mock(
            status_code=status_code,
            json=lambda: {"error": error_message}
        )

        with pytest.raises(Exception) as exc_info:
            fetch_venue_data("home-assignment-venue-berlin")

        assert error_message in str(exc_info.value)
