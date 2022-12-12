from flask import Flask,render_template, Response, request
import pymongo
import json
from bson.objectid import ObjectId
from datetime import date

app = Flask(__name__)

try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS= 1000
    )
    db = mongo.abcBook
    mongo.server_info()
except:
    print("Error - Cannot Connect to DB")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/users',methods=['GET'])
def get_user():
    try:
        users = list(db.users.find())
        for user in users:
            user["_id"] = str(user["_id"])
        return Response(
            response = json.dumps(users),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message":"cannot read users" }),status=500,mimetype="application/json")        

@app.route('/users',methods=['POST'])
def create_user():
    try:
        user = {
            "name":request.form["name"],
            "role":request.form["role"],
            "dateJoined":[date.today().strftime("%d/%m/%Y")]
        }
        dbResponse = db.users.insert_one(user)

        return Response(
            response = json.dumps(
                {"message":"user created",
                "id":f"{dbResponse.inserted_id}"
                }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        return Response(
            response = json.dumps({"message":"cannot create user" }),status=500,mimetype="application/json")        

@app.route('/users/<idx>',methods=['PATCH'])
def update_user(idx):
    try:
        
        dbResponse = db.users.update_one(
            {"_id":ObjectId(idx)},
            {"$set":{"name":request.form["name"]}}
        )
        updateMessage = "user updated" if dbResponse.deleted_count == 1 else "user not changed"
        
        return Response(
            response = json.dumps({"message":updateMessage}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message":"cannot update user" }),status=500,mimetype="application/json")        

@app.route('/users/<idx>',methods=['DELETE'])
def delete_user(idx):
    try:
        dbResponse = db.users.delete_one({"_id":ObjectId(idx)})
        delMessage = "user deleted" if dbResponse.deleted_count == 1 else "user not found"
        return Response(
            response = json.dumps(
            {"message": delMessage}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message":"cannot delete user" }),status=500,mimetype="application/json")        

@app.route('/books',methods=['GET'])
def get_book():
    try:
        books = list(db.books.find())
        for book in books:
            book["_id"] = str(book["_id"])
        return Response(
            response = json.dumps(books),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message":"cannot read books" }),status=500,mimetype="application/json")        

@app.route('/books',methods=['POST'])
def create_book():
    try:
        book = {
            "title":request.form["title"],
            "description":request.form["description"],
            "genre":request.form["genre"],
            "author":request.form["author"],
            "yearPublished":request.form["yearPublished"],
            "availStatus":bool(request.form["availStatus"]),
            "lastBorrower":request.form["lastBorrower"],
        }
        dbResponse = db.books.insert_one(book)

        return Response(
            response = json.dumps(
                {"message":"book created",
                "id":f"{dbResponse.inserted_id}"
                }),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        return Response(
            response = json.dumps({"message":"cannot create book" }),status=500,mimetype="application/json")        

@app.route('/books/<idx>',methods=['PATCH'])
def update_book(idx,):
    try:
        
        dbResponse = db.books.update_one(
            {"_id":ObjectId(idx)},
            {"$set":{"name":request.form["name"]}}
        )
        updateMessage = "book updated" if dbResponse.modified_count == 1 else "book not changed"
        
        return Response(
            response = json.dumps({"message":updateMessage}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message":"cannot update book" }),status=500,mimetype="application/json")        

@app.route('/books/<idx>',methods=['DELETE'])
def delete_book(idx):
    try:
        dbResponse = db.books.delete_one({"_id":ObjectId(idx)})
        delMessage = "book deleted" if dbResponse.deleted_count == 1 else "book not found"
        return Response(
            response = json.dumps(
            {"message": delMessage}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message":"cannot delete book" }),status=500,mimetype="application/json")        

@app.route('/books/<idx>',methods=['PATCH'])
def borrow_book(idx,user):
    try:
        dbResponse = db.books.update_one(
            {"_id":ObjectId(idx)},
            {"$set":{"availStatus": False,"lastBorrower":"userName"}}
        )
        borrowMessage = "book borrowed successfully" if dbResponse.modified_count == 1 else "book not available"
        
        return Response(
            response = json.dumps({"message":borrowMessage}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message":"error borrowing book" }),status=500,mimetype="application/json")        

@app.route('/books/<idx>',methods=['PATCH'])
def return_book(idx):
    try:
        dbResponse = db.books.update_one(
            {"_id":ObjectId(idx)},
            {"$set":{"availStatus": True}}
        )
        returnMessage = "book returned successfully" if dbResponse.modified_count == 1 else "book not available"
        
        return Response(
            response = json.dumps({"message":returnMessage}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response = json.dumps({"message":"error returning book" }),status=500,mimetype="application/json")        

if __name__ == "__main__":
    app.run(port=80,debug=True)