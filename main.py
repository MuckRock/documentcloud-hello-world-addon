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
    token = params.pop("token")
    # base_uri is the URI to make API calls to - allows the plugin to function
    # in non-production environments
    base_uri = params.pop("base_uri", None)
    # Documents is a list of document IDs which were selected to run with this
    # plugin activation
    documents = params.pop("documents")
    # params will contain add on specific data in 'data', and the user and org
    # IDs in 'user_id' and 'org_id'
    return token, base_uri, documents, params


def init():
    """Load the paraneters and initialize the DocumentCloud client"""
    token, base_uri, params = load_params()
    kwargs = {'base_uri': base_uri} if base_uri is not None else {}
    client = documentcloud.DocumentCloud(**kwargs)
    client.session.headers.update({"Authorization": "Bearer {}".format(token)})
    return client, documents, params


def main(client, documents, params):
    """The main plugin functionality goes here"""
    # fetch your plugin specific data
    name = params['data'].get("name", "world")

    # add a hello note to the first page of each selected document
    for doc_id in documents:
        document = client.documents.get(doc_id)
        document.annotations.create(f"Hello {name}!", 0)


if __name__ == "__main__":
    client, documents, params = init()
    main(client, documents, params)
