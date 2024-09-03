from dash import Dash, html, dcc 
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import date
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

# initialize the dash app as 'app'
app = Dash(__name__)

# create the dataframe from some fake data
datetime=pd.date_range('2024-01-01', periods=1e5, freq='min') # datetime range
u_winds=np.random.rand(100000)*4+5 # random values between 5 and 9
v_winds=np.random.rand(100000) # random values between 0 and 1
temp=(np.random.rand(100000)*10)-5 # random values between -5 and 5
d={'datetime':datetime, 'u':u_winds, 'v':v_winds, 'temp':temp} # set a data dictionary
csat_output_df=pd.DataFrame(data=d) # create the dataframe
csat_output_df.set_index('datetime', inplace=True) # set the datetime index
beginning_date=csat_output_df.index[0]
ending_date=csat_output_df.index[-1]
today=dt.today().strftime('%Y-%m-%d')
print(beginning_date, ending_date)
# use specs parameter in make_subplots function
# to create secondary y-axis


# plot a scatter chart by specifying the x and y values
# Use add_trace function to specify secondary_y axes.
def create_figure(csat_output_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=csat_output_df.index, y=csat_output_df['u'], name="U Wind Speed"),
        secondary_y=False)
    
    # Use add_trace function and specify secondary_y axes = True.
    fig.add_trace(
        go.Scatter(x=csat_output_df.index, y=csat_output_df['v'], name="V Wind Speed"),
        secondary_y=False,)

    fig.add_trace(
        go.Scatter(x=csat_output_df.index, y=csat_output_df['temp'], name="Temperature"),
        secondary_y=True,)

    # set axis titles
    fig.update_layout(
        template='simple_white',
        title='HWY 401 CSAT Data',
        xaxis_title="Date",
        yaxis_title="Winds (m/s)",
        yaxis2_title="Temperature (C)",
        yaxis2_range=[-10,10],
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )   
    )
    return fig

# set up the app layout
app.layout = html.Div(children=
                    [
                    html.H1(children=['SWAPIT HWY 401 Met Dashboard']),
                    html.Div(children=['Met plot display with date picker']),

                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=beginning_date,
                        max_date_allowed=ending_date
                    ),
                    dcc.Graph(id='cru-csat-plot',figure=create_figure(csat_output_df)),
                    
                    ] 
                    )

# @app.callback(
#     Output('graph_2', 'figure'),
#     [Input('date-picker', 'start_date'),
#     Input('date-picker', 'end_date')],
#     [State('submit_button', 'n_clicks')])

@app.callback(
    Output('cru-csat-plot', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))

def update_output(start_date, end_date):
    print (start_date, end_date)
    if not start_date or not end_date:
        raise PreventUpdate
    else:
        output_selected_df = csat_output_df.loc[
            (csat_output_df.index >= start_date) & (csat_output_df.index <= end_date), :
        ]
        return create_figure(output_selected_df)


if __name__=='__main__':
    app.run(debug=False, host='0.0.0.0', port=8050)
    # app.run(debug=True)