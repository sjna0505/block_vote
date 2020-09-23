# block_vote
blockchain as a decentralized store of electronic voting

the central location of voting results is vulnerable to many risks and threats.
so using blockchain, we can implement simple decentralized vote result store which is more secure to data forgery, DDoS attack and data loss incident

I wrote a very simple voting system which can store voting results into distributed nodes.
The OS I worked is ubuntu 18.04

To run the code, flask module is needed
Please follow the instructions below
1. make sure you have python3
```
python3 -V
```
```
output
Python 3.6.9
```

2. install 'venv' module to use a virtual environment
```
sudo apt install python3-venv
```

3. create a virtual environment
```
mkdir my_flask_app
cd my_flask_app
python3 -m venv venv
source venv/bin/activate
```

4. install Flask
```
(venv) $ pip install Flask
```

5. copy blockvote.py into the my_flask_app directory and export FLASK_APP variable
```
(venv) $ export FLASK_APP=blockvote
```

6. run the node
```
(venv) $ flask run
 * Serving Flask app "blockvote"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

7. open one more terminal to run another node with 5001 port
```
$ source venv/bin/activate
(venv) $ export FLASK_APP=blockvote
(venv) $ flask run -p 5001
 * Serving Flask app "blockvote"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5001/ (Press CTRL+C to quit)
```

8. at another terminal run 'batch_curl.sh'
```
$ sh batch_curl.sh
```
9. check the result with 'results.txt'
```
{"message":"the token_id 1 vote will be added to Block 2"}
{"error":"the token_id 1 already voted"}
{"message":"the token_id 2 vote will be added to Block 2"}
{"message":"the token_id 3 vote will be added to Block 2"}
{"1":1,"2":1,"3":1}
{}
{"index":2,"message":"New Block Forged","previous_hash":"7f87e272dfe110e96a9e14dc3c835c8811a3391b71ff4c9ade2b00f2fb892df1","proof":63785,"votes":[{"selection":"Biden","token_id":1},{"selection":"Trump","token_id":2},{"selection":"Biden","token_id":3}]}
{"Biden":2,"Trump":1}
{"error":"the token_id 3 already voted"}
{"message":"the token_id 4 vote will be added to Block 3"}
{"message":"the token_id 5 vote will be added to Block 3"}
{"message":"the token_id 6 vote will be added to Block 3"}
{"message":"New nodes have been added","total_nodes":["127.0.0.1:5001"]}
{"message":"New nodes have been added","total_nodes":["127.0.0.1:5000"]}
{"error":"the token_id 3 already voted"}
{"error":"the token_id 6 already voted"}
{"message":"the token_id 7 vote will be added to Block 3"}
{"error":"the token_id 7 already voted"}
{"message":"the token_id 8 vote will be added to Block 3"}
{"message":"the token_id 9 vote will be added to Block 3"}
{"index":3,"message":"New Block Forged","previous_hash":"dea1b5741ed8b225f94196b032eb28d5ff90c3ccac19dfddb104507e982b696e","proof":15023,"votes":[{"selection":"Biden","token_id":4},{"selection":"Biden","token_id":5},{"selection":"Trump","token_id":6},{"selection":"Trump","token_id":7}]}
{"index":4,"message":"New Block Forged","previous_hash":"b1e92151d97a00cbc620cdc04c409d00e7ab1cee20d5a16cf17cd19c29af8efc","proof":2250,"votes":[{"selection":"Biden","token_id":8},{"selection":"Biden","token_id":9}]}
{"message":"Our chain was replaced","new_chain":[{"index":1,"previous_hash":"1","proof":100,"timestamp":1600829112.4173272,"votes":[]},{"index":2,"previous_hash":"7f87e272dfe110e96a9e14dc3c835c8811a3391b71ff4c9ade2b00f2fb892df1","proof":63785,"timestamp":1600829117.749363,"votes":[{"selection":"Biden","token_id":1},{"selection":"Trump","token_id":2},{"selection":"Biden","token_id":3}]},{"index":3,"previous_hash":"dea1b5741ed8b225f94196b032eb28d5ff90c3ccac19dfddb104507e982b696e","proof":15023,"timestamp":1600829117.8644311,"votes":[{"selection":"Biden","token_id":4},{"selection":"Biden","token_id":5},{"selection":"Trump","token_id":6},{"selection":"Trump","token_id":7}]},{"index":4,"previous_hash":"b1e92151d97a00cbc620cdc04c409d00e7ab1cee20d5a16cf17cd19c29af8efc","proof":2250,"timestamp":1600829117.8720303,"votes":[{"selection":"Biden","token_id":8},{"selection":"Biden","token_id":9}]}]}
{"chain":[{"index":1,"previous_hash":"1","proof":100,"timestamp":1600829112.4173272,"votes":[]},{"index":2,"previous_hash":"7f87e272dfe110e96a9e14dc3c835c8811a3391b71ff4c9ade2b00f2fb892df1","proof":63785,"timestamp":1600829117.749363,"votes":[{"selection":"Biden","token_id":1},{"selection":"Trump","token_id":2},{"selection":"Biden","token_id":3}]},{"index":3,"previous_hash":"dea1b5741ed8b225f94196b032eb28d5ff90c3ccac19dfddb104507e982b696e","proof":15023,"timestamp":1600829117.8644311,"votes":[{"selection":"Biden","token_id":4},{"selection":"Biden","token_id":5},{"selection":"Trump","token_id":6},{"selection":"Trump","token_id":7}]},{"index":4,"previous_hash":"b1e92151d97a00cbc620cdc04c409d00e7ab1cee20d5a16cf17cd19c29af8efc","proof":2250,"timestamp":1600829117.8720303,"votes":[{"selection":"Biden","token_id":8},{"selection":"Biden","token_id":9}]}],"message":"Our chain is authoritative"}
{"Biden":6,"Trump":3}
{"Biden":6,"Trump":3}
```
