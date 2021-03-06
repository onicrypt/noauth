from os import getenv
from pprint import pformat
from time import time

from flask import Flask, request, redirect, session, url_for
from flask.json import jsonify
import requests
from requests_oauthlib import OAuth2Session

app = Flask(__name__)

# This information is obtained upon registration of a new Google OAuth
# application at https://code.google.com/apis/console
google_client_id = getenv('GOOGLE_CLIENT_ID') 
google_client_secret = getenv('GOOGLE_CLIENT_SECRET') 

google_client_id = getenv('LEAKY_CLIENT_ID') 
google_client_secret = getenv('LEAKY_CLIENT_SECRET') 

app_url ='http://ec2-52-8-68-137.us-west-1.compute.amazonaws.com:5000' 
redirect_uri = app_url + '/oauth2callback'
leaky_redirect_uri = app_url + '/leakycallback'
# Uncomment for detailed oauthlib logs
#import logging
#import sys
#log = logging.getLogger('oauthlib')
#log.addHandler(logging.StreamHandler(sys.stdout))
#log.setLevel(logging.DEBUG)

# OAuth endpoints given in the Google API documentation
google_auth_base_url = "https://accounts.google.com/o/oauth2/auth"
google_token_url = "https://accounts.google.com/o/oauth2/token"
refresh_url = google_token_url # True for Google but not all providers.
scope = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

@app.route("/oauth2/google")
def google_oauth():
    """Step 1: User Authorization for Google OAuth.
    """
    google = OAuth2Session(google_client_id, scope=scope, 
				redirect_uri=redirect_uri)
    authorization_url, state = google.authorization_url(google_auth_base_url,
        # offline for refresh token
        # force to always make user click authorize
        access_type="offline", approval_prompt="force")

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)

@app.route("/oauth2/leaky")
def leaky_oauth():
    """ Initial call to OAuth Provider for leaky auth code
    """
    google = OAuth2Session(google_client_id, scope=scope, 
				redirect_uri=leaky_redirect_uri)
    authorization_url, state = google.authorization_url(google_auth_base_url,
        # offline for refresh token
        # force to always make user click authorize
        access_type="offline", approval_prompt="force")

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/oauth2callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    google = OAuth2Session(google_client_id, redirect_uri=redirect_uri,
                           state=session.pop('oauth_state', None))

    token = google.fetch_token(google_token_url, 
				client_secret=google_client_secret,
				authorization_response=request.url)

    # We use the session as a simple DB for this example.
    session['oauth_token'] = token

    return redirect(url_for('.menu'))

@app.route("/leakycallback", methods=["GET"])
def leaky_callback():
    """ Oauth callback that leaks the auth code
    """
    google = OAuth2Session(google_client_id, redirect_uri=redirect_uri,
                           state=session.pop('oauth_state', None))
    token = google.fetch_token(google_token_url, 
				client_secret=google_client_secret, 
				authorization_response=request.url)

    # We use the session as a simple DB for this example.
    session['oauth_token'] = token

    return redirect(url_for('.code/leaky'))

@app.route("/menu", methods=["GET"])
def menu():
    """ """
    return """
    <h1>Congratulations, you have obtained an OAuth 2 token!</h1>
    <h2>What would you like to do next?</h2>
    <ul>
        <li><a href="/profile"> Get account profile</a></li>
        <li><a href="/implicit/leaky"> Implicit mode leaking auth code</a></li>
        <li><a href="/automatic_refresh"> Implicitly refresh the token</a></li>
        <li><a href="/manual_refresh"> Explicitly refresh the token</a></li>
        <li><a href="/validate"> Validate the token</a></li>
    </ul>
    <pre>
        %s
    </pre>
    """ % pformat(session['oauth_token'], indent=4)

@app.route("/code/leaky", methods=["GET","POST"])
def implicit_leaky():
    leaky_form = """<form id='leaky' method="POST">
                     <tr>
                         <td><label for='leaky-image'>Upload your images to our kitchen sink</td>
                         <td><input name='leaky-image' type='text'></td>
                     </tr>
                     <tr>
                         <td><input name='upload' type='submit' value='Upload'></td>
                     </tr>
                     </form>
                 """
    if(request.method == "GET"):
        return leaky_form
    elif(request.method == "POST"):
        return leaky_form + request.form['leaky-image']
    else:
        return """Wrong method jackhole"""


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    google = OAuth2Session(google_client_id, token=session.pop('oauth_token', None))
    user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    return jsonify(google.get(user_info_url).json())


@app.route("/automatic_refresh", methods=["GET"])
def automatic_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    # We force an expiration by setting expired at in the past.
    # This will trigger an automatic refresh next time we interact with
    # Googles API.
    token['expires_at'] = time() - 10

    extra = {
        'client_id': google_client_id,
        'client_secret': google_client_secret,
    }

    def token_updater(token):
        session['oauth_token'] = token

    google = OAuth2Session(google_client_id,
                           token=token,
                           auto_refresh_kwargs=extra,
                           auto_refresh_url=refresh_url,
                           token_updater=token_updater)

    # Trigger the automatic refresh
    jsonify(google.get('https://www.googleapis.com/oauth2/v1/userinfo').json())
    return jsonify(session['oauth_token'])


@app.route("/manual_refresh", methods=["GET"])
def manual_refresh():
    """Refreshing an OAuth 2 token using a refresh token.
    """
    token = session['oauth_token']

    extra = {
        'client_id': google_client_id,
        'client_secret': google_client_secret,
    }

    google = OAuth2Session(google_client_id, token=token)
    session['oauth_token'] = google.refresh_token(refresh_url, **extra)
    return jsonify(session['oauth_token'])

@app.route("/validate", methods=["GET"])
def validate():
    """Validate a token with the OAuth provider Google.
    """
    token = session['oauth_token']

    # Defined at https://developers.google.com/accounts/docs/OAuth2LoginV1#validatingtoken
    validate_url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?'
                    'access_token=%s' % token['access_token'])

    # No OAuth2Session is needed, just a plain GET request
    return jsonify(requests.get(validate_url).json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    import os
    os.environ['DEBUG'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True, host='0.0.0.0')
