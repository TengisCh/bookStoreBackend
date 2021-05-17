from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from _datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


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
    book_ids = db.relationship('Book', backref='order', lazy=True)

    def __repr__(self):
        return f'{self.order_id}'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'))

    def __repr__(self):
        return f'{self.book_id}'

# db.create_all()
# customer = Customer(customer_id="tengis")
# db.session.add(customer)
# db.session.commit()



# def oder_id_generator():
#     datetime.now().strftime("%y%m%d%H%M%S%f")
#
#
# def post_data(customer_id, book_ids):
#     customer = Customer(customer_id=customer_id)
#     db.session.add(customer)
#     db.session.commit()
#     customer.customer_id
#     order = Book(book_id=args["book_ids"], order_id=customer)
#     return {"order_id": order_id}
