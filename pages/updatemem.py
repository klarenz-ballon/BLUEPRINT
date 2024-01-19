from dash import html,dash_table,dcc
import dash
import urllib.parse
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
from apps import dbconnect as db
from apps import commonmodule as cm
modal=html.Div([
    html.Label(className='hidden modal-background',id='modal-background'),
    html.Div([
        html.Div(
            [html.H3("Action Done",style={"font-family": "Arial"})],className='modal-header'
        ),
        html.P("Said Action is Made",id='up-mem-done'),
        html.A([html.Button("Back to List",className='enter')],href='/update-member')
    ],className='hidden modal',id='main-modal')
])
layout=html.Div([
    cm.top,
    html.Div(
        [
            cm.navigationpanel,
            html.Div([modal,
    html.H2("Update Member Status",style={"font-family": "Arial", "color": "#273250",
        }),
    html.Div(id='mem-info',children=[
        html.Div([html.Div([html.H3('Full Name:  ',style={"font-family": "Arial"}),
        html.H3(id='fullname',style={'font-weight':'normal',"font-family": "Arial","margin-left":"0.3em"}),],className='flex half'),
        html.Div([html.H3('ID:  ',style={"font-family": "Arial"}),
        html.H3(id='mem-id-up',style={'font-weight':'normal',"font-family": "Arial","margin-left":"0.3em"}),],className='flex half'),
        html.Div([html.H3('Membership Status:  ',style={"font-family": "Arial"}),
        html.H3(id='up-mem-status',style={'font-weight':'normal',"font-family": "Arial","margin-left":"0.3em"}),],className='flex half')],className='flex')
    ]),
    html.Div([html.Button(['Transfer to Alumni'],id='trans-alum-btn',n_clicks=0,className='choice'),
              html.Button('Update to Regular',id='up-reg-btn',n_clicks=0,className='choice'),
              html.Button('Update to Non-Regular',id='up-nonreg-btn',n_clicks=0,className='choice'),
              html.Button('Update to Honorary',id='up-hon-btn',n_clicks=0,className='choice'),
              html.Button('Update to Probationary',id='up-pro-btn',n_clicks=0,className='choice'),
              html.A([html.Button('Back to List',className='choice')],href='/update-member'),])
],className="body")
        ],className='flex container'
    )
])

@app.callback(
[
Output('fullname', 'children'),
Output('mem-id-up', 'children'),
Output('up-mem-status', 'children'),
],
[
Input('url', 'pathname'),
],
[State('url','search')]
)
def members(pathname,search):
    print(search)
    if search:
        parsed=urllib.parse.parse_qs(search)
        if pathname=="/update-member-modify":
            sql="""
            SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name,membership_type,person.valid_id
            FROM 
            person JOIN upciem_member 
            ON person.valid_id=upciem_member.valid_id JOIN affiliation 
            ON person.valid_id=affiliation.valid_id 
            WHERE upciem_member_delete is NULL or upciem_member_delete=False AND 
                """
            sql+="person.valid_id='"+parsed['id'][0]+"'"
            print(sql)
            values=[]
            cols=["Name","Membership",'ID']
            df = db.querydatafromdatabase(sql, values, cols)
            if df.shape[0]:    
                
                return [df["Name"][0]],[df["ID"][0]],[df["Membership"][0]]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('modal-background','className'),
        Output('main-modal','className'),
        Output('up-mem-done','children')
    ],
    [
        Input('trans-alum-btn','n_clicks'),
        Input('up-reg-btn','n_clicks'),
        Input('up-nonreg-btn','n_clicks'),
        Input('up-hon-btn','n_clicks'),
        Input('up-pro-btn','n_clicks'),
     ],
     [
         State('url','search')
    ]
)
def show_modal(alum,reg,nonreg,hon,pro,search):
    parsed=urllib.parse.parse_qs(search)
    act=dash.no_update
    if alum>0:
        act="Transferring"
    elif reg>0:
        act="Converted to regular"
        sql="UPDATE affiliation SET membership_type='Regular' WHERE valid_id=%s"
        values=[parsed['id'][0]]
        db.modifydatabase(sql,values)
    elif nonreg>0:
        act="Converted to Non-Regular"
        sql="UPDATE affiliation SET membership_type='Non-Regular' WHERE valid_id=%s"
        values=[parsed['id'][0]]
        db.modifydatabase(sql,values)
    elif hon>0:
        act="Converted to Honorary"
        sql="UPDATE affiliation SET membership_type='Honorary' WHERE valid_id=%s"
        values=[parsed['id'][0]]
        db.modifydatabase(sql,values)
    elif pro>0:
        act="Converted to Probationary"
        sql="UPDATE affiliation SET membership_type='Probationary' WHERE valid_id=%s"
        values=[parsed['id'][0]]
        db.modifydatabase(sql,values)
    else:
        raise PreventUpdate
    return 'shown modal-background','shown modal',act