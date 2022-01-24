"""
This is a hello world plugin for DocumentCloud

It demonstrates how to write a plugin which can be activated from the
DocumentCloud plugin system and run using Github Actions.  It receives data
from DocumentCloud via the request dispatch and writes data back to
DocumentCloud using the standard API
"""

import json
import sys

import documentcloud


def load_params():
    """Load the parameters passed in to the GitHub Action"""
    params = json.loads(sys.argv[1])
    # token is a JWT to use to authenticate against the DocumentCloud API
    token = params["token"]
    # Documents is a list of document IDs which were selected to run with this
    # plugin activation
    documents = params["documents"]
    # data is any plugin specific data sent with this request
    data = params["data"]
    return token, documents, data


def init():
    """Load the paraneters and initialize the DocumentCloud client"""
    token, documents, data = load_params()
    client = documentcloud.DocumentCloud()
    client.session.headers.update({"Authorization": "Bearer {}".format(token)})
    return client, documents, data


def main(client, documents, data):
    """The main plugin functionality goes here"""
    # fetch your plugin specific data
    name = data.get("name", "world")

    # add a hello note to the first page of each selected document
    for doc_id in documents:
        document = client.documents.get(doc_id)
        document.annotations.create(f"Hello {name}!", 0)


if __name__ == "__main__":
    client, documents, data = init()
    main(client, documents, data)
