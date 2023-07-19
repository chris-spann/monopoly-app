from enum import Enum, IntEnum

PASS_GO_AMOUNT = 200


class CardType(str, Enum):
    COMMUNITY_CHEST = "community-chest"
    CHANCE = "chance"


class GameSpaceType(str, Enum):
    DRAW_CHEST = "draw-chest"
    DRAW_CHANCE = "draw-chance"
    FREE = "free"
    GO_TO_JAIL = "go-to-jail"
    JAIL = "jail"
    PROPERTY = "property"
    RAILROAD = "railroad"
    TAX = "tax"
    TAX_INCOME = "tax-income"
    UTILITY = "utility"


class PayType(str, Enum):
    INCOME_TAX = "income-tax"
    TAX = "tax"
    RENT = "rent"


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
    OWNED_GROUP = "owned-group"
    OWNED_1_HOUSE = "owned-1-house"
    OWNED_2_HOUSES = "owned-2-houses"
    OWNED_3_HOUSES = "owned-3-houses"
    OWNED_4_HOUSES = "owned-4-houses"
    OWNED_HOTEL = "owned-hotel"


class RollResultCode(IntEnum):
    THIRD_DOUBLE = 98
    JAIL_DOUBLE = 99
