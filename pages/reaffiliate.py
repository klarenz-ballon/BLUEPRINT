from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import date,datetime
from apps import dbconnect as db
from app import app
from apps import commonmodule as cm
import dash
head_style = {
    "font-family": "Arial",
    "color": "#273250",
        }
comms=[
        "Academic Affairs Committee",
        "External Affairs Committee",
        "Finance Committee",
        "Internal Affairs Committee",
        "Membership and Recruitment Committee",
        "Publications and Records Committee"
]


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
        html.P("Successfully Reaffiliated",id='reaff-msg'),
        html.A([html.Button("Proceed",className='enter')],href='/reaffiliate')
    ],className='hidden modal',id='ep-main')
]),
    html.H2("Reaffiliation Form", style=head_style),
    html.H3("* Please fill out required fields in red boxes(Submit Button will only show after filling out all requied fields)", style={"font-family":"Arial", "margin":"0", "font-style":"italic", "font-weight":"normal", "font-size":"medium", "padding":"0 1em"}),
    html.Div([
        html.Div([
            html.H3("First Name:"),dcc.Input(type='text', id='reaf-fname', required=True),
            html.H3("Middle Name:"),dcc.Input(type='text', id='reaf-mname'),
            html.H3("Last Name:"),dcc.Input(type='text', id='reaf-lname', required=True),
            html.H3("Suffix:"),dcc.Input(type='text', id='reaf-sfx'),
            ],className='flex edit name', style={"display":"flex"}),
            
        html.Div([
            html.H3("Birthday:"),dcc.DatePickerSingle(id='reaf-bday',min_date_allowed=date(1940,1,1),display_format="MMM DD, YYYY", placeholder="YYYY-MM-DD", style={"font-family":"Arial"}, clearable=True),
            html.H3("Contact Number:"),dcc.Input(type='text', id='reaf-cn', required=True),
            html.H3("Emergency Contact Number:"),dcc.Input(type='text', id='reaf-ecn', required=True),
            ],className='flex edit others',style={"display":"flex"}),
        html.Div([ 
            html.Div([html.H3("Email Address:"),dcc.Input(type='text', id='reaf-email', required=True),html.H3("Valid ID:"),dcc.Input(type='text',id='reaf-vid', required=True)],className='flex add'),
            html.Div([html.H3("Present Address:"),dcc.Input(type='text', id='reaf-presadd', required=True),],className='flex add'),
            html.Div([html.H3("Permanent Address:"),dcc.Input(type='text', id='reaf-permadd', required=True)],className='flex add'),
            ],className='address'),
        html.Div([
            html.Div([html.H3("Degree Program:"),dcc.Input(type='text',id='reaf-degree'),
                      html.H3("Year Standing:"),dcc.Dropdown(id='year-stand',options=[1,2,3,4,5,6,7,8], value=1,searchable=False,clearable=False),
                      html.H3("Membership type:"),dcc.Dropdown(id='reaf-type',options=["Regular","Non-Regular","Honorary","Probationary"],value='Regular',searchable=False,clearable=False,style={'width':'100%'}),
                      html.H3("App Batch:"),dcc.Input(id='reaf-batch',type='text'),
                      html.H3("GWA:"),dcc.Input(type='text', id ='reaf-gwa')
                    ],className='flex edit name'),
                    html.H3("Committee Preferences (Select from first priority to last priority)"),
           html.Div([dcc.Dropdown(id='ranking-dropdown', options=[{'label': choice, 'value': choice} for choice in comms], multi=True,style={'width':'100%'})],className='flex edit others') 
        ]),
        html.Div([html.H3("Reaffilation Fee"),dcc.Dropdown(id='reaff-fee',options=["pay as I submit","pay at a later Date"],value='pay as I submit',searchable=False,clearable=False,style={'width':200})],className='flex'),
        html.Div([html.Button("Submit Form",id='reaff-btn',n_clicks=0, className="choice")],className='flex last')
    ],className='edit'),
],className="body")
    ],className='flex container', style={"display":"flex"})
])
@app.callback([
    Output('ep-main','className'),
    Output('ep-bg','className'),
    Output('reaff-msg','children')
],
[
    Input('reaff-btn','n_clicks'),
    Input('reaf-fname','value'),
    Input('reaf-mname','value'),
    Input('reaf-lname','value'),
    Input('reaf-sfx','value'),
    Input('reaf-bday','date'),
    Input('reaf-cn','value'),
    Input('reaf-ecn','value'),
    Input('reaf-email','value'),
    Input('reaf-vid','value'),
    Input('reaf-presadd','value'),
    Input('reaf-permadd','value'),
    Input('reaf-degree','value'),
    Input('year-stand','value'),
    Input('reaf-type','value'),
    Input('reaf-batch','value'),
    Input('reaf-gwa','value'),
    Input('ranking-dropdown','value'),
    Input('reaff-fee','value'),
],
)
def reaff_member(btn,fname,mname,lname,sfx,bday,cn,ecn,email,vid,presadd,permadd,deg,ys,rtype,btc,gwa,ranks,fee):
    if btn>0:
        #check if there is existing data
        commpref=[None,None,None,None,None,None]
        print("checking")
        sql="SELECT valid_id FROM person WHERE valid_id='"+vid+"'"
        cols=['new']
        df=db.querydatafromdatabase(sql,[],cols)
        print("checked")
        if df.shape[0]:
            print("existing")
            #there exist a data
            #update existing data
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
                present_address=%s,
                permanent_address=%s
                WHERE valid_id=%s
            """
            values=[fname,mname,lname,sfx,bday,cn,ecn,email,presadd,permadd,vid]
            db.modifydatabase(sql,values)
            #update affiliation
            print("updating affiliation")
            for i,j in enumerate(ranks):
                commpref[i]=j#update rankings of preference, None in case not selected
            sql="""
                UPDATE affiliation 
                SET 
                is_new=False,
                degree_program=%s,
                membership_type=%s,
                year_standing=%s,
                app_batch=%s,
                comm_firstchoice=%s,
                comm_secondchoice=%s,
                comm_thirdchoice=%s,
                comm_fourthchoice=%s,
                comm_fifthchoice=%s,
                comm_sixthchoice=%s,
                gwa=%s,
                reaff_fee=%s
                WHERE valid_id=%s"""
            values=[deg,rtype,ys,btc,commpref[0],commpref[1],commpref[2],commpref[3],commpref[4],commpref[5],gwa,fee,vid]
            db.modifydatabase(sql,values)
            print("done updating affilation")
            return 'shown modal', 'shown modal-background',dash.no_update
        else:  #there is no existing data
            #add new person sincec foreign key first
            print("new")
            sql="""
            INSERT INTO person(valid_id, first_name,middle_name,last_name,suffix,birthdate,contact_number, emergency_contact_number,email,present_address, permanent_address)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            values=[vid,fname,mname,lname,sfx,bday,cn,ecn,email,presadd,permadd]
            db.modifydatabase(sql,values)
            #add status to upciem_member
            sql="INSERT INTO upciem_member(valid_id,active_status) VALUES (%s,'Active')"
            values=[vid]
            db.modifydatabase(sql,values)
            #add new row in table affiliation, sql can be edited if more info is needed
            sql="""
            INSERT INTO affiliation(valid_id,is_new,degree_program,membership_type,year_standing,app_batch,comm_firstchoice,comm_secondchoice,comm_thirdchoice,comm_fourthchoice,comm_fifthchoice,comm_sixthchoice,gwa,reaff_fee)
            VALUES (%s,True,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            values=[vid,deg,rtype,ys,btc,commpref[0],commpref[1],commpref[2],commpref[3],commpref[4],commpref[5],gwa,fee]
            db.modifydatabase(sql,values)
            return 'shown modal', 'shown modal-background','New member Successfully added'
    raise PreventUpdate
@app.callback(
    Output('reaff-btn','hidden'),
    [
    Input('reaf-fname','value'),
    Input('reaf-mname','value'),
    Input('reaf-lname','value'),
    Input('reaf-bday','date'),
    Input('reaf-cn','value'),
    Input('reaf-ecn','value'),
    Input('reaf-email','value'),
    Input('reaf-vid','value'),
    Input('reaf-presadd','value'),
    Input('reaf-permadd','value'),]
)
def enable_submit(a,b,c,d,e,f,g,h,i,j):
    if a and b and c and d and e and f and g and h and i and j:#no None, no empty
        return False
    return True