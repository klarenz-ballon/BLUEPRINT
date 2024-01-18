
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
            [html.H3("Action Done")],className='modal-header'
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
        html.Div([html.Div([html.H3('Full Name: '),
        html.H3(id='fullname',style={'font-weight':'normal'}),],className='flex half'),
        html.Div([html.H3('ID: '),
        html.H3(id='mem-id-up',style={'font-weight':'normal'}),],className='flex half'),
        html.Div([html.H3('Membership Status: '),
        html.H3(id='up-mem-status',style={'font-weight':'normal'}),],className='flex half')],className='flex')
    ]),
    html.Div([html.Button(['Transfer to Alumni'],id='trans-alum-btn',n_clicks=0,className='choice'),html.Button('Reaffiliate',id='up-ref-btn',n_clicks=0,className='choice'),html.Button('Update to Regular',id='up-stat-btn',n_clicks=0,className='choice'),html.A([html.Button('Back to List',className='choice')],href='/update-member'),])
],className="body")
        ],className='flex container'
    )
])

@app.callback(
[
Output('fullname', 'children'),
Output('mem-id-up', 'children'),
Output('up-mem-status', 'children'),
Output('up-ref-btn','children'),
Output('up-stat-btn','children'),
],
[
Input('url', 'pathname'),
],
[State('url','search')]
)
def members(pathname,search):
    print(search)
    aff='Unaffiliate'
    stat='Probationary'
    if search:
        parsed=urllib.parse.parse_qs(search)
        if pathname=="/update-member-modify":
            sql="""
            SELECT member_id,(first_name||' '||middle_name||' '||last_name||' '||suffix) as full_name,membership_type
            from PERSON join upciem_member 
            ON person.valid_id=upciem_member.valid_id
            WHERE True AND
                """
            sql+="member_id='"+parsed['id'][0]+"'"
            print(sql)
            values=[]
            cols=["Member ID","Name","Membership"]
            df = db.querydatafromdatabase(sql, values, cols)
            if df.shape[0]:    
                if df['Membership'][0]=='Probationary':
                    stat='Regular'
                elif df['Membership'][0]=='Unaffiliated':
                    aff='Reaffiliate'
                return [df["Name"][0]],[df["Member ID"][0]],[df["Membership"][0]],[aff],[stat]
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
        Input('up-ref-btn','n_clicks'),
        Input('trans-alum-btn','n_clicks'),
        Input('up-stat-btn','n_clicks'),
     ],
     [
         State('up-ref-btn','children'),
         State('trans-alum-btn','children'),
         State('up-stat-btn','children'),
         State('url','search')
    ]
)
def show_modal(ref,alum,stat,ref_val,trans_val,stat_val,search):
    print(ref_val,trans_val,stat_val)
    parsed=urllib.parse.parse_qs(search)
    act=dash.no_update
    if ref>0:
        act=ref_val
        sql="UPDATE upciem_member SET membership_type=%s WHERE member_id=%s"
        values=['Reaffiliated' if 'Reaffiliate' in ref_val else 'Unaffilated',parsed['id'][0]]
        db.modifydatabase(sql,values)
    elif alum>0:
        act=trans_val
    elif stat>0:
        act=stat_val
        sql="UPDATE upciem_member SET membership_type=%s WHERE member_id=%s"
        values=['Probationary' if 'Probationary' in stat_val else 'Regular',parsed['id'][0]]
        db.modifydatabase(sql,values)
    else:
        raise PreventUpdate
    return 'shown modal-background','shown modal',act