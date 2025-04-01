import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import dash_bootstrap_components as dbc
import io
import base64
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from drawer_court import draw_court, draw_court_team
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import warnings
warnings.filterwarnings('ignore')

players = pd.read_csv('../datasets/players.csv')
sacramento_players = players[players['TEAM_ABBREVIATION'] == 'SAC']
teams = pd.read_csv('../datasets/teams.csv')

selected_columns = ['FG_PCT_Restricted_Area', 'FG_PCT_In_The_Paint_(Non-RA)', 'PTS_PER_GP', 'AST_PER_GP', 'STL_PER_GP', 'BLK_PER_GP']
selected_data = sacramento_players[selected_columns]
scaler = StandardScaler()
scaled_data = scaler.fit_transform(selected_data)
pca = PCA(n_components=4)
pca_result = pca.fit_transform(scaled_data)
kmeans = KMeans(n_clusters=3, random_state=42)
sacramento_players['cluster'] = kmeans.fit_predict(pca_result)

fig, ax = plt.subplots(figsize=(15,10))
corr_matrix = players.select_dtypes(include='number').corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix,
            annot=True,
            cmap='coolwarm_r',
            mask=mask,
            ax=ax)
plt.close()

buf = io.BytesIO()
fig.savefig(buf, format='png')
buf.seek(0)
heatmap_base64 = base64.b64encode(buf.read()).decode('utf-8')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI])

sidebar = html.Div(
    [
        html.H4("Sacramento Kings", className="text-white p-1", style={"marginTop": "1rem"}),
        html.Hr(style={"borderTop": "1px dotted white"}),
        dbc.Nav(
            [
                dbc.NavLink("Dataframe", href="/dataframe", active="exact"),
                dbc.NavLink("Correlação", href="/heatmap", active="exact"),
                dbc.NavLink("Histograma", href="/histogram", active="exact"),
                dbc.NavLink("Card dos Atletas", href="/card", active="exact"),
                dbc.NavLink("Card dos Times", href="/card_team", active="exact"),
            ],
            vertical=True,
            pills=True,
            style={"fontSize": 18},
        ),
        html.P(u"Version 1.0", className="fixed-bottom text-white p-2"),
    ],
    className="bg-dark",
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "14rem",
        "padding": "1rem",
    },
)

def render_data_dictionary():
    data_dictionary = [
        "PLAYER_NAME: Nome do jogador",
        "TEAM_ABBREVIATION: Nome do time",
        "AGE: Idade",
        "FG_PCT_Restricted_Area: Percentual de cestas na área restrita do garrafão",
        "FG_PCT_In_The_Paint_(Non-RA): Percentual de cestas no garrafão fora da área restrita",
        "FG_PCT_Mid-Range: Percentual de cestas na altura do arremesso livre",
        "FG_PCT_Left_Corner_3: Percentual de cestas de 3 pts do lado esquerdo",
        "FG_PCT_Right_Corner_3: Percentual de cestas de 3 pts do lado direito",
        "FG_PCT_Above_the_Break_3: Percentual de cestas de 3 pts perto do meio da quadra",
        "PTS_PER_GP: Pontos por partida",
        "IMC: IMC do atleta",
        "NET_RATING_PCT_PER_GP: Diferença entre os rebotes ofensivo e defensivo por 100 posses de bola",
        "OREB_PCT_PER_GP: Percentual do rebote ofensivo",
        "DREB_PCT_PER_GP: Percentual do rebote defensivo",
        "USG_PCT_PER_GP: Mede a eficiência do jogador em quadra",
        "TS_PCT_PER_GP: Mede a eficiência de cestas do jogador",
        "AST_PCT_PER_GP: Percentual de assistências por jogo",
        "PTS_PER_MIN: Pontos por minuto",
        "MIN_PER_GP: Minutos por jogo",
        "STL_PER_GP: Bolas roubadas por jogo",
        "BLK_PER_GP: Bloqueios por jogo",
        "TOV_PER_GP: Perdas de bola por jogo",
        "PF_PER_GP: Faltas cometidas por jogo",
        "AVG_SPEED_KPH: Velocidade média por jogo (km/h)"
    ]

    formatted_data = html.Div([
        html.H5("Dicionário de Dados", className="card-title"),
        html.Ul([html.Li(data) for data in data_dictionary])
    ], className="card-text")

    return dbc.Card(
        dbc.CardBody(formatted_data)
    )

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/dataframe':
        return html.Div([
            html.H1('Tabela e Algumas Estatísticas'),
            html.Pre(sacramento_players.to_string()),
            html.Hr(),
            html.Pre(sacramento_players.describe().to_string())
        ])
    elif pathname == '/heatmap':
        return html.Div([
            html.H1('Heatmap'),
            html.Img(src='data:image/png;base64,{}'.format(heatmap_base64))
        ])
    elif pathname == '/histogram':
        return html.Div([
            html.H1('Histograma'),
            dcc.Dropdown(
                id='coluna-dropdown-hist',               
                options=[{'label': col, 'value': col} for col in players.select_dtypes(include='number').columns if col != 'PLAYER_ID'],
                value=players.select_dtypes(include='number').columns[0]
            ),
            html.Div(id='histogram-container')
        ])
    elif pathname == '/card':
        return html.Div([
            html.H1('Card dos Atletas'),
            dcc.Dropdown(
                id='player-dropdown',
                options=[{'label': player, 'value': player} for player in sacramento_players['PLAYER_NAME'].unique()],
                value=sacramento_players['PLAYER_NAME'].unique()[0]
            ),
            html.Div(id='card-container'),
        ])
    elif pathname == '/card_team':
        return html.Div([
            html.H1('Card dos Times'),
            dcc.Dropdown(
                id='team-dropdown',
                options=[{'label': team, 'value': team} for team in teams['TEAM_NAME'].unique()],
                value=teams['TEAM_NAME'].unique()[0]
            ),
            html.Div(id='card_team-container'),
        ])
    else:
        return render_data_dictionary()

@app.callback(
    Output('histogram-container', 'children'),
    [Input('coluna-dropdown-hist', 'value')]
)
def update_histogram(selected_column):
    plt.figure(figsize=(15, 5))
    sns.histplot(players[selected_column], kde=True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    histogram_base64 = base64.b64encode(buf.read()).decode('utf-8')

    return html.Img(src='data:image/png;base64,{}'.format(histogram_base64))

@app.callback(
    Output('card-container', 'children'),
    [Input('player-dropdown', 'value')]
)
def update_card(selected_player):
    court_figure = draw_court(sacramento_players, selected_player)
    buf = io.BytesIO()
    court_figure.savefig(buf, format='png')
    buf.seek(0)
    court_image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return html.Img(src='data:image/png;base64,{}'.format(court_image_base64))

@app.callback(
    Output('card_team-container', 'children'),
    [Input('team-dropdown', 'value')]
)
def update_card_team(selected_team):
    court_figure = draw_court_team(teams, selected_team)
    buf = io.BytesIO()
    court_figure.savefig(buf, format='png')
    buf.seek(0)
    court_image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return html.Img(src='data:image/png;base64,{}'.format(court_image_base64))

app.layout = html.Div([
    dcc.Location(id='url'),
    sidebar,
    html.Div(id='page-content', style={'margin-left': '15rem', 'margin-right': '5rem', 'padding': '0rem 0rem', 'background-color': '#FFF', 'max-width': '80%'}),
    html.Div(id='court-container'),
    html.Div(id='card-container'),
    dcc.Store(id='court-image', data=None)
])

if __name__ == '__main__':
    app.run_server(debug=True)
