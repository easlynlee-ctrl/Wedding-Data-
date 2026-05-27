import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import math

# ---------- Load Data from Local Files ----------
#Imported math to do the calculations on the raw data that is imported onto the .py 
# file that supports the toggle for the graphic of the dress and the flower bouquet. 
data_folder = "/Users/BlushingButterfly/MY_PYTHON/VIRTUAL/py311/DataVis/Final Project/Data/wedding_data/"

df_median = pd.read_csv(data_folder + "01_median_age_first_marriage.csv")
df_marital = pd.read_csv(data_folder + "02_marital_status_by_state.csv")
df_master = pd.read_csv(data_folder + "00_MASTER_wedding_research.csv")

# Data cleaning
df_median['year'] = df_median['year'].astype(int)
df_marital['year'] = df_marital['year'].astype(int)
df_master['year'] = df_master['year'].astype(int)

# Filter cost data (years with non-null avg_cost_usd)
df_cost = df_master[df_master['avg_cost_usd'].notna()].copy()
df_cost['avg_cost_usd'] = df_cost['avg_cost_usd'].astype(float)
df_cost['avg_guests'] = df_cost['avg_guests'].astype(float)

# Normalization ranges for bouquet and dress
cost_min, cost_max = df_cost['avg_cost_usd'].min(), df_cost['avg_cost_usd'].max()
guest_min, guest_max = df_cost['avg_guests'].min(), df_cost['avg_guests'].max()

def normalize_cost(value):
    """Normalize cost to bouquet radius (0.05 to 0.25)"""
    if cost_max == cost_min:
        return 0.15
    return 0.05 + (value - cost_min) / (cost_max - cost_min) * 0.20

def normalize_guests(value):
    """Normalize guest count to dress width (0.3 to 0.7)"""
    if guest_max == guest_min:
        return 0.5
    return 0.3 + (value - guest_min) / (guest_max - guest_min) * 0.4

# Color theme
bg_cream = "#FDF5E6"
plot_bg_cream = "#FFF8E7"
olive_main = "#556B2F"
olive_light = "#6B8E23"
olive_dark = "#3B5E3B"
text_color = olive_dark

# ---------- Function to Draw Bouquet (Cost) ----------
def draw_bouquet(year, scale=1.0):
    row = df_cost[df_cost['year'] == year]
    if row.empty:
        return go.Figure()
    cost = row.iloc[0]['avg_cost_usd']
    radius = normalize_cost(cost) * scale
    radius = min(radius, 0.4)  # cap to avoid overflow

    # Bouquet center position
    center_x, center_y = 0.5, 0.5
    fig = go.Figure()

    # Stem
    fig.add_shape(type="line",
                  x0=center_x, y0=center_y - radius*0.8, x1=center_x, y1=center_y + radius*0.2,
                  line=dict(color="green", width=4))

    # Petals
    num_petals = 6
    for i in range(num_petals):
        angle = 2 * math.pi * i / num_petals
        offset_x = center_x + radius * 0.7 * math.cos(angle)
        offset_y = center_y + radius * 0.7 * math.sin(angle)
        fig.add_shape(type="circle",
                      x0=offset_x - radius*0.4, y0=offset_y - radius*0.4,
                      x1=offset_x + radius*0.4, y1=offset_y + radius*0.4,
                      fillcolor="#FFB6C1", line=dict(color="#FF69B4", width=1))

    # Center flower
    fig.add_shape(type="circle",
                  x0=center_x - radius*0.3, y0=center_y - radius*0.3,
                  x1=center_x + radius*0.3, y1=center_y + radius*0.3,
                  fillcolor="#FFD700", line=dict(color="#FFA500", width=1))

    fig.update_layout(
        title=dict(text=f"Wedding Cost (Bouquet Size)<br>{year} | Avg Cost: ${cost:,.0f}",
                   font=dict(color=text_color, size=16, family="Adam")),
        xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False),
        paper_bgcolor=bg_cream,
        plot_bgcolor=plot_bg_cream,
        height=400,
        margin=dict(l=20, r=20, t=80, b=20),
        font=dict(family="Adam, Arial, sans-serif", color=text_color)
    )
    return fig

