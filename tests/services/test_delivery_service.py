import pytest
from services.delivery_service import calculate_delivery
from http import HTTPStatus

#Tests are valid for berlin venue data

base_price = 190 #Berlin venue data
order_minimum_no_surcharge = 1000 #Berlin venue data

class Test_delivery_fee:
    """Test suite for delivery_fee"""
    @pytest.mark.parametrize("distance, selected_range, expected_fee", [
        (499, {"min": 0, "max": 500, "a":0, "b":0}, 190), #first range
        (1500, {"min": 500, "max": 1000, "a":100, "b":0}, 290), #second range
        (1250, {"min": 1000, "max": 1500, "a":200, "b":0}, 390), #third range
        (1850, {"min": 1500, "max": 2000, "a":200, "b":1}, 575), #fourth range
        (2350, {"min": 2000, "max": 0, "a":0, "b":0}, 190) #invalid range
        ])
    def test_calculate_delivery_fee_various_scenarios(self, distance, selected_range, expected_fee):
        """Test various scenarios for delivery fee calculation"""
        cart_value = 950 
        delivery_fee, surcharge, total = calculate_delivery(
            base_price, selected_range, order_minimum_no_surcharge, distance, cart_value
        )
        assert delivery_fee == expected_fee

    def test_calculate_delivery_fee_float_values(self):
        """Test delivery fee calculation with float values"""
        cart_value = 1500.5
        distance = 300.7
        selected_range = {"min": 0, "max": 500, "a":0, "b":0}
        delivery_fee, surcharge, total = calculate_delivery(
            base_price, selected_range, order_minimum_no_surcharge, distance, cart_value
        )
        assert delivery_fee == 190
    
class Test_surcharge:
    """Test suite for small_order_surcharge"""
    selected_range = {"min": 0, "max": 500, "a":0, "b":0} #berlin
    distance = 300

    @pytest.mark.parametrize("cart_value, expected_surcharge", [
        (0, 1000), #full surcharge
        (500, 500), #with surcharge
        (1000, 0), #boundry value
        (1500, 0) #without surcharge
    ])
    def test_calculate_surcharge(self, cart_value, expected_surcharge):
        """Test surcharge calculation"""
        delivery_fee, surcharge, total = calculate_delivery(
            base_price, self.selected_range, order_minimum_no_surcharge, self.distance, cart_value
        )
        assert surcharge == expected_surcharge
    
    def test_calculate_surcharge_float_values(self):
        """Test surcharge calculation with float values"""
        cart_value = 956.32

        delivery_fee, surcharge, total = calculate_delivery(
            base_price, self.selected_range, order_minimum_no_surcharge, self.distance, cart_value
        )
        assert surcharge == 44 ##43.68 rounded to 44


class Test_total:
    """Test suite for total_price"""
    distance = 450
    selected_range = {"min": 0, "max": 500, "a":0, "b":0}

    @pytest.mark.parametrize("cart_value, expected_total", [
        (0, 1190), #cart_value zero
        (-500, 1190), #considered as cart_value is zero 
        (950.85, 1190) #cart_value float, expected_total is rounded to upper value
    ])
    def test_cart_value_zero(self, cart_value, expected_total):
        """Test for total price with cart_value zero"""
        delivery_fee, surcharge, total = calculate_delivery(
            base_price, self.selected_range, order_minimum_no_surcharge, self.distance, cart_value
        )
        assert total == expected_total
