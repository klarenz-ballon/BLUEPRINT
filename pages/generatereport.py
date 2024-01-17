import plotly.graph_objs as go
from dash import html,dash_table,dcc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.express as px
from app import app
from apps import dbconnect as db
from apps import commonmodule as cm
layout=html.Div([
    cm.top,
    html.Div(
        [
            cm.navigationpanel,
            html.Div([
    html.H2("Report Generations"),
    html.H3("Tracking"),
    html.Div([html.H4("Active Members"),
    html.H5(" Current Count:",id='active-count'),],className='flex otherside'),
    html.Div(id='active-table'),
    html.Div([html.H4("Inactive Members"),
    html.H5(" Current Count:",id='inactive-count'),],className='flex otherside'),
    html.Div(id='inactive-table'),
    
    html.Div([html.H4("Alumni"),
    html.H5(" Current Count:",id='alum-count'),],className='flex otherside'),
    html.Div(id='alum-table'),
    dcc.Graph(id='by-batch'),
    dcc.Graph(id='by-year'),
    dcc.Graph(id='by-committee'),
],className='body')
        ], className='flex container'
    )
])

@app.callback(
    [
        Output('by-batch','figure'),
        Output('by-year','figure'),
        Output('by-committee','figure'),
        Output('active-count','children'),
        Output('active-table','children'),
        Output('inactive-count','children'),
        Output('inactive-table','children'),
        Output('alum-count','children'),
        Output('alum-table','children'),
     ],
    [Input('url','pathname')],
    []
)
def generate_rep(pathname):
    tckact=dash.no_update
    yearapp=dash.no_update
    comapp=dash.no_update
    actcount=dash.no_update
    acttab=dash.no_update
    inactcount=dash.no_update
    inacttab=dash.no_update
    if pathname=="/generate-report":
        #for the active table
        sql="SELECT (first_name||' '||middle_name||' '||last_name||' '||suffix) as full_name from person join upciem_member on person.valid_id=upciem_member.valid_id WHERE active_status='Active'"
        values=[]
        cols=['Full Name']
        df=db.querydatafromdatabase(sql,values,cols)
        acttab=dash_table.DataTable(
        data=df.to_dict('records'),  # Convert DataFrame to list of dictionaries
        columns=[{'name': i, 'id': i} for i in df.columns],  # Specify column names and IDs
        style_cell={
            "height":"50px",
            'text-align':'center',
            "background-color":"#EEF2FA",
            "color":"#273250",
            },
        style_header={
            "background-color":"#000097",
            "color":"#FFF",
            "text-align":"center",
            "border-bottom":"4px solid white",
            },
        page_action='native',
        page_size=5 ,
        style_table={"height":"80%",'overflow':'hidden',})
        actcount="Current Count:"+str(df.shape[0])
        #for inactive table
        sql="SELECT (first_name||' '||middle_name||' '||last_name||' '||suffix) as full_name from person join upciem_member on person.valid_id=upciem_member.valid_id WHERE active_status='Inactive'"
        values=[]
        cols=['Full Name']
        df=db.querydatafromdatabase(sql,values,cols)
        inacttab=dash_table.DataTable(
        data=df.to_dict('records'),  # Convert DataFrame to list of dictionaries
        columns=[{'name': i, 'id': i} for i in df.columns],  # Specify column names and IDs
        style_cell={
            "height":"50px",
            'text-align':'center',
            "background-color":"#EEF2FA",
            "color":"#273250",
            },
        style_header={
            "background-color":"#000097",
            "color":"#FFF",
            "text-align":"center",
            "border-bottom":"4px solid white",
            },
        page_action='native',
        page_size=5 ,
        style_table={"height":"80%",'overflow':'hidden',})
        inactcount="Current Count:"+str(df.shape[0])
        #for alumni table
        sql="SELECT (first_name||' '||middle_name||' '||last_name||' '||suffix) as full_name from person join alumni on person.valid_id=alumni.valid_id WHERE True"
        values=[]
        cols=['Full Name']
        df=db.querydatafromdatabase(sql,values,cols)
        alumtab=dash_table.DataTable(
        data=df.to_dict('records'),  # Convert DataFrame to list of dictionaries
        columns=[{'name': i, 'id': i} for i in df.columns],  # Specify column names and IDs
        style_cell={
            "height":"50px",
            'text-align':'center',
            "background-color":"#EEF2FA",
            "color":"#273250",
            },
        style_header={
            "background-color":"#000097",
            "color":"#FFF",
            "text-align":"center",
            "border-bottom":"4px solid white",
            },
        page_action='native',
        page_size=5 ,
        style_table={"height":"80%",'overflow':'hidden',})
        alumcount="Current Count:"+str(df.shape[0])
        return [tckact,yearapp,comapp,actcount,acttab,inactcount,inacttab,alumcount,alumtab]

    raise PreventUpdate