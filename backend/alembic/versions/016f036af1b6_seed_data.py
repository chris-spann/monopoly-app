"""seed data

Revision ID: 016f036af1b6
Revises: ef0cd3ffe061
Create Date: 2023-06-19 19:22:27.410203

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "016f036af1b6"
down_revision = "ef0cd3ffe061"
branch_labels = None
depends_on = None

stmt = (
    'INSERT INTO gamespaces (id, name, value, type, "group", status) VALUES '
    "(0, 'GO', 200, 'free', Null, 'vacant'), "
    "(1, 'Mediterranean Ave', 60, 'property', 'violet', 'vacant'), "
    "(2, 'Community Chest', 0, 'draw-chest', Null, 'vacant'), "
    "(3, 'Baltic Ave', 60, 'property', 'violet', 'vacant'), "
    "(4, 'Income Tax', 200, 'tax-income', Null, 'vacant'), "
    "(5, 'Reading Railroad', 200, 'railroad', 'railroad', 'vacant'), "
    "(6, 'Oriental Ave', 100, 'property', 'light-blue', 'vacant'), "
    "(7, 'Chance', 0, 'draw-chance', Null, 'vacant'), "
    "(8, 'Vermont Ave', 100, 'property', 'light-blue', 'vacant'), "
    "(9, 'Connecticut Ave', 120, 'property', 'light-blue', 'vacant'), "
    "(10, 'Jail', 500, 'jail', Null, 'vacant'), "
    "(11, 'St Charles Place', 140, 'property', Null, 'vacant'), "
    "(12, 'Electric Company', 150, 'utility', 'utility', 'vacant'), "
    "(13, 'States Ave', 140, 'property', 'purple', 'vacant'), "
    "(14, 'Virginia Ave', 160, 'property', 'purple', 'vacant'), "
    "(15, 'Pennsylvania Railroad', 200, 'railroad', 'railroad', 'vacant'), "
    "(16, 'St James Place', 180, 'property', 'orange', 'vacant'), "
    "(17, 'Community Chest', 0, 'draw-chest', Null, 'vacant'), "
    "(18, 'Tennesee Ave', 180, 'property', 'orange', 'vacant'), "
    "(19, 'New York Ave', 200, 'property', 'orange', 'vacant'), "
    "(20, 'Free Parking', 0, 'free', Null, 'vacant'), "
    "(21, 'Kentucky Ave', 220, 'property', 'red', 'vacant'), "
    "(22, 'Chance', 0, 'draw-chance', Null, 'vacant'), "
    "(23, 'Indiana Ave', 220, 'property', 'red', 'vacant'), "
    "(24, 'Illinois Ave', 240, 'property', 'red', 'vacant'), "
    "(25, 'B & O Railroad', 200, 'railroad', 'railroad', 'vacant'), "
    "(26, 'Atlantic Ave', 260, 'property', 'yellow', 'vacant'), "
    "(27, 'Ventnor Ave', 260, 'property', 'yellow', 'vacant'), "
    "(28, 'Water Works', 150, 'utility', 'utility', 'vacant'), "
    "(29, 'Marvin Gardens', 280, 'property', 'yellow', 'vacant'), "
    "(30, 'Go to Jail', 0, 'go-to-jail', Null, 'vacant'), "
    "(31, 'Pacific Ave', 300, 'property', 'green', 'vacant'), "
    "(32, 'North Carolina Ave', 300, 'property', 'green', 'vacant'), "
    "(33, 'Community Chest', 0, 'draw-chest', Null, 'vacant'), "
    "(34, 'Pennsylvania Ave', 320, 'property', 'green', 'vacant'), "
    "(35, 'Short Line', 200, 'railroad', 'railroad', 'vacant'), "
    "(36, 'Chance', 0, 'draw-chance', Null, 'vacant'), "
    "(37, 'Park Place', 350, 'property', 'blue', 'vacant'), "
    "(38, 'Luxury Tax', 75, 'tax', Null, 'vacant'), "
    "(39, 'Boardwalk', 400, 'property', 'blue', 'vacant') "
)

card_stmt = (
    "INSERT INTO cards (id, title, type, is_gooj, action_code) VALUES "
    "(1, 'Advance to Go (Collect $200)', 'community-chest', false, 'ADV-GO'), "
    "(2, 'From sale of stock, you get $45', 'community-chest', false, 'ADD-045'), "
    "(3, 'You inherit $100', 'community-chest', false, 'ADD-100'), "
    "(4, 'Pay hospital $100', 'community-chest', false, 'PAY-100'), "
    "(5, 'Grand Opera Opening. Collect $50 from every player for opening night seats.', "
    "'community-chest', false, 'ADD-X50'), "
    "(6, 'Income Tax Refund. Collect $20', 'community-chest', false, 'ADD-020'), "
    "(7, 'Receive for services, $20', 'community-chest', false, 'ADD-020'), "
    "(8, 'Doctor Fee. Pay $50', 'community-chest', false, 'PAY-050'), "
    "(9, 'Go to jail. Go directly to jail. Do not pass go. Do not collect $200', "
    "'community-chest', false, 'GO-JAIL'), "
    "(10, 'Bank error in your favor. Collect $200', 'community-chest', false, 'ADD-200'), "
    "(11, 'Xmas fund matures. Collect $100', 'community-chest', false, 'ADD-100'), "
    "(12, 'Life insurance matures. Collect $100', 'community-chest', false, 'ADD-100'), "
    "(13, 'Get out of jail free. (This card may be kept until needed, or sold)', "
    "'community-chest', true, 'GOOJF'), "
    "(14, 'Pay School tax of $150', 'community-chest', false, 'PAY-150'), "
    "(15, 'You have won 2nd price in a beauty contest. Collect $10', 'community-chest', "
    "false, 'ADD-010'), "
    "(16, 'You are assessed for street repairs. $40 per house, $115 per hotel', "
    "'community-chest', false, 'PAY-040-115'), "
    "(17, 'You have been elected chairman of the board. Pay each player $50', "
    "'chance', false, 'PAY-A50'), "
    "(18, 'Your building and loan matures. Collect $150', 'chance', false, 'ADD-150'), "
    "(19, 'Get out of jail free. This card may be kept until needed, or sold', "
    "'chance', true, 'GOOJF'), "
    "(20, 'Bank Pays you dividend of $50', 'chance', false, 'ADD-050'), "
    "(21, 'Pay poor tax of $15', 'chance', false, 'PAY-015'), "
    "(22, 'Take a ride on the Reading. If you pass go, collect $200', 'chance', false, 'GO-RERD'), "
    "(23, 'Advance to go (Collect $200)', 'chance', false, 'ADV-GO'), "
    "(24, 'Advance to St. Charles Place. If you pass go, collect $200', 'chance', "
    "false, 'ADV-STC'), "
    "(25, 'Go back 3 spaces', 'chance', false, 'BAC-003'), "
    "(26, 'Take a walk on the Boardwalk. Advance token to Boardwalk', 'chance', false, 'ADV-BRD'), "
    "(27, 'Advance token to the nearest Railroad and pay owner twice the rental to which he/she is "
    "otherwise entitled. If Railroad if UNOWNED, you may purchase it from the bank', "
    "'chance', false, 'ADV-RR'), "
    "(28, 'Advance token to the nearest Railroad and pay owner twice the rental to which he/she is "
    "otherwise entitled. If Railroad if UNOWNED, you may purchase it from the bank', "
    "'chance', false, 'ADV-RR'), "
    "(29, 'Advance token to the nearest utility. If UNOWNED you may buy if from the bank. If OWNED,"
    " throw dice and pay owner a total ten times the amount thrown', 'chance', false, 'ADV-UT'), "
    "(30, 'Advance to Illinois Ave', 'chance', false, 'ADV-ILL'), "
    "(31, 'Go directly to jail. Do not pass GO. Do not collect $200', 'chance', false, 'GO-JAIL'), "
    "(32, 'Make general repairs on all your property. For each house pay $25, "
    "for each hotel $100', 'chance', false, 'PAY-025-100')"
)


def upgrade() -> None:
    op.execute(stmt)
    op.execute(card_stmt)


def downgrade() -> None:
    op.execute("DELETE FROM gamespaces")
    op.execute("DELETE FROM cards")
