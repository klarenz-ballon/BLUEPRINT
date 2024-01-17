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
     ],
    [Input('url','pathname')],
    []
)
def generate_rep(pathname):
    tckact=dash.no_update
    yearapp=dash.no_update
    comapp=dash.no_update
    if pathname=="/generate-report":
        sql="SELECT app_batch,COUNT(*) from upciem_member WHERE True GROUP BY app_batch ORDER BY app_batch ASC;"
        values=[]
        cols=['Batch','Count']
        df=db.querydatafromdatabase(sql,values,cols)
        tckact=px.bar(df,x='Batch',y='Count',title='Total Active by App Batch')
        tckact.update_layout(xaxis=dict(dtick=1),yaxis=dict(dtick=1))
        sql="SELECT year_standing,COUNT(*) from upciem_member WHERE True GROUP BY year_standing ORDER BY year_standing ASC"
        values=[]
        cols=['Year','Count']
        df=db.querydatafromdatabase(sql,values,cols)
        yearapp=px.bar(df,x='Year',y='Count',title='Total Active by Year Standing',)
        yearapp.update_layout(xaxis=dict(dtick=1))
        sql="SELECT app_batch,COUNT(*) from upciem_member WHERE True GROUP BY app_batch;"
        values=[]
        cols=['com','Count']
        df=db.querydatafromdatabase(sql,values,cols)
        comapp=px.line(df,x='com',y='Count',title='Total Active by Committee',)
        comapp.update_layout(xaxis=dict(dtick=1),yaxis=dict(dtick=1))
        return [tckact,yearapp,comapp]

    raise PreventUpdate