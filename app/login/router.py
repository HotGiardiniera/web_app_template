from flask import Blueprint

login_router = Blueprint('login', __name__, template_folder='templates', url_prefix='/login')