
# DocumentCloud Add-On Example

This repository contains an example Add-On for DocumentCloud.  It is designed
to be forked and modified to allow one to easily write Add-Ons to bring custom
functionality to DocumentCloud.

## Files

### addon.py

This file contains a base class `AddOn`, which implements shared functionality
for all DocumentCloud Add-Ons to use.  In most cases, you should not need to
edit this file.  You will subclass this class in `main.py`.

Upon initializing this class, it parses the JSON passed in as an argument, and populates a number of member variables.

* `client` - A DocumentCloud client.  This is a python library
  (https://github.com/MuckRock/python-documentcloud) allowing easy access to
  the DocumentCloud API.  It will be configured with the access token passed
  in, which gives you access to the API as the user who activated the Add-On
  for 5 minutes. (NOTE: we may need a way to pass in a refresh token if Add-Ons
  need to run for more than 5 minutes)

* `id` - a UUID to identify this run.  This is used to update progress, status
  and upload files for this particular run of the Add-On.  This will be `None`
  if called from the `test_addon.py` script.

* `documents` - A list of document IDs selected when the Add-On was activated

* `query` - The search query which was active when the Add-On was activated

* `user_id` - The user ID of the user who activated this run of the Add-On.

* `org_id` - The organization ID of the active organization of the user who
  activated this run of the Add-On.

* `data` - The Add-On specific data.

There are also some methods which provide useful functionality for an Add-On.

* `set_progress(self, progress)` - This takes a single integer argument between
  0 and 100 which represents the percent of progress the Add-On run has made,
  to inform the user of the progress.  As it takes some time to be shown to the
  user, this is primarily of use for long running Add-Ons.

* `set_message(self, message)` - Takes a string of max length 255 characters.
  This sets a status message to let the user know what the status of the Add-On
  run is. Similar to `set_progress`, it is mostly useful for long running
  Add-Ons.

* `upload_file(self, file)` - Takes a file object to attach to this Add-On run.
  This will be presented to the user for download.  This is useful for Add-Ons
  which want to return data such as a CSV file or other exports of data to the
  user.  It is currently limited to one file per run, so please ZIP your files
  if you need to return more than one.

* `send_mail(self, subject, content)` - This is used to email yourself at the
  email address associated with your DocumentCloud account.  This can be used
  to send a notification when an Add-On run is complete or just to send
  additional information to the user who ran the Add-On.  It takes two
  character strings, one for the subject and one for the body content of the
  email.  The content is plain text and does not currently support Markdown or
  HTML.

### main.py

This is the file to edit to implement your Add-On specific functionality.  You
should define a class which inherits from `AddOn` from `addon.py`.  Then you
can instantiate a new instance and call the main method, which is the entry
point for your Add-On logic.  You may access the data parsed by `AddOn` as well
as using the helper methods defined there.  The `HelloWorld` example Add-On
demonstrates using many of these features.

If you need to add more files, remember to instantiate the main Add-On class
from a file called `main.py` - that is what the GitHub action will call with
the Add-On parameters upon being dispatched.

### requirements.txt

This is a standard `pip` `requirements.txt` file.  It allows you to specify
python packages to be installed before running the Add-On.  You may add any
dependencies your Add-On has here.  By default we install the
`python-documentcloud` API library and the `requests` HTTP request package.

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

### .github/workflows/plugin.yml

This is the GitHub Actions configuration file.  We have a very simple workflow
defined, which sets up python, installes dependencies and runs the `main.py` to
start the Add-On.  It should not need to be edited in most cases, unless you
have an advanced use case.  If you do edit it, you should leave the first step
in place, which uses the UUID as its name, to allow DocumentCloud to identify
the run.

It would be possible to make a similar workflow for other programming languages
if one wanted to write Add-Ons in a language besides python.

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

* `id` - A UUID to uniquely identify this Add-On run.  It allows DocumentCloud
  to identify the run, as well as allowing the run to send back progress,
  status message and file updates.
