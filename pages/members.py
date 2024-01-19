
from dash import html,dash_table,dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db
from apps import commonmodule as cm
layout=html.Div(
    [
        cm.top,
        html.Div([
            cm.navigationpanel,
            html.Div([
    html.Div([
    html.Label(className='hidden modal-background',id='modal-background'),
    html.Div([
        html.Div(
            [html.H3("Action Done",style={"font-family": "Arial"})],className='modal-header'
        ),
        html.P("Said Action is Made",id='up-mem-done'),
        html.A([html.Button("Back to List",className='enter')],href='/update-member')
    ],className='hidden modal',id='main-modal')
]),
    html.H2("Members",style={"font-family": "Arial", "color": "#273250",
        }),
    html.Div([
        html.Div([html.H5("Search Name", style={"font-family": "Arial"
        }),
        dcc.Input(
            type='text',
            className='searchbar',
            id='namesearch'
        )],className='flex half'),
        html.Div([
        html.H5("Filter by:",style={"font-family": "Arial"
        }),
        dcc.Dropdown(['Member Type','Year Standing','App Batch','Accountabilities'], id='filterdd',searchable=False,className='dropdown', style={"font-family": "Arial","font-size":"small"}),
        dcc.Input(
            type='text',
            className='searchbar',
            id='filtersearch'
        )],className='flex half')
    ],
        className="flex search"),
    html.Div(id="members_table",
        className="dt"),
],className="body")

        ],className='flex container')
    ]
)
@app.callback(
[
Output('members_table', 'children')
],
[
Input('url', 'pathname'),
Input('namesearch','value'),
Input('filterdd','value'),
Input('filtersearch','value'),
]
)
def members(pathname,namesearch,filterdd,filtersearch):
    if pathname=="/members":
        sql="""	SELECT CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) as full_name,birthdate,membership_type,app_batch,year_standing,degree_program,other_org_affiliation,email,present_address
            FROM 
            person JOIN upciem_member 
            ON person.valid_id=upciem_member.valid_id JOIN affiliation 
            ON person.valid_id=affiliation.valid_id 
            WHERE upciem_member_delete is NULL or upciem_member_delete=False
            """
        values=[]
        cols=["Name","Birthday","Membership","App Batch","Year Standing","Degree Program","Other Orgs","Email","Present Address"]
        if namesearch:
            sql+="""AND CONCAT(first_name, ' ',middle_name,' ' ,last_name, ' ', suffix) ILIKE %s"""
            values+={f"%{namesearch}%"}
        if filterdd:
            if filtersearch:
                if filterdd=='Year Standing':
                    sql+="AND year_standing = "+filtersearch
                else:   
                    if filterdd=='Member Type':
                        sql+="AND membership_type ILIKE %s"
                    elif filterdd=='App Batch':
                        sql+="AND app_batch ILIKE %s"
                    elif filterdd=='Accountabilities':
                        sql+="AND other_org_affiliation ILIKE %s"
                    values+={f"%{filtersearch}%"}
        df = db.querydatafromdatabase(sql, values, cols)
        table=dash_table.DataTable(
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
        page_size=10,
        style_table={"height":"80%",'overflow':'auto'}
)
        return [table]
    else:
        raise PreventUpdate