from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date,datetime
from apps import dbconnect as db
from app import app
from apps import commonmodule as cm

head_style = {
    "font-family": "Arial",
    "color": "#273250",
        }



layout=html.Div([
    cm.top,
    html.Div([cm.navigationpanel,
        html.Div([
    html.Div([
    html.Label(className='hidden modal-background',id='ep-bg'),
    html.Div([
        html.Div(
            [html.H3("Action Done")],className='modal-header'
        ),
        html.P("Successfully Reaffiliated"),
        html.A([html.Button("Proceed",className='enter')],href='/reaffiliate')
    ],className='hidden modal',id='ep-main')
]),
    html.H2("Reaffiliation Form", style=head_style),
    html.H3("* Please fill out required fields in red boxes", style={"font-family":"Arial", "margin":"0", "font-style":"italic", "font-weight":"normal", "font-size":"medium", "padding":"0 1em"}),
    html.Div([
        html.Div([
            html.H3("First Name:"),dcc.Input(type='text', id='edit-fname', required=True),
            html.H3("Middle Name:"),dcc.Input(type='text', id='edit-mname'),
            html.H3("Last Name:"),dcc.Input(type='text', id='edit-lname', required=True),
            html.H3("Suffix:"),dcc.Input(type='text', id='edit-sfx'),
            ],className='flex edit name', style={"display":"flex"}),
            
        html.Div([
            html.H3("Birthday:"),dcc.DatePickerSingle(id='edit-bday',min_date_allowed=date(1940,1,1),display_format="MMM DD, YYYY", placeholder="YYYY-MM-DD", style={"font-family":"Arial"}, clearable=True),
            html.H3("Contact Number:"),dcc.Input(type='text', id='edit-cn', required=True),
            html.H3("Emergency Contact Number:"),dcc.Input(type='text', id='edit-ecn', required=True),
            ],className='flex edit others',style={"display":"flex"}),
        html.Div([ 
            html.Div([html.H3("Email Address:"),dcc.Input(type='text', id='edit-email', required=True),html.H3("Valid ID:"),dcc.Input(type='text',id='edit-vid', required=True)],className='flex add'),
            html.Div([html.H3("Present Address:"),dcc.Input(type='text', id='edit-presadd', required=True),],className='flex add'),
            html.Div([html.H3("Permanent Address:"),dcc.Input(type='text', id='edit-permadd', required=True)],className='flex add'),
            ],className='address'),
        html.Div([html.Button("Submit Form",id='up-prof-btn',n_clicks=0, className="choice")],className='flex last')
    ],className='edit'),
],className="body")
    ],className='flex container', style={"display":"flex"})
])

@app.callback(
[
    Output('edit-fname','value'),
    Output('edit-mname','value'),
    Output('edit-lname','value'),
    Output('edit-sfx','value'),
    Output('edit-bday','date'),
    Output('edit-cn','value'),
    Output('edit-ecn','value'),
    Output('edit-email','value'),
    Output('edit-vid','value'),
    Output('edit-presadd','value'),
    Output('edit-permadd','value'),

],
[
    Input('url','pathname'),
],
[
    State('auth','data')
]
)
def populate_info(pathname, data):
    if pathname=="/edit-profile":
        id=data['acc']
        sql="""
SELECT first_name,middle_name,last_name,suffix,birthdate,contact_number,emergency_contact_number,email,valid_id,present_address,permanent_address 
from person where account_id=
"""
        sql+=id
        values=[]
        cols=['fname','mname','lname','sfx','bday','cn','ecn','em','vid','pradd','peadd']
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0]:
            return df['fname'][0],df['mname'][0],df['lname'][0],df['sfx'][0],df['bday'][0], df['cn'][0],df['ecn'][0],df['em'][0],df['vid'][0],df['pradd'][0],df['peadd'][0]
        raise PreventUpdate
    else:
        raise PreventUpdate
@app.callback(
    [Output('ep-main','className'),
     Output('ep-bg','className')
     ],
     [Input('up-prof-btn','n_clicks')],
     [
         State('edit-fname','value'),
    State('edit-mname','value'),
    State('edit-lname','value'),
    State('edit-sfx','value'),
    State('edit-bday','date'),
    State('edit-cn','value'),
    State('edit-ecn','value'),
    State('edit-email','value'),
    State('edit-vid','value'),
    State('edit-presadd','value'),
    State('edit-permadd','value'),
    State('auth','data'),
     ]
)
def edit_prof(btn,fname,mname,lname,sfx,bday,cn,ecn,email,vid,presadd,permadd,data):
    if btn>0:
        print(bday)
        sql="""
            UPDATE person
            SET
            first_name=%s,
            middle_name=%s,
            last_name=%s,
            suffix=%s,
            birthdate=%s,
            contact_number=%s,
            emergency_contact_number=%s,
            email=%s,
            valid_id=%s,
            present_address=%s,
            permanent_address=%s
            WHERE account_id=
            """
        sql+=data['acc']
        values=[fname,mname,lname,sfx,bday,cn,ecn,email,vid,presadd,permadd]
        db.modifydatabase(sql,values)
        return 'shown modal','shown modal-background'
    raise PreventUpdate