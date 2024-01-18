
from dash import html
from apps import commonmodule as cm
layout=html.Div([
    cm.top,
    html.Div([
        cm.navigationpanel,
        html.Div([
    html.H2("Update Alumni",style={"font-family": "Arial", "color": "#273250"})
],className="body")
    ],className='flex container')
])