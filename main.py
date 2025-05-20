import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash import dcc, html, Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([  # BYT UT dbc.Container MOT html.Div FÖR FLEX
    html.H2("Beräkning av laddtid för elbil med räckvidsberäkning"),  # === RUBRIK
    html.Br(),
    # === FLEX-CONTAINER STARTAR
    html.Div([  
        # === KOLUMN 1: ELBILSDATA ===
        html.Div([
            # region Elbilsdata
            html.Div([
                html.H4("Elbildata"),
                html.Hr(),                
                html.Label("Storlek på ditt elbilsbatteri (kWh):", style={"marginRight": "10px", "fontWeight": "bold"}),
                dcc.Slider(
                    id='ev_carbattery_sliderval',
                    min=5,
                    max=80, step=0.1, value=10.4,
                    marks={i: str(i) for i in range(5, 81, 5)}
                ),
                html.Div([
                    html.Label("Räckvidd vid 100% laddning enligt tillverkaren (km):", style={"marginRight": "10px", "fontWeight": "bold"}),
                    dcc.Input(id="evRange", value="0", type="number", style={"width": "65px"}),
                ]),         
                html.Br(),

                html.Div(id="evData")  # === VISAR VÄRDET FRÅN SLIDER
            ], className="evDIV"),
            # endregion
        ], className="colstyle"),  # === STÄNGER KOLUMN 1

        # === KOLUMN 2: LADDARINSTÄLLNINGAR ===
        html.Div([
            # region Laddarensdata
            html.Div([
                html.H4("Billaddare"),
                html.Hr(),
                html.Div([
                    html.Label("Storlek på laddaren (kW):", style={"marginRight": "10px", "fontWeight": "bold"}),
                    dcc.Dropdown(
                        id="charger_size_kw",
                        options=[
                            {"label": "3,7 kw, AC", "value": "3.7"},
                            {"label": "7,4 kw, AC", "value": "7.4"},
                            {"label": "11 kw, AC", "value": "11"},
                            {"label": "22 kw, AC", "value": "22"},
                            {"label": "24 kw, DC", "value": "24"},
                            {"label": "50 kw, DC", "value": "50"},
                            {"label": "100–150 kw, DC", "value": "150"},
                            {"label": "200–350 kw, DC", "value": "350"},
                        ],
                        value="--VÄLJ--",
                        clearable=False,
                        style={"width": "170px"}
                    )
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "10px"}),

                html.Label("Verkningsgrad (%):"),
                dcc.Slider(
                    id='charger_efficiency',
                    min=50,
                    max=100,
                    step=1,
                    value=90,
                    marks={i: f"{i}%" for i in range(50, 101, 10)}
                ),

                dbc.Checklist(
                    options=[{"label": "Laddbegränsning?", "value": "enabled"}],
                    value=[],
                    id="charger_max_toggle",
                    switch=True,
                    style={"marginRight": "10px", "fontWeight": "bold"}
                ),

                html.Div(
                    children=[
                        html.Label("Max laddnivå (%):"),
                        dcc.Slider(
                            id='charger_max_limit',
                            min=50,
                            max=100,
                            step=5,
                            value=100,
                            marks={i: f'{i}%' for i in range(10, 101, 10)}
                        )
                    ],
                    id="chMax",
                    style={"display": "none"},
                ),

                html.Div(id="chargerInfo"),
            ])
            # endregion
        ], className="chDIV")  # === STÄNGER KOLUMN 2

    ], className="flex-container"),  # === STÄNGER FLEX-CONTAINER

    # === SIMLUERINGSLAYOUT ====
    html.Div([
    # region --- simuleringsalayout
        html.Div([
            dcc.Graph(id='charge_simulation_plot')
        ], style={"width": "65%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            html.Img(id="battery_image", src="/assets/battery_100.png", style={
                "height": "80px",
                "display": "block",
                "margin": "auto"
            }),

            dcc.Slider(
                id="range_slider",
                min=0,
                max=500,  
                value=100,
                step=1
            ),
            html.Div(id="current_range_display", style={
                "textAlign": "center",
                "marginTop": "10px",
                "fontSize": "18px",
                "fontWeight": "bold",
                "color": "green"
            })
        ], style={"width": "50%", "paddingLeft": "20px"})
    ], style={"marginTop": "40px"})
    # endregion --- simuleringslaout

], className="main-container")  # === YTTRE WRAPPER SOM KAN CENTRERA ALLT


