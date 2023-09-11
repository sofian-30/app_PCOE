# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 10:51:31 2021

@author: SEENOVATE
"""

import dash
import dash_bootstrap_components as dbc

# Pour le calendrier français dans les datepickers
scripts = [
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/dayjs.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/dayjs/1.10.8/locale/fr.min.js",
]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, "assets/sheet.css"],
                external_scripts=scripts)

# ---------- A modifier ----------------- #
app.title = "Seenovate Application Interne PCOE"
app._favicon = "logo_favicon.ico"
# ---------- A modifier ----------------- #
# server = app.server
app.config.suppress_callback_exceptions = True