# ---------- Function to Draw Dress Bell (Guests) ----------
def draw_dress(year, scale=1.0):
    row = df_cost[df_cost['year'] == year]
    if row.empty:
        return go.Figure()
    guests = row.iloc[0]['avg_guests']
    width = normalize_guests(guests) * scale
    width = min(width, 0.9)  # cap

    center_x = 0.5
    bodice_top = 0.7
    bodice_bottom = 0.55
    skirt_bottom = 0.2
    skirt_left = center_x - width/2
    skirt_right = center_x + width/2

    fig = go.Figure()

    # Skirt (bell)
    fig.add_shape(type="path",
                  path=f"M {skirt_left} {skirt_bottom} L {center_x} {bodice_bottom} L {skirt_right} {skirt_bottom} Z",
                  fillcolor=olive_light, line=dict(color=olive_dark, width=2))
    # Bodice
    fig.add_shape(type="rect",
                  x0=center_x-0.08, y0=bodice_bottom, x1=center_x+0.08, y1=bodice_top,
                  fillcolor=olive_main, line=dict(color=olive_dark, width=2))
    # Head
    fig.add_shape(type="circle",
                  x0=center_x-0.06, y0=bodice_top-0.02, x1=center_x+0.06, y1=bodice_top+0.1,
                  fillcolor=olive_dark, line=dict(color=olive_dark, width=1))

    fig.update_layout(
        title=dict(text=f"Wedding Guests (Dress Bell Width)<br>{year} | Avg Guests: {guests:.0f}",
                   font=dict(color=text_color, size=16, family="Adam")),
        xaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[0, 1], showgrid=False, zeroline=False, visible=False),
        paper_bgcolor=bg_cream,
        plot_bgcolor=plot_bg_cream,
        height=400,
        margin=dict(l=20, r=20, t=80, b=20),
        font=dict(family="Adam, Arial, sans-serif", color=text_color)
    )
    return fig

