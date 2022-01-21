
import json
import sys

import requests

print("Hello world!")
params = json.loads(sys.argv[1])
requests.get(params["url"])
