import dash
from dash.dependencies import Input, Output, State
from dash import html,dcc
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db
from apps import commonmodule as cm

modal=html.Div([
    html.Label(className='hidden modal-background',id='cp-bg'),
    html.Div([
        html.Div(
            [html.H3("Sucess")],className='modal-header',id='mh'
        ),
        html.P("Password Changed Successfully",id='m-con'),
        html.A([html.Button("Proceed",className='enter', id='pw-btn')],href='/change-password')
    ],className='hidden modal',id='cp-main')
])

head_style = {
    "font-family": "Arial",
    "color": "#273250",
        }

pass_style = {
    "font-weight":"bold",
    "font-family": "Arial, Helvetica, sans-serif",
    "font-size":"0.9em",
}


layout=html.Div(
    [
        cm.top,
        html.Div([
            cm.navigationpanel,
        html.Div([
    modal,
    html.H2("Change Password", style=head_style),
    html.Div([
        dcc.Store(id='cur-pass', data={}),
        html.Label("Current Password:", style=pass_style), dcc.Input(type='password',id='cpw', placeholder="Type Current Password"),
        html.Br(),
        html.Label("New Password:",style=pass_style), dcc.Input(type='password',id='npw',placeholder="Type New Password"),
        html.Button("Change Password",id='change-pw',className='choice',n_clicks=0)
    ],className='flex row',)
],className="body")
        ],className='flex container', style={"align-items":"block"})
    ]
)
@app.callback(
[
Output('cur-pass', 'data')
],
[
Input('url', 'pathname'),
],
[
    State('auth','data')
]
)
def update_pass(pathname,data):
    if pathname=="/change-password":
        sql="SELECT account_password FROM user_account WHERE user_name=""'"+data['acc']+"'"
        values=[]
        cols=['pw']
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0]:
            return [{'cpw':df['pw'][0]}]
    print("anything")
    raise PreventUpdate
@app.callback(
    [
        Output('cp-bg','className'),
        Output('cp-main','className'),
        Output('mh','className'),
        Output('pw-btn','className'),
        Output('mh','children'),
        Output('m-con','children'),

    ],
    [
        Input('change-pw','n_clicks')
    ],
    [
        State('cur-pass','data'),
        State('cpw','value'),
        State('npw','value'),
        State('auth','data')
    ]
)
def change_pass(click,data,cur_pw,new_pw,accdata):
    if click>0:
        if data['cpw']==cur_pw:
            sql="UPDATE user_account SET account_password=%s WHERE user_name=""'"+accdata['acc']+"'"
            values=[new_pw]
            db.modifydatabase(sql,values)
            return 'shown modal-background','shown modal', dash.no_update,dash.no_update,dash.no_update,dash.no_update
        else:
            return 'shown modal-background','shown modal','red-modal','red-btn',"Warning",["Current Password Mismatch"]
    raise PreventUpdate