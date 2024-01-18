
from dash import html,dash_table,dcc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
from apps import dbconnect as db 
from apps import commonmodule as cm
layout=html.Div(
    [
        cm.top,
        html.Div([
            cm.navigationpanel,
            html.Div([
    html.H2("Update Members"),
        html.Div([html.H5("Search Name"),
        dcc.Input(
            type='text',
            className='searchbar',
            id='uns'
        )],className='flex half'),
    html.Div(id="update_mem",
        className="dt"),
],className="body")
        ],className='flex container')
    ]
)

@app.callback(
[
Output('update_mem', 'children')
],
[
Input('url', 'pathname'),
Input('uns','value'),
]
)
def members(pathname,namesearch):
    if pathname=="/update-member":
        sql="""	SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name,membership_type
            FROM 
            person JOIN upciem_member 
            ON person.valid_id=upciem_member.valid_id JOIN affiliation 
            ON person.valid_id=affiliation.valid_id 
            WHERE True
            """
        values=[]
        cols=["Name","Membership Type"]
        if namesearch:
            sql+="""AND CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) ILIKE %s"""
            values+={f"%{namesearch}%"}
        df = db.querydatafromdatabase(sql, values, cols)
        df['Action'] = [f'<a href="/update-member-modify?mode=edit&id={id}" ><Button class="lbtn">Edit</Button></a>' for id in df['Name']]
        table=dash_table.DataTable(
        data=df.to_dict('records'),  # Convert DataFrame to list of dictionaries
        columns=[{'name': i, 'id': i, 'presentation': 'markdown'} if i == 'Action' else {'name': i, 'id': i} for i in df.columns],  # Specify column names and IDs
        markdown_options={'html': True},
        style_cell={
            "height":"50px",
            'text-align':'left',
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
        page_size=10,
        style_table={"height":"80%",'overflow':'hidden'},
)
        return [table]
    else:
        raise PreventUpdate