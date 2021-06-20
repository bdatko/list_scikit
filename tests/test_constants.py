from list_scikit import MY_LIST_DICT
import pandas as pd


def test_diff_plus_intersection():
    # Arrange
    libraries = pd.read_csv("data/libraries.csv")
    libraries = set(libraries["library"].to_list())
    my_list_set = set(MY_LIST_DICT)
    # Act
    difference = len(my_list_set - libraries)
    intersection = len(libraries.intersection(my_list_set))
    # Assert
    assert len(MY_LIST_DICT) == (difference + intersection)
