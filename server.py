from os import environ
from flask import Flask

app = Flask(__name__)
app.run(host='0.0.0.0', port=8080)
#app.run(environ.get('PORT'))

@app.route("/")
def helloworld():
    return 'Hello P'
