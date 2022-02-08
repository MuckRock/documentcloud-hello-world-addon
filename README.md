
# DocumentCloud Add-On Example

This repository contains an example Add-On for DocumentCloud.  It is designed
to be forked and modified to allow one to easily write Add-Ons to bring custom
functionality to DocumentCloud.

## Files

### main.py

This is the main Add-On file.  It contains three functions, `load_params`,
`init`, and `main`.  The first two are designed to not be modified.  They will
load the parameters passed in to the GitHub action and pass them to the `main`
function.  The `main` function is designed to be update on a per Add-On basis
with custom functionality.  The `main` function will be passed `client`,
`documents`, `query`, and `params`.

* `client` - A DocumentCloud client.  This is a python library
  (https://github.com/MuckRock/python-documentcloud) allowing easy access to
  the DocumentCloud API.  It will be configured with the access token passed
  in, which gives you access to the API as the user who activated the Add-On
  for 5 minutes.

* `documents` - A list of document IDs selected when the Add-On was activated

* `query` - The search query which was active when the Add-On was activated

* `params` - The rest of the parameters as a dictionary.  Add-On specific data
  is in "data", whil ethe user and organization IDs can be found in "user" and
  "organization".

Add-On specific data can be defined when registering the Add-On with
DocumentCloud.  It allows DocumentCloud to show an Add-On specific form for
collecting data when the Add-On is activated.

### test_addon.py

This is a test runner script, which will allow you to easily pass data in the
correct format into `main.py`, allowing you to run the Add-On locally, useful
for development purposes.  It requires your DocumentCloud username and
password, which is used to fetch an access token.  They can be passed in as
command line arguments (`--username` and `--password`), or in environment
variables (`DC_USERNAME` and `DC_PASSWORD`).

You can also pass in a list of document IDs (`--documents`), a search query
(`--query`), and JSON parameters for your Add-On (`--params`) - be sure to
properly quote your JSON at the command line.

Example invocation:
```
python test_addon.py --documents 123 --params '{"name": "World"}'
```

## Reference

### Full parameter reference

This is a reference of all of the data passed in to the Add-On.  A single JSON
object is passed in to `main.py` as a quoted string.  The `init` and
`load_params` functions parse this out and convert it to useful python objects
for your `main` function to use.  The following are the top level keys in the object.

* `token` - An access token which will be valid for 5 minutes, giving you API
  access authorized as the user who activated the plugin.  The `init` function
  uses this value to configure the DocumentCloud client object.

* `base_uri` - This can be used to point the API server to other instances,
  such as our internal staging server.  It should not be used unless you are
  running your own instance of DocumentCloud.  It is also used in the
  initialization of the DocumentCloud client.

*  `documents` - This is the list of Document IDs which is passed in to `main`

*  `query` - This is the search query which is passed in to `main`

*  `data` - This is the Add-On specific data, as defined when registering the
   Add-On with DocumentCloud.  It is passed in to `main` in the `params`
   dictionary under the key `data`

* `user` and `organization` - The user ID and organiation ID of the user who
  activated the Add-On.  They are also passed in to `main` through the `params`
  dictionary under the keys `user` and `organization` respectively.

* If more metadata is added in the future, it will automatically be passed in
  through the `params` dictionary.
