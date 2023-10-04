# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:10:03 2021

@author: SEENOVATE
"""

from dash.dependencies import Input, Output, State

from app import app
from appPCOE.layout import layout_PCOE
from layout import home_page


@app.callback(
    Output('page-content', 'children'),
    [Input('url2', 'pathname')],
    [State('page-content', 'children')]
)
def display_page(pathname, content):
    if pathname == '/':
        content = home_page
    elif pathname == '/appPCOE':
        content = layout_PCOE
    else:
        pass
    return content