# region === HÄNDELSE I DIV ELBILSDATA ===
@app.callback(
    Output('evData', 'children'),
    Input('ev_carbattery_sliderval', 'value'),
    Input('evRange', 'value')
)

def evDisplayComponent(value, range_km):
    if value >= 70:
        color = "green"
    elif value >= 40:
        color = "orange"
    else:
        color = "red"

    # Default: visa endast batteristorlek
    lines = [
        html.Span("🔋", style={"fontSize": "32px", "marginRight": "10px"}),
        html.Div([
        html.Hr(),            
            html.Div(
                f"Vald batteristorlek: {value:.1f} kWh",
                style={
                    "fontWeight": "bold",
                    "color": "red",
                    "fontSize": "20px",
                }
            )
        ])
    ]

    # Lägg till energieffektivitet om räckvidd angivits
    if range_km and float(range_km) > 0:
        eff = (value * 1000) / float(range_km)
        lines[1].children.append(
            html.Div(
                f"Energieffektivitet: {eff:.0f} Wh/km",
                style={
                    "fontWeight": "bold",
                    "color": "red",
                    "fontSize": "18px",
                    "marginTop": "4px"
                }
            )
        )

    return html.Div(
        lines,
        style={
            "display": "flex",
            "alignItems": "flex-start",
            "gap": "12px",
            "marginTop": "10px",
            "marginBottom": "10px"
        }
    )

def update_ev_display(battery_size, ev_range):
    return evDisplayComponent(battery_size, ev_range)
# endregion === SLUT PÅ CALLBACK EV ===

# region === HÄNDELSE I DIV BILLDDARE ===

# region -- En separat callback för toggle av visning ---
@app.callback(
    Output("chMax", "style"),
    Input("charger_max_toggle", "value")
)

# === TOGGLAR MELLAN VISA OCH GÖM
def toggle_slider_visibility(toggle_values):
    if 'enabled' in toggle_values:
        return {"display": "block"}
    return {"display": "none"}
# endregion --- sluttogglat

# region -- En seperat callback för räkna på laddningskapacitet och visa ---
# endregion -- SLUT HÄNDELSE I BILLADDARE
@app.callback(
    Output("chargerInfo", "children"),
    Input("charger_size_kw", "value"),
    Input("charger_efficiency", "value"),   
    Input("charger_max_limit", "value"),
    Input("charger_max_toggle", "value")
)

# === UPPDATERA TEXT
def update_charger_display(charger_size_kw, charger_efficiency, charger_max_limit, charger_max_toggle):
    if not charger_size_kw or not charger_efficiency:
        return "Välj laddare och verkningsgrad"

    limit_active = 'enabled' in charger_max_toggle

    driftkapacitet = calculateEffectiveChargingCapacity(
        charger_size_kw, charger_efficiency, charger_max_limit, limit_active
    )

    return html.Div([
        html.Span("🔌", style={"fontSize": "28px", "marginRight": "10px"}),
        html.Div([
            html.Hr(),               
            html.Div(
                f"Driftkapacitet: {driftkapacitet} kW",
                style={"fontWeight": "bold", "color": "blue", "fontSize": "18px"}
            ),
        ])
    ], style={"display": "flex", "alignItems": "center", "gap": "12px", "marginTop": "10px"})

# === BERÄKNA AKTUELL DRIFTLADDNING (EFFEKTIV LADDNINGSEFFEKT i kW)
def calculateEffectiveChargingCapacity(charger_size_kw, charger_efficiency, charger_max_limit, limit_active):
    """
    Beräknar effektiv driftkapacitet i kW för en laddare.
    Tar hänsyn till verkningsgrad och eventuell laddbegränsning.
    """
    # Säkerställ att alla värden är float
    charger_size_kw = float(charger_size_kw)    # storlek på laddaren, i kW
    efficiency_pct = float(charger_efficiency)      # verkningsgrad, i procent
    limit_pct = float(charger_max_limit)                # Max laddnivå i procent – om laddbegränsning är aktiv

    # Steg 1: Verkningsgrad
    effective_power = charger_size_kw * (charger_efficiency / 100)

    # Steg 2: Laddbegränsning (om aktiv)
    if limit_active:
        effective_power *= (charger_max_limit / 100)

    return round(effective_power, 2)  # avrundat till 2 decimaler

