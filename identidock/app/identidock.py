from flask import Flask, Response, request
import requests
import redis


app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, db=0)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    name = 'jason'
    if request.method == 'POST':
        name = request.form['name']

    header = '<html><head><title>On Identidock</title></head><body>'
    body = '''<form method="POST">
			Hello <input type="text" name="name" value="{0}">
			<input type="submit" value="submit">
			</form>
			<p>You look like: 
			<img src="/monster/{1}"/></p>
			'''.format(name, name)
    footer = '</body></html>'

    return header + body + footer


@app.route('/monster/<name>')
def get_identicon(name):
    image = cache.get(name)
    if image is None:
        res = requests.get('http://dnmonster:8080/monster/' + name + '?size=80')
        image = res.content
        cache.set(name, image)
    else:
    	print('use redis.')

    return Response(image, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