# ---------- Dash App ----------
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Marriage Trends Dashboard", style={'textAlign': 'center', 'color': text_color, 'fontFamily': "Adam", 'marginTop': 20}),
    html.P("Interactive analysis of marriage age, wedding costs, guest counts, and state marriage rates.",
           style={'textAlign': 'center', 'color': olive_main, 'fontFamily': "Adam", 'fontSize': 18}),

    # Graph 1: Median age at first marriage
    html.Div([dcc.Graph(id="median-graph")], style={'marginBottom': 30}),

    # Year slider for wedding visuals
    html.Div([
        html.Label("Select Year for Wedding Data:", style={'color': text_color, 'fontFamily': "Adam", 'fontWeight': 'bold'}),
        dcc.Slider(
            id="wedding-year-slider",
            min=int(df_cost['year'].min()),
            max=int(df_cost['year'].max()),
            step=1,
            value=int(df_cost['year'].max()),
            marks={int(y): str(y) for y in df_cost['year'].unique()},
            tooltip={"placement": "bottom", "always_visible": True}
        ),
    ], style={'padding': '20px', 'marginBottom': 20}),

    # Two separate wedding graphs side by side
    #This is where I originally had a problem with the additional graphs overlapping
    # and had to explicitly separate the two from each other
    #I would like the bell of the wedding dress to expand and shrink based on the amount of wedding guest. 
    # I was able to use Claude to create the actual dashboard to produce it, but it could not teach me how to make the code.  
    # The same issue shows with the flower – the flower expands instead of the amount of flowers in the bouquet shrinking and growing. 
    # The information is displayed by a dragger. It originally remove the plus and minus sign as it adds no value to the viewer – the data doesn’t translate. 
    html.Div([
        # Bouquet (Cost) graph with its own scale buttons
        html.Div([
            html.H4("Bouquet Size = Wedding Cost", style={'textAlign': 'center', 'color': text_color}),
            html.Div([
                html.Button("+", id="bouquet-grow", n_clicks=0, style={'margin': '5px'}),
                html.Button("-", id="bouquet-shrink", n_clicks=0, style={'margin': '5px'}),
            ], style={'textAlign': 'center'}),
            dcc.Graph(id="bouquet-graph")
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        # Dress (Guests) graph with its own scale buttons
    #The scale is seperate from the toggle - it will expand the size but not align with the year information. 
    #I've tried to update it with AI but it disrupts the whole graph
        html.Div([
            html.H4("Dress Bell Width = Number of Guests", style={'textAlign': 'center', 'color': text_color}),
            html.Div([
                html.Button("+", id="dress-grow", n_clicks=0, style={'margin': '5px'}),
                html.Button("-", id="dress-shrink", n_clicks=0, style={'margin': '5px'}),
            ], style={'textAlign': 'center'}),
            dcc.Graph(id="dress-graph")
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    ], style={'marginBottom': 30}),

    # Graph 3: State marriage percentages
    html.Div([
        html.Label("Select Year for State Data:", style={'color': text_color, 'fontFamily': "Adam", 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id="state-year-dropdown",
            options=[],
            value=int(df_marital['year'].max()),
            clearable=False,
            style={'width': '200px'}
        ),
        dcc.Graph(id="state-graph")
    ])
], style={'backgroundColor': bg_cream, 'padding': '20px'})

# ---------- Callbacks ----------
@app.callback(
    Output("median-graph", "figure"),
    Input("median-graph", "id")
)
def update_median_graph(_):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_median['year'], y=df_median['men'], mode='lines+markers', name='Men',
                             line=dict(color=olive_dark, width=3)))
    fig.add_trace(go.Scatter(x=df_median['year'], y=df_median['women'], mode='lines+markers', name='Women',
                             line=dict(color=olive_light, width=3)))
    fig.add_trace(go.Scatter(x=df_median['year'], y=df_median['gap_years'], mode='lines+markers', name='Age Gap',
                             line=dict(color="#B8860B", width=2, dash='dot')))
    fig.update_layout(
        title="Median Age at First Marriage (1890–2024)",
        xaxis_title="Year",
        yaxis_title="Age (years)",
        paper_bgcolor=bg_cream,
        plot_bgcolor=plot_bg_cream,
        font=dict(family="Adam, Arial, sans-serif", color=text_color),
        hovermode="closest"
    )
    return fig

# Bouquet callback
@app.callback(
    Output("bouquet-graph", "figure"),
    Input("wedding-year-slider", "value"),
    Input("bouquet-grow", "n_clicks"),
    Input("bouquet-shrink", "n_clicks")
)
def update_bouquet(year, grow, shrink):
    scale = 1.0 + (grow - shrink) * 0.1
    scale = max(0.2, min(2.0, scale))
    return draw_bouquet(year, scale)

# Dress callback
@app.callback(
    Output("dress-graph", "figure"),
    Input("wedding-year-slider", "value"),
    Input("dress-grow", "n_clicks"),
    Input("dress-shrink", "n_clicks")
)
def update_dress(year, grow, shrink):
    scale = 1.0 + (grow - shrink) * 0.1
    scale = max(0.2, min(2.0, scale))
    return draw_dress(year, scale)

# State graph callback
@app.callback(
    Output("state-graph", "figure"),
    Input("state-year-dropdown", "value")
)
def update_state(year):
    if year is None:
        return go.Figure()
    df_year = df_marital[df_marital['year'] == year]
    if df_year.empty:
        return go.Figure()
    top15 = df_year.nlargest(15, 'pct_married')
    fig = px.bar(top15, x='pct_married', y='state', orientation='h', text='pct_married',
                 labels={'pct_married': 'Percentage Married (%)', 'state': 'State'})
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside',
                      marker=dict(color=olive_main, line=dict(color=olive_dark, width=1)))
    fig.update_layout(
        title=f"States with Highest Marriage Percentage ({year})",
        paper_bgcolor=bg_cream,
        plot_bgcolor=plot_bg_cream,
        font=dict(family="Adam, Arial, sans-serif", color=text_color)
    )
    return fig

# State dropdown options
@app.callback(
    Output("state-year-dropdown", "options"),
    Input("state-year-dropdown", "id")
)
def set_state_options(_):
    years = sorted(df_marital['year'].unique())
    return [{"label": str(y), "value": int(y)} for y in years]

# ---------- Run the App ----------
if __name__ == "__main__":
    app.run(debug=True)
