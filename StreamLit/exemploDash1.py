from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd


# lendo os dados do arquivo CSV
df = pd.read_csv('dados.csv',delimiter=';', encoding='utf-8')
print(df['Valores'])
app = Dash(__name__)

graph = dcc.Graph()

dropdown = dcc.Dropdown(['Algodão', 'Pluma', 'Caroço', 'Todos'], 'Todos', clearable=False)
app.layout = html.Div([
    html.H4("Exemplo de dados de algodão"), dropdown, graph])


@callback(Output(graph, 'figure'), Input(dropdown, 'value'))
def update_barchart(tipo):
    if tipo != 'Todos':
        mascara = df["Tipos"] == tipo
        print(mascara)
    else:
        mascara = [True]*len(df["Tipos"])
    fig = px.bar(df[mascara], x="Tipos", y="Valores")
    return fig

if __name__ == '__main__':
    app.run(debug=True)