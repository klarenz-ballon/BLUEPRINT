from dash import html,dash_table,dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from apps import dbconnect as db
from apps import commonmodule as cm
import urllib.parse
layout=html.Div(
    [
        cm.top,
        html.Div([
            cm.navigationpanel,
            html.Div([
    html.H2("Managers"),
    html.Div(
        [
            html.Div(id='manager-table')
        ]
    )
],className="body")
        ],className='flex container')
    ]
)

@app.callback(
    [
        Output('manager-table','children')
    ],
    [Input('url','pathname')],
    [State('auth','data'),State('url','search')]
)
def mode_managers(pathname,data,search):
    accid=data['acc']
    parsed=''
    if search:
        parsed=urllib.parse.parse_qs(search[1:])
    if pathname=='/managers':
        print(parsed)
        if not parsed or 'view' in parsed['mode']:
            sql="SELECT user_account.account_id,(first_name||' '||middle_name||' '||last_name||' '||suffix)as full_name,contact_number,email FROM person join user_account ON person.account_id=user_account.account_id WHERE True"
            values=[]
            cols=['ID','Full Name','Contact','Email']
            df=db.querydatafromdatabase(sql,values,cols)
            df['Action'] = ['' if str(id)==str(accid) else f'<a href="/managers?mode=delete&id={id}" ><Button class="red lbtn">Delete</Button></a>' for id in df['ID']]
            if df.shape[0]:
                table=dash_table.DataTable(
                    data=df.to_dict('records'),  # Convert DataFrame to list of dictionaries
                    columns=[{'name': i, 'id': i, 'presentation': 'markdown'} if i == 'Action' else {'name': i, 'id': i} for i in df.columns],  # Specify column names and IDs
                    markdown_options={'html': True},    
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
                    style_table={"height":"80%",'overflow':'hidden'}
                )
                return [table]
        elif 'add' in parsed['mode']:
            return [html.H3("ADDING")]
        elif 'delete' in parsed['mode']:
            return[html.H3('deleting')]
        else:
            return [html.H3("No Managers to Show")]
    raise PreventUpdate