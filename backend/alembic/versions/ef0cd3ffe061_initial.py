"""initial

Revision ID: ef0cd3ffe061
Revises:
Create Date: 2023-06-19 17:52:34.952628

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ef0cd3ffe061"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "authors",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column(
            "time_created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("time_updated", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cards",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("type", sa.String(length=50), nullable=True),
        sa.Column("is_gooj", sa.Boolean(), nullable=True),
        sa.Column("action_code", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cards_id"), "cards", ["id"], unique=False)
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.Column("cash", sa.Integer(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=True),
        sa.Column("in_jail", sa.Boolean(), nullable=True),
        sa.Column("roll_1", sa.Boolean(), nullable=True),
        sa.Column("roll_2", sa.Boolean(), nullable=True),
        sa.Column("roll_3", sa.Boolean(), nullable=True),
        sa.Column("jail_count", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_players_id"), "players", ["id"], unique=False)
    op.create_index(op.f("ix_players_name"), "players", ["name"], unique=False)
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column(
            "time_created",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("time_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["authors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_books_id"), "books", ["id"], unique=False)
    op.create_table(
        "gamespaces",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.Column("value", sa.Integer(), nullable=True),
        sa.Column("type", sa.String(length=50), nullable=True),
        sa.Column("group", sa.String(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["players.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_gamespaces_id"), "gamespaces", ["id"], unique=False)
    op.create_index(op.f("ix_gamespaces_name"), "gamespaces", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_gamespaces_name"), table_name="gamespaces")
    op.drop_index(op.f("ix_gamespaces_id"), table_name="gamespaces")
    op.drop_table("gamespaces")
    op.drop_index(op.f("ix_books_id"), table_name="books")
    op.drop_table("books")
    op.drop_index(op.f("ix_players_name"), table_name="players")
    op.drop_index(op.f("ix_players_id"), table_name="players")
    op.drop_table("players")
    op.drop_index(op.f("ix_cards_id"), table_name="cards")
    op.drop_table("cards")
    op.drop_table("authors")
    # ### end Alembic commands ###
