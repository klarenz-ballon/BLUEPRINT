from dash import html,dash_table,dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db
from apps import commonmodule as cm
layout=html.Div([
    cm.top,
    html.Div([
        cm.navigationpanel,
    html.Div([
    html.H2("Alumni"),
    html.Div([
        html.Div([html.H5("Search Name"),
        dcc.Input(
            type='text',
            className='searchbar',
            id='alname'
        )],className='flex half'),
        html.Div([
        html.H5("Filter by Specialization:"),
        dcc.Input(
            type='text',
            className='searchbar',
            id='specsearch'
        )],className='flex half')
    ],
        className="flex search"),
    html.Div(id="alumn_table",
        className="dt"),

],className="body")
    ],className='flex container')
])

@app.callback(
[
Output('alumn_table', 'children')
],
[
Input('url', 'pathname'),
Input('alname','value'),
Input('specsearch','value'),
]
)
def members(pathname,namesearch,filtersearch):
    if pathname=="/alumni":
        sql="""
        SELECT alumni_id,(first_name||' '||middle_name||' '||last_name||' '||suffix) as full_name, specialization, birthdate, contact_number,email,present_address
        FROM alumni JOIN person
        ON alumni.valid_id=person.valid_id
        WHERE True
            """
        values=[]
        cols=["Alumni ID","Name","Specialization","Birthday","Contact Number","Email","Present Address"]

        if namesearch:
            sql+="""AND (first_name||' '||middle_name||' '||last_name||' '||suffix) ILIKE %s"""
            values+={f"%{namesearch}%"}
        if filtersearch:
            sql+="AND specialization ILIKE %s"
            values+={f"%{filtersearch}%"}
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0]:
            table=dash_table.DataTable(
            data=df.to_dict('records'),  # Convert DataFrame to list of dictionaries
            columns=[{'name': i, 'id': i} for i in df.columns],  # Specify column names and IDs
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
            style_table={"height":"80%",'overflow':'hidden'}
            )
            return [table]
        else:
            return[(html.H2("No Alumni to Display"))]
    else:
        raise PreventUpdate