from enum import Enum
import os
from typing import (
    Final,
    List,
)

DB_PATH = "db.db" 

# # Open API parameters
OPEN_API_TITLE: Final = "what"
OPEN_API_DESCRIPTION: Final = "what2"
POSSIBLE_GRID_TYPES: Final = ["nationality", "team", "league", "title", "manager", "player"]
