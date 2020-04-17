#!/usr/bin/python3
import flask
import flask_login as fl
import python.backend as backend
import python.user as user
import argparse

app = flask.Flask("serien-ampel")
app.secret_key             = 'super secret key'

app.config['SESSION_TYPE']    = 'filesystem'
app.config['REDIRECT_BASE']   = "/"
app.config["ENFORCE_COMPLETE"] = False

loginManager = fl.LoginManager()
SEPERATOR = ","
TITLE = "Serienampel"

@app.route('/')
def rootPage():
    print(fl.current_user)

    return flask.render_template("home.html")

@app.route('/static/<path:path>')
def staticFiles():
    send_from_directory('static', path)

@app.route('/defaultFavicon.ico')
def icon():
    return app.send_static_file('defaultFavicon.ico')


##### USER SESSION MANAGEMENT #####
@loginManager.user_loader
def load_user(userName):
    return user.getUserFromDB(userName)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']
        if username in user.userDB and password == user.userDB[username].password:
            fl.login_user(user.User(username))
            return flask.redirect(app.config["REDIRECT_BASE"])
        else:
            return flask.abort(401)
    else:
        return flask.render_template('login.html', navbar=navbar, footer=footer, header=header)

@app.route("/logout")
@fl.login_required
def logout():
    fl.logout_user()
    return flask.redirect(app.config["REDIRECT_BASE"])

if __name__ == "__main__":

    parser  = argparse.ArgumentParser(description="Mobile Script Execution", \
                                        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-i", "--interface",  default="0.0.0.0", help="Interface to listen on")
    parser.add_argument("-p", "--port",       default="5000",    help="Port to listen on")
    parser.add_argument("-s", "--servername",       help="External hostname (i.e. serienampel.de)")
    args = parser.parse_args()
    if args.servername:
        app.config['REDIRECT_BASE']  = args.servername + "/"
    app.config["ENFORCE_COMPLETE"] = args.enforce_complete

    app.run(host=args.interface, port=args.port)
