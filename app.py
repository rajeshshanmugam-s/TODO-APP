# Flask Basic structure
# Create Mongo DB Connector
# List of Endpoints 1. Insert, 2. Read, 3. Delete,
# Add JWT Middleware
from flask import Flask, request
import json

from config import mongo_coll
from data_models import Item, UpdateModel

app = Flask(__name__)


@app.route("/test", methods=["GET"])
def test_endpoint():
    return "working"


@app.route("/todo/insert", methods=["POST"])
def add_todo():
    item = Item.model_validate(json.loads(request.data))
    res = mongo_coll_todo.insert_one(item.model_dump())
    if res.acknowledged:
        return {"status": "Inserted successfully"}, 201
    else:
        return {"status": "DB Error"}, 500


@app.route("/todo/list_all", methods=["GET"])
def list_all_items():
    res = mongo_coll_todo.find({}, {"_id": False})
    return list(res)


@app.route("/todo/find/<item_id>", methods=["GET"])
def retrieve_via_id(item_id):
    res = mongo_coll_todo.find_one({"item_id": int(item_id)}, {"_id": False})
    if not res:
        return {"status": f"Requested ID {item_id} not found"}, 404
    return res


@app.route("/todo/update/<item_id>", methods=["PUT"])
def update_item(item_id):

    update_value = UpdateModel.model_validate(json.loads(request.data))
    update_value = {"$set": update_value.model_dump()}
    filter_value = {"item_id": int(item_id)}

    res = mongo_coll_todo.update_one(filter_value, update_value)
    if res.modified_count == 0:
        return {"status": f"ID: {item_id} not Updated"}, 400

    return {"status": f"ID: {item_id}  Updated successfully"}


@app.route("/todo/delete/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    res = mongo_coll_todo.delete_one({"item_id": int(item_id)})
    if not res:
        return {"status": f"Requested ID {item_id} not found"}, 404
    return {"status": f"Successfully deleted the ID {item_id}"}


if __name__ == "__main__":
    app.run(debug=True)
