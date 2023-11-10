from flask import Blueprint, render_template, redirect, session, request, url_for
import google_auth_oauthlib.flow


from app.settings import settings
from app.signup.utils import hash_pw

settings = settings()
signup_router = Blueprint('signup', __name__, template_folder='templates', url_prefix='/signup')


@signup_router.route('/', methods=('GET',))
def get_signup():
    return render_template(
        'signup.html'
    )


@signup_router.route('/', methods=('POST',))
def post_signup():
    print(hash_pw(request.form['password']))
    return redirect(url_for('home'))


@signup_router.route('/google', methods=('GET',))
def test():
    # TODO the below is mainly Google code examples
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        {
          "web": {
            "client_id": settings.google_oauth_client_id,
            "client_secret": settings.google_oauth_client_secret,
            "redirect_uris": ["http://localhost:5002/signup/goauth_callback"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token"
          }
        },
        scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = 'http://localhost:5002/signup/goauth_callback'

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        state="Chris-trying-to-login",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    session["state"] = state
    return redirect(authorization_url)


@signup_router.route('/goauth_callback', methods=('GET',))
def oauth_callback():
    state = request.args['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        {
          "web": {
            "client_id": settings.google_oauth_client_id,
            "client_secret": settings.google_oauth_client_secret,
            "redirect_uris": ["http://localhost:5002/signup/goauth_callback"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token"
          }
        },
        scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'],
        state=state)
    flow.redirect_uri = "https://localhost:5002/signup/goauth_callback"

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials
    # TODO create DB or ffetch

    return render_template(
        "test.html",
        test="CHRIS CALL BACK",
    )
