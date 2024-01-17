import webbrowser

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime
# Importing your app definition from app.py so we can use it
from app import app
from apps import commonmodule as cm
from pages import home,alumni,changepassword, generatereport,managers,members,reaffiliate,updatealum,updatemember,login,updatemem
from pages import reaffiliate
dcc_store=dcc.Store(id='auth', data={'isAuthenticated':False,'acc':"-1"},storage_type='session')
dcc_loginstore=dcc.Store(id='login-auth',modified_timestamp=-1)
dcc_logoutstore=dcc.Store(id='logout-auth',modified_timestamp=-1)
app.layout = html.Div(
    [       
            dcc_logoutstore,
            dcc_loginstore,
            dcc_store,
            dcc.Location(id='url', refresh=True),
            #cm.navbar,
           
            html.Div(
                id='page-content'
            ),
    ],
)

@app.callback(
    [
        
        Output('page-content', 'children'),
        Output('url','pathname')
    ],
    [
        
        Input('auth','modified_timestamp'),
        Input('url', 'pathname'),
    ],
    [State('auth','data')]
)
def displaypage (timestamp,pathname,data):
    print('current data in display->', data)
    ctx = dash.callback_context
    if ctx.triggered:
        eventids = ctx.triggered
        for eventidmore in eventids:
            eventid=eventidmore['prop_id'].split('.')[0]
            if eventid == 'url':
                if data['isAuthenticated']:
                    if pathname=='/logout':
                        return [login.layout],'/login'
                    if pathname == '/' or pathname == '/home':
                        pathname='/home'
                        returnlayout = home.layout
                    elif pathname=="/change-password":
                        returnlayout=changepassword.layout
                    # elif pathname=="/edit-profile":
                    #     returnlayout=reaffiliate.layout
                    elif pathname=="/generate-report":
                        returnlayout=generatereport.layout
                    elif pathname=="/managers":
                        pathname="/managers"
                        returnlayout=managers.layout
                    elif pathname=="/members":
                        returnlayout=members.layout
                    elif pathname=="/reaffiliate":
                        returnlayout=reaffiliate.layout
                    elif pathname=="/update-alumni":
                        returnlayout=updatealum.layout
                    elif pathname=="/update-member":
                        returnlayout=updatemember.layout
                    elif pathname=="/alumni":
                        returnlayout=alumni.layout
                    elif pathname=='/update-member-modify':
                        returnlayout=updatemem.layout
                    else:
                        returnlayout = 'error404'
                    return returnlayout,pathname
                else:
                    return [login.layout],'/login'
            elif data['isAuthenticated'] and pathname=='/login':
                    return dash.no_update,'/home'
            elif not data['isAuthenticated']:
                    return [login.layout],'/login'
            else:
                PreventUpdate
    else:
        raise PreventUpdate
@app.callback(
    [Output('auth','data'),Output('login-auth','modified_timestamp'),Output('logout-auth','modified_timestamp')],
    [Input('login-auth','modified_timestamp'),Input('logout-auth','modified_timestamp')],
    [State('login-auth','data'),State('logout-auth','data'),State('auth','data')]
)
def update_cache(in_ts,out_ts,in_data,out_data,data):
    
    print("in updating data:",dash.callback_context.triggered,"date->",datetime.now())
    print('current data->',data)
    print("-----------------")
    if out_ts>0 and out_data:
        print('logging out')
        return out_data,-1,-1
    elif in_ts>0 and in_data:
        print('logging in')
        return in_data,-1,-1
    raise PreventUpdate
    
@app.callback(
    Output('logout-auth','data'),
    Input('lo','n_clicks')
)
def logout_session(loc):
    if loc>0:
        return {'isAuthenticated':False,'acc':"-1"}
if __name__ == '__main__':
    
    app.run_server(debug=True)