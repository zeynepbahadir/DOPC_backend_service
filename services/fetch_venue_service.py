import requests
from config import HOME_ASSIGNMENT_API
from http import HTTPStatus


def fetch_venue_data(venue_slug: str) -> tuple[list, tuple] | Exception:
    """
    Fetching venue data from Home Assignment Api that provides two JSON endpoints

    Args:
        venue_slug (str): type of the venue given in query parameters

    Returns:
        tuple[dict, dict]: information from static and dynamic api
    
    Raises:
        Exception: If any problem occurs
    """
    
    static_url = f"{HOME_ASSIGNMENT_API}/{venue_slug}/static"
    dynamic_url = f"{HOME_ASSIGNMENT_API}/{venue_slug}/dynamic"

    try:
        static_response = requests.get(static_url)
        dynamic_response = requests.get(dynamic_url)

        if static_response.status_code != HTTPStatus.OK:
            error_message = {
                "error": "Failed to fetch venue data",
                "static_response.status_code": static_response.status_code
            }
            raise Exception(error_message)
        
        if dynamic_response.status_code != HTTPStatus.OK:
            error_message = {
                "error": "Failed to fetch venue data",
                "dynamic_response.status_code": dynamic_response.status_code}
            raise Exception(error_message)

        #extract static venue data
        coordinates = static_response.json()["venue_raw"]["location"]["coordinates"]

        #extract dynamic venue data
        delivery_specs = dynamic_response.json()["venue_raw"]["delivery_specs"]
        order_minimum_no_surcharge = delivery_specs["order_minimum_no_surcharge"]
        base_price = delivery_specs["delivery_pricing"]["base_price"]
        distance_ranges = delivery_specs["delivery_pricing"]["distance_ranges"]

        delivery_info = order_minimum_no_surcharge, base_price, distance_ranges

        return coordinates, delivery_info
    
    except requests.exceptions.ConnectionError as ce:
        raise Exception(f"Failed to fetch venue data due to Connection Error: {ce}")
    
    except requests.exceptions.RequestException as re:
        raise Exception(f"Failed to fetch venue data due to RequestException: {re}")
    
    except ValueError as ve:
        raise Exception(f"Failure on JSON response: {ve}")
    