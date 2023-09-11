# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 17:10:03 2021

@author: SEENOVATE
"""

from app import app
from appPCOE.layout import layout_PCOE
#from app2.layout import layout_app2
#from app3.layout import layout_app3
from layout import home_page
from dash.dependencies import Input, Output, State


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





