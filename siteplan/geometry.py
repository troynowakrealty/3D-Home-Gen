from dataclasses import dataclass
import json
from typing import List
import os

@dataclass
class Rectangle:
    name: str
    x: float
    y: float
    width: float
    height: float

@dataclass
class Point:
    x: float
    y: float


def load_layout(path: str) -> List[Rectangle]:
    if not os.path.exists(path):
        return []
    with open(path) as f:
        data = json.load(f)
    rects = []
    for item in data:
        if item.get("type") == "rectangle":
            rects.append(Rectangle(
                name=item.get("name", ""),
                x=item["x"],
                y=item["y"],
                width=item["width"],
                height=item["height"],
            ))
    return rects
