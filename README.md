# Bookstore’s backend service

**Add order**  
 - Input: customerId, list of bookIds
 - Output: orderId

**List orders** 
 - Input: customerId
 - Output: list of {orderId, list of bookIds} records

**Delete order** 
 - Input: orderId

## Description
**Used tools: flask, flask_restful, flask_sqlalchemy**

 - Multiple orders can be made for single user
 - customer_id , book_id(s) are integer
 - order_id is timestamp of the order time
 - Customer -> Order -> Book databases have one -> many relationships

test.py file can be used to test the functionalities.
