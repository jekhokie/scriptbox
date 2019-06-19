import os
from flask import Flask, render_template, g, redirect, url_for
from flask_oidc import OpenIDConnect
import socket
import yaml

# load configuration settings
with open('config/settings.yml', 'r') as yml:
  config = yaml.load(yml)

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': config['oidc_secret_key'],
    'OIDC_CLIENT_SECRETS': 'config/client_secrets.json',
    'OIDC_TOKEN_COOKIE_NAME': config['oidc_token_cookie_name'],
    'OIDC_ID_TOKEN_COOKIE_SECURE': config['oidc_id_token_cookie_secure'],
    'OIDC_REQUIRE_VERIFIED_EMAIL': config['oidc_require_verified_email'],
    'OIDC_USER_INFO_ENABLED': config['oidc_user_info_enabled'],
    'OIDC_OPENID_REALM': config['oidc_openid_realm'],
    'OIDC_INTROSPECTION_AUTH_METHOD': config['oidc_introspection_auth_method']
})

oidc = OpenIDConnect(app)

@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = oidc.user_getinfo(['email_verified', 'name', 'preferred_username', 'given_name', 'family_name', 'email', 'sub'])
    else:
        g.user = None

@app.route('/')
def index():
    return render_template("index.html.j2", hostname=socket.gethostname())

@app.route('/dashboard')
@oidc.require_login
def dashboard():
    return render_template("dashboard.html.j2")

@app.route('/login')
@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))

@app.route('/logout')
def logout():
    oidc.logout()
    return redirect(url_for(".index"))
