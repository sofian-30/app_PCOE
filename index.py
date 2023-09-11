# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 10:52:41 2021

@author: SEENOVATE
"""

import os
from app import app
import callbacks
import dash_auth
from layout import layout_template
from appPCOE import callbacks_appPCOE
#from app2 import callbacks_app2
#from app3 import callbacks_app3
 

port = int(os.environ.get('PORT', 3000))
 

# Authentification par ID / Mdp, que l'on liste ici :
VALID_USERNAME_PASSWORD_PAIRS = {
    'template': 'Seenovate1234' ,
    '':''
}
 
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = layout_template 

if __name__ == '__main__':
    #if sys.platform.startswith('win32'): ?
    app.run_server(debug=True)
    #else:
     #   app.run_server(host='0.0.0.0', port=port)
