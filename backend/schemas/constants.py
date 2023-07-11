from enum import Enum


class CardTypes(Enum):
    COMMUNITY_CHEST = "community_chest"
    CHANCE = "chance"


class GameSpaceTypes(Enum):
    DRAW_CHEST = "draw-chest"
    DRAW_CHANCE = "draw-chance"
    FREE = "free"
    GO_TO_JAIL = "go-to-jail"
    JAIL = "jail"
    PROPERTY = "property"
    RAILROAD = "railroad"
    TAX = "tax"
    TAX_INCOME = "tax-income"


class PropertyGroup(Enum):
    BLUE = "blue"
    GREEN = "green"
    LIGHT_BLUE = "light-blue"
    ORANGE = "orange"
    RAILROAD = "railroad"
    RED = "red"
    PURPLE = "purple"
    VIOLET = "violet"
    YELLOW = "yellow"


class PropertyStatus(Enum):
    OWNED = "owned"
    VACANT = "vacant"


class RollResultCodes(Enum):
    THIRD_DOUBLE = 98
    JAIL_DOUBLE = 99
