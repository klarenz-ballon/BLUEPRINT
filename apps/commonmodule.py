from app import app
from dash import html,Output,Input
import dash
from dash.exceptions import PreventUpdate

navbar_style = {
    "font-family": "Arial",
    "font-size": "0.9rem"
    }
navigationpanel = html.Nav(
    [
        html.Div(
            [
            html.H4("Main", style=navbar_style),
            html.A("Home", href="/home", id='home', style=navbar_style),
            html.A("Logout", href="#",id='lo',n_clicks=0, style={"font-family": "Arial", "font-size": "0.9rem","font-style":"italic"})
            ],className="module-div"),
        html.Div(
            [
            html.H4("Reaffiliation", style=navbar_style),
            html.A("Reaffiliation Form", href="/reaffiliate",id='reaff', style=navbar_style),
            ],className="module-div"),
        # html.Div(
        #     [
        #     html.H4("Reaffilation"),
        #     html.A("Reaffilation Form",href="/reaffiliate",id='reaff'),
        #     ],className="module-div"),
        html.Div(
            [
            html.H4("Members", style=navbar_style),
            html.A("All Members", href="/members",id='members', style=navbar_style),
            ],className="module-div"),
        html.Div(
            [
            html.H4("Alumni", style=navbar_style),
            html.A("All Alumni", href="/alumni",id='alumns', style=navbar_style),
            ],className="module-div"),
        html.Div(
            [
            html.H4("Account Management", style=navbar_style),
            html.A("Member Status", href="/update-member",id='update-mems', style=navbar_style),
            html.A("Alumni Status", href="/update-alumni",id='update-alums', style=navbar_style),
            html.A("Change Password", href="/change-password",id='change', style=navbar_style),
            #html.A("Managers", href="/managers?mode=view",id='managers'),
            ],className="module-div"),
        html.Div([
            html.H4("Reports", style=navbar_style),
            html.A("Generate Report", href="/generate-report",id='tracks', style=navbar_style),
            ],className="module-div"),
    ],
className="nav", style={"padding":"0px 15px"})

@app.callback(
    [
        Output('home','className'),
        #Output('edit','className'),
        Output('change','className'),
        Output('reaff','className'),
        Output('members','className'),
        Output('alumns','className'),
        Output('update-mems','className'),
        Output('update-alums','className'),
        #Output('managers','className'),
        Output('tracks','className'),
     ],
     [Input('url','pathname')]
)
def current_page(pathname):
    h=dash.no_update
    #e=dash.no_update
    c=dash.no_update
    r=dash.no_update
    m=dash.no_update
    a=dash.no_update
    um=dash.no_update
    ua=dash.no_update
    #mg=dash.no_update
    tr=dash.no_update
    if pathname == '/' or pathname == '/home':
        h='disabled-a'
    elif pathname=="/change-password":
        c='disabled-a'
    # elif pathname=="/edit-profile":
    #     e='disabled-a'
    elif pathname=="/generate-report":
        tr='disabled-a'
    #elif pathname=="/managers":
        #mg='disabled-a'
    elif pathname=="/members":
        m='disabled-a'
    elif pathname=="/reaffiliate":
        r='disabled-a'
    elif pathname=="/update-alumni":
        ua='disabled-a'
    elif pathname=="/update-member" or pathname=="/update-member-modify":
        um='disabled-a'
    elif pathname=="/alumni":
        a='disabled-a'
    return h,c,r,m,a,um,ua,tr
top=html.Div([
        html.A([
            html.Div([
                html.Img(src="./assets/logo.png",className="logo", style={"margin-top":"0"}),
                html.H2("UP Circle of Industrial Engineering Majors (UP CIEM)", style={"font-family":"Tahoma", "font-weight":"normal","padding":"0px 8px"}),
                html.H2("BLUEPrint", style={"font-family":"Tahoma", "font-weight":"normal"}),
                ],
            
                
                className="flex center"),
                
            ],
            href="/home", style={"padding":"0px 15px"}),
            
            
        ],
        className="topbar")
       