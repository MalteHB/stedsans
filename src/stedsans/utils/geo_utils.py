"""Geography utilities
"""


def calc_bbox(coordinates, edge=0.15):
    """ Calculates bounding box with frame by finidng pair of max and min coordinates
    and adding/subtracting edge degrees as the frame

    Args:
        coordinates (list): list of coordinates
        edge (float, optional): Amount to expand/diminish the bounding box by. Defaults to 0.15.

    Returns:
        bbox (list): A bounding box for the given coordinates
    """
    # Create bounding box with frame by finidng pair of max and min coordinates and adding/subtracting edge degrees as the frame
    bbox = [[max([item[0] for item in coordinates]) + edge, max([item[1] for item in coordinates]) + edge],
            [min([item[0] for item in coordinates]) - edge, min([item[1] for item in coordinates]) - edge]]

    return bbox
