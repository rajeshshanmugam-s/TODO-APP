# Flask Basic structure
# Create Mongo DB Connector
# List of Endpoints 1. Insert, 2. Read, 3. Delete,
# Add JWT Middleware

from flask import Flask, request
from datetime import datetime

from config import mongo_coll_todo, mongo_coll_user
from data_models import Item, UpdateModel, User
from utils import generate_token, verify_token

app = Flask(__name__)


def validate_jwt(f):
    def decor(*args, **kargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"status": "Token is missing"}, 401
        # Bearer Token
        token = token.split(" ")[1]
        status, valid_token = verify_token(token)
        if not valid_token:
            return status, 401

        return f(*args, **kargs)

    return decor


@app.route("/test", methods=["GET"])
def test_endpoint():
    return "working"


@app.route("/users/register", methods=["POST"])
def register_user():
    user = User.model_validate(request.json)
    users_list = mongo_coll_user.find({"username": user.username})

    # FIXME: Encrypt the password before saving
    if list(users_list) == []:
        resp = mongo_coll_user.insert_one(user.model_dump())
        if resp.acknowledged:
            return {"status": "User added successfully"}, 201
        else:
            return {"status": "Unable to add User"}, 500

    return {"status": "Username already exists"}, 409


@app.route("/users/login", methods=["GET"])
def login_user():
    user = User.model_validate(request.json)
    user_list = mongo_coll_user.find_one(user.model_dump())
    if user_list:
        token = generate_token(user.username)
        return {"token": token}
    else:
        return {"status": "Invalid Username or Password"}, 401


@app.route("/todo/insert", methods=["POST"], endpoint="add_todo")
@validate_jwt
def add_todo():
    request_data = request.json
    request_data["created_at"] = datetime.now()  # TODO: If required, add Timezone
    item = Item(**request_data)
    res = mongo_coll_todo.insert_one(item.model_dump())
    if res.acknowledged:
        return {"status": "Inserted successfully"}, 201
    else:
        return {"status": "DB Error"}, 500


@app.route("/todo/list_all", methods=["GET"], endpoint="list_all_items")
@validate_jwt
def list_all_items():
    res = mongo_coll_todo.find({}, {"_id": False})
    return list(res)


@app.route("/todo/find/<item_id>", methods=["GET"], endpoint="retrieve_via_id")
@validate_jwt
def retrieve_via_id(item_id):
    res = mongo_coll_todo.find_one({"item_id": int(item_id)}, {"_id": False})
    if not res:
        return {"status": f"Requested ID {item_id} not found"}, 404
    return res


@app.route("/todo/update/<item_id>", methods=["PUT"], endpoint="update_item")
@validate_jwt
def update_item(item_id):

    update_value = UpdateModel.model_validate(request.json)
    update_value = {"$set": update_value.model_dump()}
    filter_value = {"item_id": int(item_id)}

    res = mongo_coll_todo.update_one(filter_value, update_value)
    if res.modified_count == 0:
        return {"status": f"ID: {item_id} not Updated"}, 400

    return {"status": f"ID: {item_id}  Updated successfully"}


@app.route("/todo/delete/<item_id>", methods=["DELETE"], endpoint="delete_item")
@validate_jwt
def delete_item(item_id):
    res = mongo_coll_todo.delete_one({"item_id": int(item_id)})
    if not res:
        return {"status": f"Requested ID {item_id} not found"}, 404
    return {"status": f"Successfully deleted the ID {item_id}"}


if __name__ == "__main__":
    app.run(debug=True)
