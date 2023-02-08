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

class Likes(BaseModel):
    userid= ForeignKeyField(User, to_field="username")
    posterid = ForeignKeyField(Post, to_field="id")
    numberlikes= IntegerField()
    
class Authentication(BaseModel):
    username= ForeignKeyField(User, to_field="username")
    password= ForeignKeyField(User, to_field="password")


def create_tables():
    database.connect()
    database.create_tables([User],safe=True)
    database.create_tables([Post],safe=True)
    database.create_tables([Likes],safe=True)
    database.create_tables([Authentication],safe=True)
    database.close()

create_tables()


# user = User.create(username= "13", password= "qwee",email ="hello@gmasil.com")
# User.create(username= "12e3", password= "qwdse",email ="hellodsa@gmail.com")
# User.create(username= "12233", password= "qwsdccdce",email ="llo@gmail.com")
# User.create(username= "3", password= "qwcdsfe",email ="hello@gdfhjmail.com")
# User.create(username= "Aryan", password= "q4wee",email ="hell2o@gmasil.com")
# user.save()

# post=Post.create(caption="hello",poster="Aryan")
# Post.create(caption="hello cogoport",poster="Nitish")

# post.save()

# like=Likes.create(userid="12345",posterid="1",numberlikes="69")
# Likes.create(userid="145",posterid="2",numberlikes="13") 
# like.save()
# authentication= Authentication.create(username= "13", password= "qwee")
# Authentication.create(username= "12e3", password= "qwdse")
# Authentication.create(username= "12233", password= "qwsdccdce")
# Authentication.create(username= "3", password= "qwcdsfe")
# Authentication.create(username= "Aryan", password= "q4wee")
# authentication.save()
from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def read_root():
    return{"Hello": "World"}

# @app.get("/")
# def func():

@app.get("/get_users")
def func():
    hi=User.select()
    arr=[]
    for i in hi:
        arr.append(i.username)
    return arr

@app.get("/getsingleuser/{ij}")
def funct(ij):
    h=User.select()

    for j in h:
        if j.username==ij:
            return j

@app.get("/getposts")
def fu():
    h=[]
    k=Post.select()
    for i in k:
        h.append(i)
    return h

@app.get("/getbyuser/{x}")
def funtio(x):
    k=Post.select()
    for i in k:
        if i.poster.username==x:
            return i






@app.put("/increaselikes/{x}")
def func(x):
    k=Likes.select()
    for i in k:
        if i.posterid_id==int(x):
            print(i.numberlikes)
            i.numberlikes = i.numberlikes + 1
            i.save()
            return {"post": "was liked"}

@app.put("/decreaselikes/{x}")
def func(x):
    k=Likes.select()
    for i in k:
        if i.posterid_id==int(x):
            print(i.numberlikes)
            i.numberlikes = i.numberlikes - 1
            # i.save()
            return {"post": "was disliked"}

@app.delete("/deleteposts/{x}")
def funct(x):
    
    query = Likes.delete().where(Likes.posterid ==x)
    query.execute()
    return {"post": "deleted"}

@app.get("/partialsearch/{x}")
def search_job(x):
    k=User.select().where(User.username.startswith(x))
    a=[]
    for i in k:
        a.append(i)
    return a

@app.get("/gethead/{x}")
def func(x):
    a=[]
    for i in range(0,int(x)):
        a.append(Post.select()[i])
    return a
from fastapi import File, UploadFile
# @app.post("/upload")
# def upload(file: UploadFile = File(...)):
#     try:
#         contents = file.file.read()
#         with open(file.filename, 'abc.txt') as f:
#             f.write(contents)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         file.file.close()

#     return {"message": f"Successfully uploaded {file.filename}"}



from typing import List

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()
@app.post("/uploadfile/")
async def create_upload_file(data: UploadFile):
#Prints result in cmd – verification purpose
    print(data.filename)
#Sends server the name of the file as a response
    return {"Filename": data.filename}

# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile]):
#     return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<input name="data" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# @app.post("/putnewuser/{x}/{y}")
# def func(x,y):
#     k=User.select().where(User.username==x or User.password==y)
#     if(len(k)>=1):
#         return {"user": "exists"}   
#     else:
#         u = User.create(username= x, password= y,email ="hellsdhco@gmasil.com")
#         u.save()
#         return {"user": "added"}

from fastapi import Form, status
from fastapi.responses import RedirectResponse

@app.post("/enteridp/")
async def createdata(x: str=Form(...), y: str=Form(...)):
    k=User.select().where(User.username==x or User.password==y)
    if(len(k)>=1):
        l=User.select().where(User.username==x and User.password==y)
        if(len(l)>=1):
            content = """
        <body>
        <form action="/authtoken" enctype="multipart/form-data" method="post">
        Image:
        <input name="data" type="image" src="https://upload.wikimedia.org/wikipedia/commons/6/6e/Shah_Rukh_Khan_graces_the_launch_of_the_new_Santro.jpg" width="300px"><br><br>
        Caption:
        <textarea name="cbox" rows="10" cols="55">Enter content here</textarea>
        <br><br>
        Enter Authentication token:
        <input name="x" type="number">
        <input type="submit">
        </form>
        </body>
            """
            return HTMLResponse(content=content)
        return {"user": "exists"}   
    else:
        u = User.create(username= x, password= y,email ="hsdhco@gmasil.com")
        a = Authentication.create(username=x, password= y)
        u.save()
        a.save()
        return {"user": "added"}

@app.post("/authtoken")
async def func(x: int=Form(...), u: str=Form(...),p: str=Form(...)):
    k=Authentication.select().where(Authentication.id==x and
    Authentication.username==u and Authentication.password==p)
    if(len(k)>=1):
        return {"user": "exists"}
    else:
        return {"error 403"}

@app.get("/redirected")
async def func():
    content = """
<body>
<form action="/authtoken" enctype="multipart/form-data" method="post">
Enter Authentication token:
<input name="x" type="number">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.get("/putuserpw")
async def main():
    content = """
<body>
<form action="/enteridp/" enctype="multipart/form-data" method="post">
Username:
<input name="x" type="text">
Password:
<input name="y" type="password">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


