curl http://127.0.0.1:5000/vote -X POST -d '{"token_id":1,"selection":"Biden"}' -H "content-type: application/json"
curl http://127.0.0.1:5000/vote -X POST -d '{"token_id":1,"selection":"Trump"}' -H "content-type: application/json"
curl http://127.0.0.1:5000/vote -X POST -d '{"token_id":2,"selection":"Trump"}' -H "content-type: application/json"
curl http://127.0.0.1:5000/vote -X POST -d '{"token_id":3,"selection":"Biden"}' -H "content-type: application/json"
curl http://127.0.0.1:5000/token_id
curl http://127.0.0.1:5000/view_vote
curl http://127.0.0.1:5000/store
curl http://127.0.0.1:5000/view_vote
curl http://127.0.0.1:5000/vote -X POST -d '{"token_id":3,"selection":"Trump"}' -H "content-type: application/json"
curl http://127.0.0.1:5000/vote -X POST -d '{"token_id":4,"selection":"Biden"}' -H "content-type: application/json"
curl http://127.0.0.1:5000/vote -X POST -d '{"token_id":5,"selection":"Biden"}' -H "content-type: application/json"
curl http://127.0.0.1:5000/vote -X POST -d '{"token_id":6,"selection":"Trump"}' -H "content-type: application/json"
curl http://127.0.0.1:5000/nodes/register -X POST -H "content-type: application/json" -d '{"nodes":["http://127.0.0.1:5001"]}'
curl http://127.0.0.1:5001/nodes/register -X POST -H "content-type: application/json" -d '{"nodes":["http://127.0.0.1:5000"]}'
curl http://127.0.0.1:5001/vote -X POST -d '{"token_id":3,"selection":"Biden"}' -H "content-type: application/json"
curl http://127.0.0.1:5001/vote -X POST -d '{"token_id":6,"selection":"Trump"}' -H "content-type: application/json"
curl http://127.0.0.1:5000/vote -X POST -d '{"token_id":7,"selection":"Trump"}' -H "content-type: application/json"
curl http://127.0.0.1:5001/vote -X POST -d '{"token_id":7,"selection":"Biden"}' -H "content-type: application/json"
curl http://127.0.0.1:5001/vote -X POST -d '{"token_id":8,"selection":"Biden"}' -H "content-type: application/json"
curl http://127.0.0.1:5001/vote -X POST -d '{"token_id":9,"selection":"Biden"}' -H "content-type: application/json"
curl http://127.0.0.1:5000/store
curl http://127.0.0.1:5001/store
curl http://127.0.0.1:5000/sync
curl http://127.0.0.1:5001/sync
curl http://127.0.0.1:5000/view_vote
curl http://127.0.0.1:5001/view_vote
