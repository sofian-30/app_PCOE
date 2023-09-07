from dash import Dash
import flask

################## Server Infos ########################
server = flask.Flask(__name__) # define flask app.server
#app = Dash(external_stylesheets=[dbc.themes.CERULEAN])
app = Dash(__name__,server=server, url_base_pathname="/", external_scripts=scripts, use_pages=True,suppress_callback_exceptions=True)
server = app.server

