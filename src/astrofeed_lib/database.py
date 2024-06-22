from datetime import datetime

import peewee
from .config import DatabaseConfig


# Local DB:
# db = peewee.SqliteDatabase('feed_database.db')
# print(DATABASE_HOST, DATABASE_PORT, DATABASE_USER, DATABASE_PASSWORD)

# MySQL DB:
DATABASE_CONFIG = DatabaseConfig()
db = peewee.MySQLDatabase(DATABASE_CONFIG.name, **DATABASE_CONFIG.params)


class BaseModel(peewee.Model):
    class Meta:
        database = db


# Todo should set attributes based on feeds / have some way to add new columns to the mysql db
class Post(BaseModel):
    indexed_at = peewee.DateTimeField(default=datetime.utcnow, index=True)
    uri = peewee.CharField(index=True)
    cid = peewee.CharField(index=True)
    author = peewee.CharField()
    text = peewee.CharField()
    feed_all = peewee.BooleanField(default=False)
    feed_astro = peewee.BooleanField(default=False)
    feed_exoplanets = peewee.BooleanField(default=False)
    feed_astrophotos = peewee.BooleanField(default=False)
    # feed_moderation = peewee.BooleanField(default=False)
    # reply_parent = peewee.CharField(null=True, default=None)
    # reply_root = peewee.CharField(null=True, default=None)


class SubscriptionState(BaseModel):
    service = peewee.CharField(unique=True)
    cursor = peewee.IntegerField()


class Account(BaseModel):
    handle = peewee.CharField(index=True)
    submission_id = peewee.CharField()
    did = peewee.CharField(default="not set", index=True)
    is_valid = peewee.BooleanField()
    feed_all = peewee.BooleanField(default=False)  # Also implicitly includes allowing feed_astro
    indexed_at = peewee.DateTimeField(default=datetime.utcnow)
    mod_level = peewee.IntegerField(null=False, index=True, unique=False, default=0)


class BotActions(BaseModel):
    indexed_at = peewee.DateTimeField(default=datetime.utcnow, index=True)
    did = peewee.CharField(default="not set")
    type = peewee.CharField(null=False, default="unrecognized", index=True)
    stage = peewee.CharField(null=False, default="initial", index=True)  # Initial: command initially sent but not replied to
    parent_uri = peewee.CharField(null=False, default="")
    parent_cid = peewee.CharField(null=False, default="")
    latest_uri = peewee.CharField(null=False , default="")
    latest_cid = peewee.CharField(null=False , default="")
    complete = peewee.BooleanField(null=False, default=False, index=True)


class ModActions(BaseModel):
    indexed_at = peewee.DateTimeField(default=datetime.utcnow, index=True)
    did_mod = peewee.CharField(index=True, null=False)
    did_user = peewee.CharField(index=True)
    action = peewee.CharField(index=True, null=False)
    expiry = peewee.DateTimeField(index=True)



# class Signups(BaseModel):
#     did = peewee.CharField(index=True)
#     status = peewee.CharField(index=True)
#     uri = peewee.CharField()
#     cid = peewee.CharField()


if db.is_closed():
    db.connect()
    db.create_tables([Post, SubscriptionState, Account, BotActions, ModActions])
    if not db.is_closed():
        db.close()
