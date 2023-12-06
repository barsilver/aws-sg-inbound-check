from flask import Flask, request
import requests

app = Flask(__name__)

api_url = "https://official-joke-api.appspot.com/random_joke"
response = requests.get(api_url)
content = response.json()
punchline = content['punchline']
joke_id = content['id']

@app.route("/", methods=['GET'])
def joke():
    if request.method == 'GET':
        return'''
           The punchline value is: {}
           The id value is: {}'''.format(punchline, joke_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)