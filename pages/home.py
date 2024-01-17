
from dash import html
from apps import commonmodule as cm

bot_style={
    "font-family":"Tahoma", 
    "font-weight":"bold",
    "color": "white",
    "padding":"0px 8px", 
    "margin":"0"}



layout=html.Div([
    cm.top,
    html.Div([
        cm.navigationpanel,
        html.Div([
            html.H2("One Circle, One Family",
                    style={
                    "text-align": "center",
                    "font-family": "Tahoma",
                    "font-size":"3rem",
                    "margin-top": "0",
                    "margin-bottom": "0",
                    "color": "#273250",
                    "font-weight":"bolder"
                    }
                    ),
            html.H2("Expanding the Circle Since 1976",
                    style={
                    "text-align": "center",
                    "font-family": "Tahoma",
                    "font-size":"1.5em",
                    "margin-bottom": "0.5em",
                    "margin-top": "0",
                    "color": "#273250",
                    "font-weight":"bold"}
                    ),
            html.Img(src="./assets/ciempic.jpeg",style={"max-width": "100%"}),
            html.H2("About CIEM",
                    style={
                    "text-align": "left",
                    "font-family": "Tahoma",
                    "font-size":"1.5em",
                    "margin-bottom": "0.3em",
                    "margin-top": "0.5em",
                    "color": "#273250",
                    "font-weight":"bold"}
                    ),
            html.H4("The University of the Philippines Circle of Industrial Engineering Majors (UP CIEM) was established on November 23, 1976 by a group of students from the Department of Industrial Engineering and Operations Research, College of Engineering at the University of the Philippines, Diliman. Over the years, UP CIEM has grown from a fledging organization to a force to be reckoned with, not only in academics but in sports, social activities, and leadership as well. The business of UP CIEM never falls short of the foundations of Industrial Engineering – effectiveness, efficiency, and productivity. UP CIEM is a duly recognized college-wide, socio-academic organization. UP CIEM consistently makes its mark through rendering service to the college, the university, and the country by upholding its core values: academic excellence, leadership in service, and social relevance through numerous projects that cater to the needs of Industrial Engineering students. More than being an organization, UP CIEM continues to be the family of camaraderie and trust for the IE student body and the sanctuary of excellent Industrial Engineers for the nation’s future.",
                    style={
                    "font-family": "Arial",
                    "font-weight":"normal",
                    "text-align":"justify",
                    "margin":"0"}
                    ),
        html.Br(),

html.Div([
        html.A([
            html.Div([
                html.Img(src="./assets/fb.png",className="logo", style={"margin-top":"0","height":"2em"}),
                html.H4("Facebook Page", style=bot_style),
                ],
                className="flex center")
        ], href="https://www.facebook.com/upciem",  
                ),
        html.A([
            html.Div([
                html.Img(src="./assets/ig.png",className="logo", style={"margin-top":"0","height":"2em"}),
                html.H4("Instagram", style=bot_style),
                ],
                className="flex center")
        ], href="https://www.instagram.com/upciem/",
                ),
        html.A([
            html.Div([
                html.Img(src="./assets/twt.png",className="logo", style={"margin-top":"0","height":"2em"}),
                html.H4("Twitter", style=bot_style),
                ],
                className="flex center")
        ], href="https://twitter.com/upciem",
                ),
        html.A([
            html.Div([
                html.Img(src="./assets/in.png",className="logo", style={"margin-top":"0","height":"2em"}),
                html.H4("LinkedIn", style=bot_style),
                ],
                className="flex center")
        ], href="https://ph.linkedin.com/company/upciem1976",
                ),
], className="flex center", style={"background-color":"#3F66BD", "padding":"0.7em 0.7em","justify-content":"space-evenly"})
        
        ], 
                className="body"),
    ],className='flex container')
])