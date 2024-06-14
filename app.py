# Flask Basic structure
# Create Mongo DB Connector
# List of Endpoints 1. Insert, 2. Read, 3. Delete,
# Add JWT Middleware
from flask import Flask, request
import json
app = Flask(__name__)

from pydantic import BaseModel
from datetime import datetime


class Item(BaseModel):
    id: int
    name: str
    description: str
    created_at: str


@app.route("/test", methods=["GET"])
def test_endpoint():
    return "working"


@app.route("/todo/insert", methods=["POST"])
def add_todo():
    item = Item.model_validate(json.loads(request.data))
    return item.model_dump()


if __name__ == "__main__":
    app.run()
