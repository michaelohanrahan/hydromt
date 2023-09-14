"""Utility functions for hydromt that have no other home."""
import os
import numpy as np


class _classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def partition_dictionaries(left, right):
    """Calculate a partitioning of the two dictionaries.

    given dictionaries A and B this function will the follwing partition:
    (A ∩ B, A - B, B - A)
    """
    common = {}
    left_less_right = {}
    right_less_left = {}
    key_union = set(left.keys()) | set(right.keys())

    for key in key_union:
        value_left = left.get(key, None)
        value_right = right.get(key, None)
        if isinstance(value_left, dict) and isinstance(value_right, dict):
            (
                common_children,
                unique_left_children,
                unique_right_children,
            ) = partition_dictionaries(value_left, value_right)
            common[key] = common_children
            if unique_left_children != unique_right_children:
                left_less_right[key] = unique_left_children
                right_less_left[key] = unique_right_children
        elif value_left == value_right:
            common[key] = value_left
        else:
            if value_left is not None:
                left_less_right[key] = value_left
            if value_right is not None:
                right_less_left[key] = value_right

    return common, left_less_right, right_less_left


def create_folder(path):
    """Create a folder if there is none."""
    if not os.path.exists(path):
        os.makedirs(path)


def elevation2rgb(val):
    """Convert elevation to rgb tuple"""
    val += 32768
    r = np.floor(val / 256).astype(np.uint8)
    g = np.floor(val % 256).astype(np.uint8)
    b = np.floor((val - np.floor(val)) * 256).astype(np.uint8)

    return (r, g, b)


def rgb2elevation(r, g, b):
    """Convert rgb tuple to elevation"""
    val = (r * 256 + g + b / 256) - 32768
    return val


def _dict_pprint(d):
    import json

    return json.dumps(d, indent=2)
