"""seed deed data

Revision ID: 85c69722775d
Revises: 016f036af1b6
Create Date: 2023-06-19 20:44:06.059473

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "85c69722775d"
down_revision = "016f036af1b6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "deeds",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("gamespace_id", sa.Integer(), nullable=True),
        sa.Column("deed_type", sa.String(length=50)),
        sa.Column("rent", sa.Integer(), nullable=True),
        sa.Column("rent_group", sa.Integer(), nullable=True),
        sa.Column("rent_1_house", sa.Integer(), nullable=True),
        sa.Column("rent_2_houses", sa.Integer(), nullable=True),
        sa.Column("rent_3_houses", sa.Integer(), nullable=True),
        sa.Column("rent_4_houses", sa.Integer(), nullable=True),
        sa.Column("rent_hotel", sa.Integer(), nullable=True),
        sa.Column("house_cost", sa.Integer(), nullable=True),
        sa.Column("hotel_cost", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_deeds_id"), "deeds", ["id"], unique=False)
    stmt = (
        "INSERT INTO deeds (id, gamespace_id, deed_type, rent, rent_group, rent_1_house, "
        "rent_2_houses, rent_3_houses, rent_4_houses, rent_hotel, house_cost, hotel_cost) VALUES "
        "(1, 1, 'property', 2, 4, 10, 30, 90, 160, 250, 50, 50), "
        "(3, 3, 'property', 4, 8, 20, 60, 180, 320, 450, 50, 50), "
        "(6, 6, 'property', 6, 12, 30, 90, 270, 400, 550, 50, 50), "
        "(8, 8, 'property', 6, 12, 30, 90, 270, 400, 550, 50, 50), "
        "(9, 9, 'property', 8, 16, 40, 100, 300, 450, 600, 50, 50), "
        "(11, 11, 'property', 10, 20, 50, 150, 450, 620, 750, 100, 100), "
        "(13, 13, 'property', 10, 20, 50, 150, 450, 620, 750, 100, 100), "
        "(14, 14, 'property', 12, 24, 60, 180, 500, 700, 900, 100, 100), "
        "(16, 16, 'property', 14, 28, 70, 200, 550, 750, 950, 100, 100), "
        "(18, 18, 'property', 14, 28, 70, 200, 550, 750, 950, 100, 100), "
        "(19, 19, 'property', 16, 32, 80, 220, 600, 800, 1000, 100, 100), "
        "(21, 21, 'property', 18, 36, 90, 250, 700, 875, 1050, 150, 150), "
        "(23, 23, 'property', 18, 36, 90, 250, 700, 875, 1050, 150, 150), "
        "(24, 24, 'property', 20, 40, 100, 300, 750, 925, 1100, 150, 150), "
        "(26, 26, 'property', 22, 44, 110, 330, 800, 975, 1150, 150, 150), "
        "(27, 27, 'property', 22, 44, 110, 330, 800, 975, 1150, 150, 150), "
        "(29, 29, 'property', 24, 48, 120, 360, 850, 1025, 1200, 150, 150), "
        "(31, 31, 'property', 26, 52, 130, 390, 900, 1100, 1275, 200, 200), "
        "(32, 32, 'property', 26, 52, 130, 390, 900, 1100, 1275, 200, 200), "
        "(34, 34, 'property', 28, 56, 150, 450, 1000, 1200, 1400, 200, 200), "
        "(37, 37, 'property', 35, 70, 175, 500, 1100, 1300, 1500, 200, 200), "
        "(39, 39, 'property', 50, 100, 200, 600, 1400, 1700, 2000, 200, 200)"
    )
    op.execute(stmt)
    op.create_foreign_key(None, "deeds", "gamespaces", ["gamespace_id"], ["id"])

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DELETE FROM deeds")
    op.drop_index(op.f("ix_deeds_id"), table_name="deeds")
    op.drop_table("deeds")
    # ### end Alembic commands ###