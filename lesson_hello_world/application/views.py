from application import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World... again 2"
