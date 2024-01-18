from dash import html,dash_table,dcc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
from apps import dbconnect as db
from apps import commonmodule as cm

layout=html.Div([
    html.Video(src="./assets/appsor.mp4", className="video", muted=True, width="100%", loop=True, autoPlay=True),
        html.Div([
                html.Div([
                        html.H1("LOGIN", 
                                style={
                                    "font-family":"Arial",
                                    "text-align":"center"
                                }),
                        dcc.Input(id='uname', type='text', className='input', placeholder='Username'),
                        dcc.Input(type='password', id='pword', className='input', placeholder='Password'),
                        html.H4(id='errormessage', className='error'),
                        html.Button('Log In', id='submit-val', className='loginbutton', n_clicks=0),

                ],className='half left'),
                
                html.Div([
                    html.Img(src="./assets/announcement.jpg", style={"position":"absolute", "max-height":"100%"})
                ],className='half')
            ],className='flex login-module')
        ],className='FullScreen')    

@app.callback(
    [Output('errormessage','children'),Output('login-auth','data')],
    [Input('submit-val','n_clicks')],
    [State('uname','value'),State('pword','value')]
)
def try_log(submit,uname,pword):
    if submit>0: 
                    print('This is triggered')
                    sql="SELECT account_password FROM user_account WHERE user_name="
                    if uname:
                        sql+="'"+uname+"'"
                    else:
                        sql+='0'
                    print(sql)
                    values=[]
                    cols=['pass']
                    df = db.querydatafromdatabase(sql, values, cols)
                    if df.shape[0]:
                        if (df['pass'][0]==pword):
                            print('authenticated')
                            return dash.no_update,{'isAuthenticated':True,'acc':uname}
                        else:
                            return ["Account or Password mismatch"],dash.no_update
    raise PreventUpdate
                