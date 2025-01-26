def calculate_distance(user_lat: float, user_lon: float, venue_lat: float, venue_lon: float) -> int:
    """
    Calculating distance between venue and user based on Pythagoras theorem

    Args:
        user_lat (float): The latitude of the user's location
        user_lon (float): The longitude of the user's location
        venue_lat (float): The latitude of the venue
        venue_lon (float): The longtitute of the venue

    Returns:
        (int): Calculation of distance
    """

    return int(pow((user_lat-venue_lat), 2) + pow((user_lon-venue_lon),2))