import sqlalchemy as sa
from sqlalchemy import orm

from yubichecker.model import meta

def init_model(bind):
  global engine,Session
  """Call me before using any of the tables or classes in the model"""
  engine = bind
  Session = orm.scoped_session(
    orm.sessionmaker(autocommit=False, autoflush=True, bind=bind))
  orm.mapper(id_AES, aes_table, properties={'yubikey': orm.relation(Key)} )
  orm.mapper(Key, key_table, properties={'yubi_aes': orm.relation(id_AES), 'api': orm.relation(API)} )
  orm.mapper(API, api_table)

meta = sa.MetaData()


aes_table = sa.Table('aes', meta,
    sa.Column('id', sa.types.Integer, primary_key=True),
    sa.Column('aes', sa.types.String(255), unique=True),
    )

key_table = sa.Table('key', meta,
    sa.Column('id',         sa.types.Integer,    primary_key=True),
    sa.Column('id_aes',     sa.types.Integer,    sa.ForeignKey('aes.id')),
    sa.Column('private_id', sa.types.String(32), unique=True),
    sa.Column('api_key',    sa.types.Integer, sa.ForeignKey('api.id')),
    sa.Column('public_id',  sa.types.String(32), unique=True),
    sa.Column('email',      sa.types.String(255) ),
    sa.Column('increment',  sa.types.Integer),
    )

api_table = sa.Table('api', meta,
    sa.Column('id',  sa.types.Integer, primary_key=True),
    sa.Column('key', sa.types.String(255), unique=True),
    )

class id_AES(object):
  pass

class Key(object):
  pass

class API(object):
  pass

## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass
