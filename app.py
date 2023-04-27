from flask import Flask, url_for, session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
from py_console import console

app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')

oauth = OAuth(app)
oauth.register(
    name='actionstep',
    access_token_url='https://api.actionstepstaging.com/api/oauth/token',
    authorize_url='https://go.actionstepstaging.com/api/oauth/authorize',
    client_kwargs={
        'scope': 'actions',
    }
)


@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)


@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return oauth.actionstep.authorize_redirect(redirect_uri)


@app.route('/auth')
def auth():
    token = oauth.actionstep.authorize_access_token()
    console.log(token)
    session['user'] = token
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
