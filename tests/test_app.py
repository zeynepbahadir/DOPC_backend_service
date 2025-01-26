import pytest
from app import app
from http import HTTPStatus


@pytest.fixture
def client():
    app.testing = True
    app.debug = True
    with app.test_client() as client:
        yield client

class Test_response_success:
    qs = {
        "venue_slug": "home-assignment-venue-berlin",
        "cart_value": 2000,
        "user_lat": 41.9028,
        "user_lon": 12.4964 
    }

    def test_response_status_code(self, client):
        """
        Test for succesfull response status code
        """
        response = client.get("/api/v1/delivery-order-price", query_string=self.qs)
        assert response.status_code == HTTPStatus.OK

    def test_response_json(self, client):
        """
        Test for succesfull response json
        """
        response = client.get("/api/v1/delivery-order-price", query_string=self.qs)
        assert response.json == {
            "total_price": 2190,
            "small_order_surcharge": 0,
            "cart_value": 2000,
            "delivery": {
                "fee": 190,
                "distance": 113
            }
        }

class Test_missing_query:
    def test_response_status_code(self, client):
        """
        Test for missing query response status code
        """
        response = client.get("/api/v1/delivery-order-price")
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_response_json(self, client):
        """
        Test for missing query response json
        """
        response = client.get("/api/v1/delivery-order-price")
        assert response.json == {"error": "Missing query parameters."}

class Test_distance_ranges:
    qs = {
        "venue_slug": "home-assignment-venue-berlin",
        "cart_value": 2000,
        "user_lat": 41.9028,
        "user_lon": 12.4964 
    }

    def test_distance_range_0(self, client, mocker):
        """
        Test for distance range 0 delivery fee calculations
        """
        calculate_distance = mocker.patch("app.calculate_distance", return_value=440)
        response = client.get("/api/v1/delivery-order-price", query_string=self.qs)
        assert response.json == {
            "total_price": 2190,
            "small_order_surcharge": 0,
            "cart_value": 2000,
            "delivery": {
                "fee": 190,
                "distance": 440
            }
        }

    def test_distance_range_1(self, client, mocker):
        """
        Test for distance range 1 delivery fee calculations
        """
        calculate_distance = mocker.patch("app.calculate_distance", return_value=550)
        response = client.get("/api/v1/delivery-order-price", query_string=self.qs)
        assert response.json == {
            "total_price": 2290,
            "small_order_surcharge": 0,
            "cart_value": 2000,
            "delivery": {
                "fee": 290,
                "distance": 550
            }
        }

    def test_distance_range_2(self, client, mocker):
        """
        Test for distance range 2 delivery fee calculations
        """
        calculate_distance = mocker.patch("app.calculate_distance", return_value=1200)
        response = client.get("/api/v1/delivery-order-price", query_string=self.qs)
        assert response.json == {
            "total_price": 2390,
            "small_order_surcharge": 0,
            "cart_value": 2000,
            "delivery": {
                "fee": 390,
                "distance": 1200
            }
        }

    def test_distance_range_3(self, client, mocker):
        """
        Test for distance range 3 delivery fee calculations
        """
        calculate_distance = mocker.patch("app.calculate_distance", return_value=1750)
        response = client.get("/api/v1/delivery-order-price", query_string=self.qs)
        assert response.json == {
            "total_price": 2565,
            "small_order_surcharge": 0,
            "cart_value": 2000,
            "delivery": {
                "fee": 565,
                "distance": 1750
            }
        }

    def test_distance_range_4(self, client, mocker):
        """
        Test for distance range 4 delivery fee calculations
        """
        calculate_distance = mocker.patch("app.calculate_distance", return_value=2300)
        response = client.get("/api/v1/delivery-order-price", query_string=self.qs)
        assert response.json == {"Error": "Not deliverible for your distance: 2300"}

class Test_small_order_surcharge:
    def test_small_order_surcharge_charged(self, client):
        qs = {
            "venue_slug": "home-assignment-venue-berlin",
            "cart_value": 990,
            "user_lat": 41.9028,
            "user_lon": 12.4964 
        }
        response = client.get("/api/v1/delivery-order-price", query_string=qs)
        assert response.json == {
            "total_price": 1190,
            "small_order_surcharge": 10,
            "cart_value": 990,
            "delivery": {
                "fee": 190,
                "distance": 113
            }
        }

    def test_small_order_surcharge_no_charge_equal(self, client):
        qs = {
            "venue_slug": "home-assignment-venue-berlin",
            "cart_value": 1000,
            "user_lat": 41.9028,
            "user_lon": 12.4964 
        }
        response = client.get("/api/v1/delivery-order-price", query_string=qs)
        assert response.json == {
            "total_price": 1190,
            "small_order_surcharge": 0,
            "cart_value": 1000,
            "delivery": {
                "fee": 190,
                "distance": 113
            }
        }

    def test_small_order_surcharge_no_charge_more(self, client):
        qs = {
            "venue_slug": "home-assignment-venue-berlin",
            "cart_value": 1900,
            "user_lat": 41.9028,
            "user_lon": 12.4964 
        }
        response = client.get("/api/v1/delivery-order-price", query_string=qs)
        assert response.json == {
            "total_price": 2090,
            "small_order_surcharge": 0,
            "cart_value": 1900,
            "delivery": {
                "fee": 190,
                "distance": 113
            }
        }

class Test_distance:
    qs = {
        "venue_slug": "home-assignment-venue-berlin",
        "cart_value": 2000,
        "user_lat": 41.9028,
        "user_lon": 12.4964 
    }

    def test_distance_negative(self, client, mocker):
        calculate_distance = mocker.patch("app.calculate_distance", return_value=-100)
        response = client.get("/api/v1/delivery-order-price", query_string=self.qs)
        assert response.json == {"Error": "Distance cannot be negative."}