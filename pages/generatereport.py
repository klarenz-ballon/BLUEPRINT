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
    html.H2("Reports for AY 2022-2023", style={"font-family": "Arial", "color": "#273250"}),
    html.Div(
        [
            html.H2("Tracking List: Members"),
             html.Div([html.H3("Reaffiliated Members"),
            html.H4(" Current Count:",id='reaff-count'),],className='flex otherside'),
            html.Div(id='reaffiliated-table'),
             html.Div([html.H3("New Members"),
            html.H4(" Current Count:",id='new-count'),],className='flex otherside'),
            html.Div(id='new-table'),
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
        html.Div(
        [
            html.H2("Comittee Preferences: Reaffiliated Members"),
            
        ],
        className='section'),
        html.Div(
        [
            html.H2("14 White Stripes: Scores (Ranked)"),
            html.Div(id='whitestripescore-table')
        ],
        className='section'),
        html.Div(
        [
            html.H2("14 White Stripes: Top 14"),
             html.Div(id='whitestripestop-table')
            
        ],
        className='section'),

],className='body')
        ], className='flex container'
    )
])

@app.callback(
    [
        Output('reaff-count','children'),
        Output('reaffiliated-table','children'),
        Output('new-count','children'),
        Output('new-table','children'),
        Output('active-count','children'),
        Output('active-table','children'),
        Output('inactive-count','children'),
        Output('inactive-table','children'),
        Output('alum-count','children'),
        Output('alum-table','children'),
        Output('by-year','children'),
        Output('by-batch','children'),
        Output('whitestripescore-table','children'),
        Output('whitestripestop-table','children'),
     ],
    [Input('url','pathname')],
    []
)
def generate_rep(pathname):
    if pathname=="/generate-report":
        #for reaff table
        sql="""
            SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name, membership_type, degree_program
            from 
            upciem_member join affiliation 
            on upciem_member.affiliation_id=affiliation.affiliation_id 
            join person 
            on upciem_member.valid_id=person.valid_id 
            WHERE is_new=False"""
        values=[]
        cols=['Full Name','Membership','Degree']
        df=db.querydatafromdatabase(sql,values,cols)
        reaftab=dash_table.DataTable(
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
        reafcount="Current Count:"+str(df.shape[0])
        #for new table
        sql="""
            SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name, membership_type, degree_program
            from 
            upciem_member join affiliation 
            on upciem_member.affiliation_id=affiliation.affiliation_id 
            join person 
            on upciem_member.valid_id=person.valid_id 
            WHERE is_new=True"""
        values=[]
        cols=['Full Name','Membership','Degree']
        df=db.querydatafromdatabase(sql,values,cols)
        newtab=dash_table.DataTable(
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
        newcount="Current Count:"+str(df.shape[0])
        #for the active table
        sql="""
            SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name, membership_type, degree_program
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
            SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name, membership_type, degree_program
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
        sql="SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name from person join alumni on person.valid_id=alumni.valid_id WHERE True"
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
        sql="SELECT DISTINCT year_standing FROM affiliation WHERE year_standing IS NOT NULL"
        values=[]
        cols=['ys']
        df=db.querydatafromdatabase(sql,values,cols)
        yeartab=[]
        for year in df['ys']:
            yearstring="YEAR "+str(year)
            yeartab+=[html.H4(yearstring)]
            sql="""
            SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name, membership_type, degree_program
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
        sql="SELECT DISTINCT app_batch FROM affiliation WHERE app_batch IS NOT NULL"
        values=[]
        cols=['ab']
        df=db.querydatafromdatabase(sql,values,cols)
        batchtab=[]
        for batch in df['ab']:
            batchstr="Batch"+str(batch)
            batchtab+=[html.H4(batchstr)]
            sql="""
            SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name, membership_type, degree_program
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
        #for 14 whites
        sql="""
            SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name, membership_type, degree_program,gwa::numeric(10,2)
            from 
            upciem_member join affiliation 
            on upciem_member.affiliation_id=affiliation.affiliation_id 
            join person 
            on upciem_member.valid_id=person.valid_id 
            WHERE True ORDER BY gwa ASC"""#edit this by changing the order you can use formula or something
        values=[]
        cols=['Full Name','Membership','Degree','GWA']
        df=db.querydatafromdatabase(sql,values,cols)
        whitetab=dash_table.DataTable(
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
        #for top 14
        sql="""
            SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name, membership_type, degree_program,gwa::numeric(10,2)
            from 
            upciem_member join affiliation 
            on upciem_member.affiliation_id=affiliation.affiliation_id 
            join person 
            on upciem_member.valid_id=person.valid_id 
            WHERE True ORDER BY gwa ASC LIMIT 14;"""#edit this by changing the order you can use formula or something
        values=[]
        cols=['Full Name','Membership','Degree','GWA']
        df=db.querydatafromdatabase(sql,values,cols)
        whitetoptab=dash_table.DataTable(
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
        page_size=14,
        style_table={"height":"80%",'overflow':'hidden',})
        return [reafcount,reaftab,newcount,newtab,actcount,acttab,inactcount,inacttab,alumcount,alumtab,yeartab,batchtab,whitetab,whitetoptab]

    raise PreventUpdate