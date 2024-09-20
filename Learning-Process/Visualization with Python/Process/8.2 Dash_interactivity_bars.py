import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output

### Task 1: read data

airline_data = pd.read_csv('airline_data.csv',
                   encoding='ISO-8859-1',
                   dtype={'Div1Airport':str, 'Div1TailNum':str,
                          'Div2Airport':str, 'Div2TailNum':str})

### Task 2: Create dash application and get the layout
#create Dash application layout

app = dash.Dash(__name__)
app.layout = html.Div(children=[ html.H1('Total number of flights to the destination state split by reporting airline',
                            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                            html.Div(["Input Year: ", dcc. Input(id='input-year',value='2010',
                            type='number', style={'height':'50px', 'font-size': 35}),], 
                            style={'font-size': 40}),html.Br(), html.Br(),
                            html.Div(dcc.Graph(id='bar-plot')),]) 
              
### Task 3: Add the application callback function
@app.callback(Output(component_id='bar-plot', component_property='figure'),
              Input(component_id='input-year', component_property='value'))


### Task 4: Define Callback graph function
def get_graph(entered_year):
    df =  airline_data[airline_data['Year']==int(entered_year)]
    bar_data = df.groupby('DestState')['Flights'].sum().reset_index()
    fig = px.bar(bar_data, x= "DestState", y= "Flights", title='Total number of flights to the destination state split by reporting airline') 
    fig.update_layout(title='Flights to Destination State', xaxis_title='DestState', yaxis_title='Flights')
    return fig        

### Task 5: run app
if __name__== '__main__':
    app.run_server()
