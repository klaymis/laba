import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px


df = pd.read_csv('your_data.csv')


app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("Анализ данных о солнечной радиации"),


    dcc.Graph(id='solar-radiation-graph'),


    dcc.Graph(id='second-graph'),


    dcc.RangeSlider(
        id='date-range-slider',
        marks={i: str(df['Date'][i]) for i in range(0, len(df), len(df) // 5)},
        min=0,
        max=len(df),
        step=1,
        value=[0, len(df)],
        tooltip={'placement': 'bottom'}
    ),


    dcc.Dropdown(
        id='graph-type-dropdown',
        options=[
            {'label': 'Line Plot', 'value': 'line'},
            {'label': 'Scatter Plot', 'value': 'scatter'}
        ],
        value='line'
    ),



])



@app.callback(
    dash.dependencies.Output('solar-radiation-graph', 'figure'),
    [dash.dependencies.Input('date-range-slider', 'value'),
     dash.dependencies.Input('graph-type-dropdown', 'value')])
def update_graph(selected_range, graph_type):
    # Обновление графика в зависимости от выбранного диапазона дат и типа графика
    filtered_df = df.iloc[selected_range[0]:selected_range[1]]

    if graph_type == 'line':
        fig = px.line(filtered_df, x='Date', y='Solar Radiation', title='Line Plot: Solar Radiation over Time')
    elif graph_type == 'scatter':
        fig = px.scatter(filtered_df, x='Date', y='Solar Radiation', title='Scatter Plot: Solar Radiation over Time')

    return fig



@app.callback(
    dash.dependencies.Output('second-graph', 'figure'),
    [dash.dependencies.Input('date-range-slider', 'value')])
def update_second_graph(selected_range):
    # Логика обновления второго графика в зависимости от выбранного диапазона дат
    filtered_df = df.iloc[selected_range[0]:selected_range[1]]
    fig = px.histogram(filtered_df, x='Column2', title='Histogram of Column2')

    return fig



if __name__ == '__main__':
    app.run_server(debug=True)