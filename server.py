from logging import debug, error
from flask_app.controllers import users
from flask_app.controllers import orders
from flask_app import app

#@app.errorhandler(KeyError)
@app.errorhandler(404)
def page_not_found(error):
    return "Sorry! Page Not Available."

if __name__ == "__main__":
    app.run(debug=True)
