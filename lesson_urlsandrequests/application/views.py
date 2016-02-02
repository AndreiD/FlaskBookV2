from application import app, logger
from flask import render_template, request, make_response, abort
import json


@app.route('/')
@app.route('/index')
def index():
    print "this is a simple debug message"
    return render_template("index.html")


@app.route('/a_post_example', methods=["GET", "POST"])
def functions_names_must_be_unique():
    if request.method == 'POST':
        return "you made a POST request"

    # this is an example how to use logger
    logger.warning("warning! you make a GET REQUEST!")
    return "you made a GET request"


# Test this with: http://46.101.210.246:1337/get_example?search=Who am I?
# Test this with: http://46.101.210.246:1337/get_example [what error you see? why ?]
# Test by sending a POST to: http://46.101.210.246:1337/get_example [what error you see? why ?]
@app.route('/get_example')
def testing_get():
    if request.method == 'POST':
        # this will never get triggered because you didn't specify the POST method in the @app.route
        return "never going to show"

    if 'search' not in request.args:
        logger.error("you forgot to pass the search args")
        return "failed."

    search = request.args.get("search")
    logger.info("the search variable is  = " + search)
    return "you made a GET request with a parameter search = " + search


# http://46.101.210.246:1337/get_example_2
# http://46.101.210.246:1337/get_example_2/Tom Sawyer
@app.route('/get_example_2')
@app.route('/get_example_2/<username>')
def testing_get_2(username="Bob Smith"):
    logger.debug("the username variable is = " + username)
    return "you made a GET request with a username = " + username


# GET http://46.101.210.246:1337/post_example [why you see the error ?]
# POST http://46.101.210.246:1337/post_example with no parameters. you get a 400 bad request.
# POST http://46.101.210.246:1337/post_example with the parameters in BODY as form-data!
@app.route('/post_example', methods=["POST"])
def testing_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return "you made a post request with username=" + username + " and password=" + password

    return "this will never get called"


# GET http://46.101.210.246:1337/post_and_get
# GET http://46.101.210.246:1337/post_and_get?job=flask%20rockstar%20programmer
# GET http://46.101.210.246:1337/post_and_get?job=flask%20rockstar%20programmer
# POST http://46.101.210.246:1337/post_and_get
# POST http://46.101.210.246:1337/post_and_get?job=flask%20rockstar%20programmer
@app.route('/post_and_get', methods=["GET", "POST"])
def post_and_get():
    data = {}

    data['job'] = "jobless"
    if 'job' in request.args:
        data['job'] = request.args["job"]

    if request.method == 'POST':
        username = request.form['username']
        age = request.form['age']

        data['username'] = username
        data['age'] = age

    return render_template("another_template.html", data=data)


# POST http://46.101.210.246:1337/json_example (no json sent). what error you see ?
# POST http://46.101.210.246:1337/json_example | in postman select body, select "raw",  write {"username":"andrei","age":99, "status":true}
@app.route('/json_example', methods=["POST"])
def testing_json():
    # do we need to check if the request is POST ? no, because we already specified it in the methods
    data = request.data

    try:
        dataDict = json.loads(data)
    except ValueError, ex:
        logger.warning("Are you sending a json file ? " + str(ex))
        abort(404)

    return str(dataDict)
