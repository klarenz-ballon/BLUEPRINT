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
    html.H1("Reports"),
    html.Div(
        [
            html.H2("Tracking List: Members"),
            html.Div([html.H3("Active Members"),
            html.H4(" Current Count:",id='active-count'),],className='flex otherside'),
            html.Div(id='active-table'),
            html.Div([html.H3("Inactive Members"),
            html.H4(" Current Count:",id='inactive-count'),],className='flex otherside'),
            html.Div(id='inactive-table'),
            html.Div([html.H3("Alumni"),
            html.H4(" Current Count:",id='alum-count'),],className='flex otherside'),
            html.Div(id='alum-table'),
        ],
        className='section'),
        html.Div(
        [
            html.H2("Tracking List: Headships"),
            
        ],
        className='section'),
        html.Div(
        [
            html.H2("Tracking List: Alumni Specialization"),
            
        ],
        className='section'),
        html.Div(
        [
            html.H2("Tracking List: Committee"),
            
        ],
        className='section'),
        html.Div(
        [
            html.H2("Tracking List: Year Standing"),
            html.Div(id='by-year')
        ],
        className='section'),
        html.Div(
        [
            html.H2("Tracking List: App Batch"),
            html.Div(id='by-batch')
            
        ],
        className='section'),
        html.Div(
        [
            html.H2("Tracking List: Accountabilities"),
            
        ],
        className='section'),
],className='body')
        ], className='flex container'
    )
])

@app.callback(
    [
        Output('active-count','children'),
        Output('active-table','children'),
        Output('inactive-count','children'),
        Output('inactive-table','children'),
        Output('alum-count','children'),
        Output('alum-table','children'),
        Output('by-year','children'),
        Output('by-batch','children')
     ],
    [Input('url','pathname')],
    []
)
def generate_rep(pathname):
    actcount=dash.no_update
    acttab=dash.no_update
    inactcount=dash.no_update
    inacttab=dash.no_update
    if pathname=="/generate-report":
        #for the active table
        sql="""
            SELECT (first_name||' '||middle_name||' '||last_name||' '||suffix) as full_name, membership_type, degree_program
            from 
            upciem_member join affiliation 
            on upciem_member.affiliation_id=affiliation.affiliation_id 
            join person 
            on upciem_member.valid_id=person.valid_id 
            WHERE active_status='Active'"""
        values=[]
        cols=['Full Name','Membership','Degree']
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
        sql="""
            SELECT (first_name||' '||middle_name||' '||last_name||' '||suffix) as full_name, membership_type, degree_program
            from 
            upciem_member join affiliation 
            on upciem_member.affiliation_id=affiliation.affiliation_id 
            join person 
            on upciem_member.valid_id=person.valid_id 
            WHERE active_status='Inactive'"""
        values=[]
        cols=['Full Name','Membership','Degree']
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
        #for year standing
        sql="SELECT DISTINCT year_standing FROM affiliation WHERE True"
        values=[]
        cols=['ys']
        df=db.querydatafromdatabase(sql,values,cols)
        yeartab=[]
        for year in df['ys']:
            yearstring="YEAR "+str(year)
            yeartab+=[html.H4(yearstring)]
            sql="""
            SELECT (first_name||' '||middle_name||' '||last_name||' '||suffix) as full_name, membership_type, degree_program
            from 
            upciem_member join affiliation 
            on upciem_member.affiliation_id=affiliation.affiliation_id 
            join person 
            on upciem_member.valid_id=person.valid_id 
            WHERE year_standing="""
            sql+=str(year)
            cols=['Full Name','Membership','Degree']
            df=db.querydatafromdatabase(sql,[],cols)
            temp_year=dash_table.DataTable(
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
            yeartab+=[temp_year]
            #for app-batch
            sql="SELECT DISTINCT app_batch FROM affiliation WHERE True"
        values=[]
        cols=['ab']
        df=db.querydatafromdatabase(sql,values,cols)
        batchtab=[]
        for batch in df['ab']:
            batchstr="Batch"+str(batch)
            batchtab+=[html.H4(batchstr)]
            sql="""
            SELECT (first_name||' '||middle_name||' '||last_name||' '||suffix) as full_name, membership_type, degree_program
            from 
            upciem_member join affiliation 
            on upciem_member.affiliation_id=affiliation.affiliation_id 
            join person 
            on upciem_member.valid_id=person.valid_id 
            WHERE app_batch=%s"""
            values=[]
            values+={f"{batch}"}
            cols=['Full Name','Membership','Degree']
            df=db.querydatafromdatabase(sql,values,cols)
            temp_batch=dash_table.DataTable(
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
            batchtab+=[temp_batch]
        print(batchtab)
        return [actcount,acttab,inactcount,inacttab,alumcount,alumtab,yeartab,batchtab]

    raise PreventUpdate