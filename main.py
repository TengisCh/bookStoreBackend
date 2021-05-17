from flask import Flask, request
from flask_restful import Resource, Api, abort, reqparse
import uuid
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class OrderModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), nullable=False)
    customer_id = db.Column(db.String(20), nullable=False)
    book_ids = db.Column(db.List, nullable=False)

    def __repr__(self):
        return f"Order(Order ID = {self.order_id}, Customer ID = {self.customer_id}, Book IDs = {self.book_ids})"

db.create_all()

order_post_args = reqparse.RequestParser()
order_post_args.add_argument("customer_id", type=str, help="Please send customer ID", required=True)
order_post_args.add_argument("book_ids", type=int, action="append", help="Please send book Id(s)", required=True)

data = {}


class PlaceOrder(Resource):
    def post(self):
        order_id = str(uuid.uuid4())
        args = order_post_args.parse_args()
        data[order_id] = args
        return {"order_id": order_id}


class ListOrders(Resource):
    def get(self, customer_id):
        order_id = "none"
        for key, value in data.items():
            if customer_id == value["customer_id"]:
                order_id = key
        try:
            return {order_id: data[order_id]["book_ids"]}
        except KeyError:
            abort(404, message="Please check the customer ID")


class DeleteOrder(Resource):
    def delete(self, order_id):
        if order_id not in data:
            abort(404, message="Order does not exist")
        else:
            del data[order_id]
            return 204


api.add_resource(ListOrders, "/list/<string:customer_id>")
api.add_resource(PlaceOrder, "/order")
api.add_resource(DeleteOrder, "/delete/<string:order_id>")

if __name__ == "__main__":
    app.run(debug=True)
