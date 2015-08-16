# !/usr/bin/env python
# -*- coding: UTF-8 -*-

import misaka
import redis
import random
import json
from flask import Flask, request, g, redirect

app = Flask(__name__)

service_name = "dataswarm"
version = "0.0.2"
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
social_mediatypes = ["mb", "bl", "cm", "md", "sc",
                     "vi", "wi", "ot", "rv", "cf"]
editorial_mediatypes = ["news"]


def parse_doc(data):
    try:
        valid_json = json.loads(data)
        doc_id = valid_json["id"]
        mediaType = valid_json["metaData"]["mediaType"]
    except Exception as e:
        print("Something went wrong:", e)

    if mediaType in social_mediatypes:
        doc_type = "social"
    elif mediaType in editorial_mediatypes:
        doc_type = "editorial"
    else:
        doc_type = "unknown"

    return doc_id, doc_type


@app.before_request
def before_request():
    g.r = redis.Redis(connection_pool=pool)


def post_doc(doc_id, doc_type, doc):
    # POST to db
    try:
        # Add document to db
        g.r.set(doc_id, doc)

        # Add doc_id to specific db set,
        # so we know the type of the doc
        g.r.sadd(doc_type, doc_id)
        g.r.bgsave()

        return '', 201
    except Exception as e:
        print("Something went wrong:", e)
        return '', 400


def delete_doc(doc_id):
    # DELETE from db
    try:
        # Get the doc and identify doc_type
        doc_type = json.loads(g.r.get(doc_id))["metaData"]["mediaType"]
        # Remove from db
        g.r.delete(doc_id)
        # Remove from db set
        g.r.srem(doc_type, doc_id)
        return '', 204
    except Exception as e:
        print("Something went wrong:", e)
        return '', 400


def get_doc(doc_id):
    # GET doc if exists, or 404
    try:
        return g.r.get(doc_id), 200
    except Exception as e:
        print("Something went wrong:", e)
        return '', 404


@app.route("/{0}/doc/<doc_id>".format(service_name), methods=['GET', 'DELETE'])
def editorial_doc(doc_id):
    # Handling of specific doc

    if request.method == 'DELETE':
        return delete_doc(doc_id)
    else:
        return get_doc(doc_id)


@app.route("/{0}/doc/editorial/".format(service_name))
def random_editorial():
    # From lists of editorial, choose one
    doc_id = random.choice(list(g.r.smembers("editorial")))
    return get_doc(doc_id)


@app.route("/{0}/doc/social/".format(service_name))
def random_social():
    # From lists of social, choose one
    doc_id = random.choice(list(g.r.smembers("social")))
    return get_doc(doc_id)


@app.route("/{0}/doc/".format(service_name), methods=['GET', 'POST'])
def post_or_random():
    if request.method == 'POST':
        data = request.data
        doc_id, doc_type = parse_doc(data)
        return post_doc(doc_id, doc_type, data)

    else:
        # From lists of social and editorial doc_ids, choose one
        doc_id = random.choice(
            list(g.r.smembers("social")) + list(g.r.smembers("editorial")))
        return get_doc(doc_id)


@app.route("/{0}/".format(service_name))
def doc():
    with open('README.md', 'r') as f:
        text = misaka.html(f.read())
    return text


@app.route("/{0}/_status".format(service_name))
def status():
    return '{{"version": "{0}","statusCode":"OK"}}'.format(version)


@app.route("/{0}/_health".format(service_name))
def health():
    return '{{"db_size": "{0}",'
    '"redis_version":"{1}"}}'.format(g.r.dbsize(), g.r.info()['redis_version'])


@app.route('/')
def redirect_to_doc():
    return redirect("/{0}/".format(service_name), code=302)

if __name__ == "__main__":
    app.run(debug=False)