# endregion --- SLUT BILLADDARE

# region === HÄNDELSE UPPDATERA GRAF MED VÄRDE
# region --- callback graf ---
@app.callback(
    Output("charge_simulation_plot", "figure"),
    Output("range_slider", "max"),
    Input("ev_carbattery_sliderval", "value"),
    Input("charger_efficiency", "value"),
    Input("charger_size_kw", "value"),
    Input("charger_max_limit", "value"),
    Input("charger_max_toggle", "value"),
    Input("evRange", "value")
)

def update_simulation(batt_kwh, efficiency_pct, charger_kw, max_limit_pct, toggle, ev_range):
    fig = go.Figure()

    # Skydd mot evRange = 0
    try:
        ev_range = float(ev_range)
    except (TypeError, ValueError):
        ev_range = 0

    if ev_range == 0:
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='lines+markers', name="Ingen räckvidd"))
    else:
        x_vals = list(range(0, 101, 10))  # batterinivå i procent
        y_vals = [round(ev_range * (x / 100), 1) for x in x_vals]  # beräknad sträcka
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines+markers',
                                 name="Beräknad körsträcka", line=dict(color="green")))

    fig.update_layout(
        xaxis_title="Batterinivå (%)",
        yaxis_title="Körsträcka (km)",
        yaxis_range=[0, max(ev_range, 10)]
    )

    return fig, ev_range


# --- callback för uppdatera bilden på laddningen
@app.callback(
    Output("battery_image", "src"),
    Input("range_slider", "value"),
    State("range_slider", "max")
)

def update_battery_image(current_val, max_val):
    if max_val == 0:
        return "/assets/battery_10.png"

    percentage = (current_val / max_val) * 100

    if percentage >= 90:
        return "/assets/battery_100.png"
    elif percentage >= 60:
        return "/assets/battery_75.png"
    elif percentage >= 40:
        return "/assets/battery_50.png"
    elif percentage >= 15:
        return "/assets/battery_25.png"
    else:
        return "/assets/battery_10.png"

# endregion callback för batteriikon med text

# region --- SLUT: callback graf ---
@app.callback(
    Output("current_range_display", "children"),
    Input("range_slider", "value"),
    Input("evRange", "value"),
    Input("ev_carbattery_sliderval", "value"),
    Input("charger_efficiency", "value"),
    Input("charger_size_kw", "value"),
    Input("charger_max_limit", "value"),
    Input("charger_max_toggle", "value"),
)
def update_range_display(current_km, max_km, battery_kwh, efficiency_pct, charger_kw, limit_pct, toggle):
    try:
        current_km = float(current_km)
        max_km = float(max_km)
        battery_kwh = float(battery_kwh)
        efficiency = float(efficiency_pct) / 100
        charger_kw = float(charger_kw)
        limit_factor = float(limit_pct) / 100 if 'enabled' in toggle else 1.0
    except (TypeError, ValueError):
        return "Aktuell körsträcka: ? km\nLaddtid: ?"

    if max_km == 0 or charger_kw == 0:
        return f"Aktuell körsträcka: {current_km} km\nLaddtid: –"

    # Uträkning: hur mycket energi krävs för den körsträckan?
    wh_per_km = (battery_kwh * 1000) / max_km
    required_energy_kwh = (current_km * wh_per_km) / 1000

    # Effektiv laddningseffekt
    effective_power = charger_kw * efficiency * limit_factor

    # Laddtid i minuter
    charging_time_hours = required_energy_kwh / effective_power
    charging_time_minutes = charging_time_hours * 60

    return html.Div([
        html.Div(f"Aktuell körsträcka: {current_km:.0f} km"),
        html.Div(f"Laddtid för denna sträcka: {charging_time_minutes:.0f} min")
    ], style={"textAlign": "center", "fontWeight": "bold", "color": "green"})
# endregion --- SLUT: callback för batteriikon med text---

# endregion === SLUT UPPDATERA HÄNDELSE I GRAF MED VÄRDE


app = app.server  # För Gunicorn / WSGI
if __name__ == '__main__':
    app.run(debug=True)
