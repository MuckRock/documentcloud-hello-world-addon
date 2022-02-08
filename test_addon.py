"""
This is a test harness to run your DocumentCloud add-ons from the command line
for development purposes.
"""

import argparse
import json
import os

import documentcloud


def arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Test a DocumentCloud add on")
    parser.add_argument(
        "--username",
        help="DocumentCloud username - "
        "can also be passed in environment variable DC_USERNAME",
    )
    parser.add_argument(
        "--password",
        help="DocumentCloud password - "
        "can also be passed in environment variable DC_PASSWORD",
    )
    parser.add_argument("--documents", type=int, nargs="+", help="Document IDs")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--params", help="Parameter JSON")
    parser.add_argument("--staging", action="store_true", help="Use the staging site")
    args = parser.parse_args()
    username = args.username if args.username else os.environ.get("DC_USERNAME")
    password = args.password if args.password else os.environ.get("DC_PASSWORD")
    if args.staging:
        base_uri = "https://api.staging.documentcloud.org/api/"
        auth_uri = "https://squarelet-staging.herokuapp.com/api/"
    else:
        base_uri = "https://api.www.documentcloud.org/api/"
        auth_uri = "https://accounts.muckrock.com/api/"
    return username, password, base_uri, auth_uri, args


def test():
    """Run the Add On locally"""
    username, password, base_uri, auth_uri, args = arguments()
    client = documentcloud.DocumentCloud(
        username=username,
        password=password,
        base_uri=base_uri,
        auth_uri=auth_uri,
    )
    user = client.users.get("me")
    access_token = client._get_tokens(client.username, client.password)[0]
    payload = json.dumps(
        {
            "token": access_token,
            "base_uri": client.base_uri,
            "documents": args.documents,
            "query": args.query,
            "user": user.id,
            "organization": user.organization,
            "data": json.loads(args.params),
        }
    )

    os.system(f"python main.py '{payload}'")


if __name__ == "__main__":
    test()
