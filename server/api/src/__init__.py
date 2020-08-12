from flask import Flask, g, request, Response
from flask_restful import Api
from flask_cors import CORS, cross_origin
import psycopg2
import time
import sys
import signal
from src.routes.index import Index
from src.routes.graph import generate_graph
from src.routes.prereqs import api_get_all_prereqs
from src.routes.course import get_course_info
from src.routes.search import search_courses
from src.routes.relationship import get_course_relationship
from src.routes.vote import like, dislike, unlike, undislike

app = Flask(__name__)
# Access-Control-Allow-Origin header
CORS(app)
# api = Api(app)

# could go in separate file
def connect_to_db():
    connection = psycopg2.connect("") # "" to use env vars
    return connection

def get_db():
    if not hasattr(g, 'postgres_db'):
        g.postgres_db = connect_to_db()
    return g.postgres_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'postgres_db'):
        g.postgres_db.close()

@app.route('/')
def index():
    return "hi"

@app.route('/graph', methods=['GET'])
def graph():
    return generate_graph(get_db())

@app.route('/prereqs', methods=['GET'])
def prereqs():
    return api_get_all_prereqs(get_db())

@app.route('/course/<string:course>', methods=['GET'])
def api_course(course):
    return get_course_info(get_db(), course)

@app.route('/search', methods=['GET'])
def search_keyword():
    phrase = request.args.get("phrase").split(',')
    return search_courses(get_db(), phrase)

@app.route('/relationship/<string:course_a>/<string:course_b>', methods=['GET'])
def relationship(course_a, course_b):
    return get_course_relationship(get_db(), course_a, course_b)

@app.route('/vote', methods=['PUT'])
def vote_on_relationship():
    body = request.get_json()
    keys = ('course_a', 'course_b', 'action')
    if any(i not in body for i in keys):
        return Response("Body requires JSON with 'course_a'/'course_b'/'action' keys.", status=400)
    if any(not isinstance(i, str) for i in keys):
        return Response("keys must all be str value", 400)

    a = body['course_a']
    b = body['course_b']
    if body['action'] == 'like':
        like(get_db(), a, b)
    elif body['action'] == 'dislike':
        dislike(get_db(), a, b)
    elif body['action'] == 'unlike':
        unlike(get_db(), a, b)
    elif body['action'] == 'undislike':
        undislike(get_db(), a, b)
    else:
        return Response("'action' must be either 'like'/'dislike'/'unlike'/'undislike'", 400)
    return Response("success", 202)
        