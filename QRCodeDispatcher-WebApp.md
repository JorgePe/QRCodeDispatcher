# QRCode Dispatcher - The Frontend Component

# Intro

This implements a web app to be hosted in a public site.

Visitors that want to see activate one of my models
will point their smartphone or tablet to a QR Code that
points to a URL served by this app.

When this URL is reached the web app publishes a message
on a public MQTT broker.

For example my animated OWL will have a QR Code near by
that points to:

```
https://myaccountname.pythonanywhere.com/publish?OWL
```

So when someone uses that QR Code the web app just parses
the 'OWL' value and publishes a MQTT message with
'OWL' as payload and then redirects the visitor
for the main page where it can find some information about
the models being shown.

Just for convenience the main page ('index.html') also
shows a list of all models available to control so
one can use a convencional browser instead. This page
can also be extended with aditional information about
each model (like a photo or a video).

# Implementation

I'm using PythonAnywhere.com to host my web app.
It's a very small app made in flask, a python-based
web server.

First we creat a python virtual environment:

```
python3 --version
Python 3.10.5

python3 -m venv qrcode/
source qrcode/bin/activate
(qrcode) ~ $
```

then we install the required libraries ('flask' for the
web server and 'paho-mqtt' for message queing communications)

```
pip install flask
pip install paho-mqtt
```

We also need to create a folder for the html files rendered by the
web app:

```
mkdir templates
```

Then on the PythonAnywhere dashboard we create a new web app:

+ Add a new web app
- myaccountname.pythonanywhere.com
- Manual configuration
- Python version: Python 3.10

+ Enter a path to a virtualenv if desired
- /home/myaccountname/qrcode

Then we upload the required files:
- 'app.py' to the main folder
- 'index.html' and 'message.html' to the 'templates' folder

And finally we edit the WSGI configuration file, 
deleting the HELLO WORLD part at the beggining of the fileno inicio
and adding this lines at the flask part:

```
import sys
path = '/home/myaccountname/app.py'
if path not in sys.path:
   sys.path.append(path)

from app import app as application
```

When saving this file a yellow triangle will appear at the line edited,
we can safely ignore it.

To apply all these changes we need to press 'Reload'. After this our web app
should be running at

https://myaccountname.pythonanyhwere.com/

and we can publish a message using this URL:

https://myaccountname.pythonanyhwere.com/publish?OWL

You can use any MQTT client like MQTT Explorer to subscribe to the chosen
topic (i.e. '/QRCodeDispatcher/message') and confirm that the messages are
being published.

You can also use any MQTT client to publish to the same topic so you can
test your middleware even if you don't have the web app frontend available.
