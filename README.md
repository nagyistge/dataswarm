# Dataswarm

Providing test-data as a service, with redis.

## Usage

To start Dataswarm:

1. Install depencencies: `sudo pip install requirements.txt`

2. Start the web server by: `python dataswarm.py`

Now you can visit `localhost:5000/dataswarm/doc/` etc.

### Examples

    To get random doc:

    % curl -X GET localhost:5000/dataswarm/doc/

    To get random of specific type:

    % curl -X GET localhost:5000/dataswarm/doc/editorial/

    % curl -X GET localhost:5000/dataswarm/doc/social/

    To add a doc:

    % curl -X POST -H "Content-Type: application/json" -d@ file_name http://localhost:5000/dataswarm/doc/

    To add many documents:

    % for file in *quiddity.json; do curl -iLX POST -H "Content-Type: application/json" -d@$file http://localhost:5000/dataswarm/doc/; sleep 0.5; done

    To get, or delete, a specific doc:

    % curl -X GET localhost:5000/dataswarm/doc/gWoH_EmEVKnnmpB9shwfBT4Sa28

    % curl -X DELETE http://localhost:5000/dataswarm/doc/iIYcdfGa-EIiBo6MEVPwdGLF3W4


## All endpoints

`/doc/`

GET gives a random document

POST to add document to db

`/doc/editorial`

Gives a random editorial document

`/doc/social`

Gives a random social document

`/doc/{doc_id}`

For a specific document.

Valid methods are: GET, and DELETE

`/`

Exposes this README.md file

`/_status`

Simple status endpoint

`/_health`

Essential info on the backend
