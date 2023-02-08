from peewee import *
import datetime

DATABASE='tweepee1.db'

database=SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database=database

class User(BaseModel):
    username= CharField(unique=True,primary_key=True)
    password= CharField()
    email= CharField()
    join_date= DateTimeField(default=datetime.datetime.utcnow())

class Post(BaseModel):
    caption=CharField()
    poster = ForeignKeyField(User, to_field="username")

def create_tables():
    database.connect()
    database.create_tables([User],safe=True)
    database.create_tables([Post],safe=True)
    database.close()

create_tables()


user = User.create(username= "13", password= "qwee",email ="hello@gmasil.com")
User.create(username= "12e3", password= "qwdse",email ="hellodsa@gmail.com")
User.create(username= "12233", password= "qwsdccdce",email ="llo@gmail.com")
User.create(username= "3", password= "qwcdsfe",email ="hello@gdfhjmail.com")
User.create(username= "Aryan", password= "q4wee",email ="hell2o@gmasil.com")
user.save()

post=Post.create(caption="hello",poster="Aryan")
Post.create(caption="hello cogoport",poster="Nitish")

post.save()

query = Post.select().join(User).where(User.username == 'Aryan')
for i in query:
    print(i.poster.password)




