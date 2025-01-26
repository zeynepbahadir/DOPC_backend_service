import os
from flask import Flask, request, jsonify
from services.fetch_venue_service import fetch_venue_data
from services.delivery_service import calculate_delivery
from services.range_service import select_range
from utils.distance_calculator import calculate_distance
from config import FLASK_HOST, FLASK_PORT
from http import HTTPStatus


app = Flask(__name__)

# TODO: add a dockerfile and docker-compose.yml file to run the app with docker.
# TODO: Input Validation: like validating numeric inputs for negative values, string inputs for empty values, etc. 

@app.route("/api/v1/delivery-order-price", methods=["GET"])
def delivery_order_price_calculator():
    """
    Delivery Order Price Calculator (DOPC) Service for calculating the total price and price breakdown of a delivery order.

    Returns:
        total_price (int): The calculated total price
        small_order_surcharge (int): The calculated small order surcharge
        cart_value (int): The cart value. This is the same as what was got as query parameter.
        delivery (dict): An object containing:
            fee (int): The calculated delivery fee
            distance (int): The calculated delivery distance in meters
    """

    try:
        #getting query parameters
        venue_slug = request.args.get("venue_slug", type=str)
        cart_value = request.args.get("cart_value", type=int)
        user_lat = request.args.get("user_lat", type=float)
        user_lon = request.args.get("user_lon", type=float)
        
        #validation query parameters
        if not all([venue_slug, cart_value, user_lat, user_lon]):
            return jsonify({"error": "Missing query parameters."}), HTTPStatus.BAD_REQUEST

        #fetching venue data
        try:
            coordinates, delivery_info = fetch_venue_data(venue_slug)
        except Exception as e:
            return jsonify({"Error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
        
        venue_lon, venue_lat = coordinates
        order_minimum_no_surcharge, base_price, distance_ranges = delivery_info
        
        distance = calculate_distance(user_lat, user_lon, venue_lat, venue_lon)

        #select range according to distance
        try:
            selected_range = select_range(distance_ranges, distance)
        except Exception as e:
            return jsonify({"Error": str(e)}), HTTPStatus.BAD_REQUEST

        #calculate delivery charges
        delivery_fee, small_order_surcharge, total_price = calculate_delivery(base_price, selected_range, order_minimum_no_surcharge, distance, cart_value)
        
        return jsonify({"total_price": total_price,
                        "small_order_surcharge": small_order_surcharge,
                        "cart_value": cart_value,
                        "delivery":{
                            "fee": delivery_fee,
                            "distance": distance
                        }
                    }), HTTPStatus.OK

    except ValueError as ve:
        return jsonify({"error": str(ve)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        return jsonify({"error": "Internal server error"}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", FLASK_HOST)
    port = int(os.getenv("FLASK_PORT", FLASK_PORT))
    app.run(host=host, port=port, debug=True)
