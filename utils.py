#mine the block
curl http://localhost:5000/mine


#new transaction
curl http://localhost:5000/transactions/new



#work without postman
$ curl -X POST -H "Content-Type: application/json" -d '{
 "sender": "d4ee26eee15148ee92c6cd394edd974e",
 "recipient": "someone-other-address",
 "amount": 5
}' "http://localhost:5000/transactions/new