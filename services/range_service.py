from typing import List


def select_range(distance_ranges: List[dict[str, int]], distance: int) -> dict[str, int] | Exception:
    """
    Selecting the range for the delivery fee according to distance calculated

    Args:
        distance_ranges (dict): specific parameters and with each distance intervals
        distance (int): calculated distance between venue and user

    Returns:
        dr (dict): specific parameters for that selected distance range
    
    Raises:
        Exception: If any problem occurs
    """
    for dr in distance_ranges:
        if dr["max"] == 0:
            raise Exception(f"Not deliverible for your distance: {distance}")
        
        if distance < 0:
            raise Exception(f"Distance cannot be negative.")
            
        else:
            if dr["min"]<=distance<dr["max"]:
                return dr

    raise Exception(f"No matching range selected {distance}")