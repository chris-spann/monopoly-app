from enum import Enum, IntEnum


class CardTypes(str, Enum):
    COMMUNITY_CHEST = "community_chest"
    CHANCE = "chance"


class GameSpaceTypes(str, Enum):
    DRAW_CHEST = "draw-chest"
    DRAW_CHANCE = "draw-chance"
    FREE = "free"
    GO_TO_JAIL = "go-to-jail"
    JAIL = "jail"
    PROPERTY = "property"
    RAILROAD = "railroad"
    TAX = "tax"
    TAX_INCOME = "tax-income"


class PropertyGroup(str, Enum):
    BLUE = "blue"
    GREEN = "green"
    LIGHT_BLUE = "light-blue"
    ORANGE = "orange"
    RAILROAD = "railroad"
    RED = "red"
    PURPLE = "purple"
    VIOLET = "violet"
    YELLOW = "yellow"


class PropertyStatus(str, Enum):
    OWNED = "owned"
    VACANT = "vacant"


class RollResultCodes(IntEnum):
    THIRD_DOUBLE = 98
    JAIL_DOUBLE = 99
