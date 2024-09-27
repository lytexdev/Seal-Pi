from flask import Flask, render_template, Response
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.after_request
def add_header(response):
    response.headers['X-Robots-Tag'] = 'noindex, nofollow'
    return response


@app.route('/robots.txt')
def robots_txt():
    try:
        return Response("User-agent: *\nDisallow: /", mimetype="text/plain")
    except Exception as e:
        app.logger.error(f"Error generating robots.txt: {str(e)}")
        return Response("Error generating robots.txt", status=500)    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
