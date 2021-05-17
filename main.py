from flask import Flask
from flask_restful import Resource, Api, abort, reqparse, marshal_with, fields, marshal
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# Database tables with one to many relationships
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(20), nullable=False)

    order_ids = db.relationship('Order', backref='customer', lazy=True)

    def __repr__(self):
        return f'{self.customer_id}'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    book_ids = db.relationship('Book', backref='order', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'{self.order_id}'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))

    def __repr__(self):
        return f'{self.book_id}'


db.create_all()

# Request parser for post requests
order_post_args = reqparse.RequestParser()
order_post_args.add_argument("customer_id", type=str, help="Please send customer ID", required=True)
order_post_args.add_argument("book_ids", type=int, action="append", help="Please send book Id(s)", required=True)


# GET request, input: customer_id output: {order_id: [book_ids]}
class ListOrders(Resource):
    def get(self, customer_id):
        customer = Customer.query.filter_by(customer_id=customer_id).first()
        if customer is None:
            abort(404, message=f"No customer with id: [{customer_id}] found")

        result = {}
        i = 0
        for order_id in customer.order_ids:
            resource_fields_order = {f"order_id_{i}": fields.Integer(attribute="order_id")}
            order_dict = marshal(order_id, resource_fields_order)
            order_id_temp = order_dict[f"order_id_{i}"]

            result.update(order_dict)

            order = Order.query.filter_by(order_id=order_id_temp).first()
            j = 0
            book = {}
            for book_id in order.book_ids:
                resource_fields_book = {f"book_id_{j}": fields.Integer(attribute="book_id")}
                book_dict = marshal(book_id, resource_fields_book)
                book.update(book_dict)
                j += 1
            result["book_ids"] = book

        return result


def oder_id_generator():
    return datetime.now().strftime("%y%m%d%H%M%S%f")


def add_to_database(value):
    db.session.add(value)
    db.session.commit()


# POST request, input customer_id, book_ids output: order_id
class PlaceOrder(Resource):
    def post(self):
        args = order_post_args.parse_args()
        customer = Customer(customer_id=args["customer_id"])
        add_to_database(customer)

        order_id = oder_id_generator()
        order = Order(order_id=order_id, customer=customer)
        add_to_database(order)

        for book in args["book_ids"]:
            new_book = Book(book_id=book, order=order)
            add_to_database(new_book)

        return {"order_id": order_id}


# DELETE request, input: order_id
class DeleteOrder(Resource):
    def delete(self, order_id):
        order = Order.query.filter_by(order_id=order_id).first()
        db.session.delete(order)
        db.session.commit()


# Request APIs
api.add_resource(ListOrders, "/list/<string:customer_id>")
api.add_resource(PlaceOrder, "/order")
api.add_resource(DeleteOrder, "/delete/<string:order_id>")

if __name__ == "__main__":
    app.run(debug=True)
