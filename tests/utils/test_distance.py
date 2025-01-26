import pytest
from utils.distance_calculator import calculate_distance
from http import HTTPStatus
    

def test_calculate_distance():
    test_coordinates = {
        "user_lon": 45.4567,
        "user_lat": 23.4567,
        "venue_lon": 34.3456, 
        "venue_lat": 30.3456
        }

    assert calculate_distance(**test_coordinates) == 170
    
    # test for negative values
    test_coordinates["user_lon"] = -45.4567
    test_coordinates["user_lat"] = -23.4567
    assert calculate_distance(**test_coordinates) == 9263
