import requests

BASE = "http://127.0.0.1:5000/"

postResponse = requests.post(BASE + "order", {"customer_id": "tengis", "book_ids": [1, 2, 3, 4]})
print(postResponse.json())

input()

getResponse = requests.get(BASE + "list/tengis")
print(getResponse.json())

input()

order_id = postResponse.json()["order_id"]
deleteResponse = requests.delete(BASE + f"delete/{order_id}")
print(deleteResponse)

