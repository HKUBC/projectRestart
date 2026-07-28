import sqlalchemy as sa
from app.db.db_setup import metadata

users_items = sa.Table(
    "",
    metadata,
    sa.Column(),
    sa.Column(),
    sa.Column()
)