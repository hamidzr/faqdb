#init db
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine

engine = create_engine('sqlite+pysqlite:///test.db', module=sqlite)
# engine = create_engine('sqlalchemy.db', echo=True)

#create session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

#base class
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


#define classes
from sqlalchemy import Column, Integer, String
class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	fullname = Column(String)
	password = Column(String)

	def __repr__(self):
	  return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)


#create all databases
Base.metadata.create_all(engine)


#start a session? 

session = Session()

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)

#force commit
session.commit()

#test
u = session.query(User).all()
print u
