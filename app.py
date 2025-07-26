import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc

# Load data
df = pd.read_excel('final_data.xlsx')

# Initialize Dash app with Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("🎓 ระบบข้อมูลหลักสูตรมหาวิทยาลัย", className="text-center text-primary mb-4"),
                width=12)
    ]),

    dbc.Row([
        dbc.Col([
            html.Label("ประเภทหลักสูตร", className="fw-bold"),
            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in sorted(df['ประเภทหลักสูตร'].unique())],
                id='type-filter',
                placeholder="เลือกประเภทหลักสูตร"
            ),
        ], md=4),

        dbc.Col([
            html.Label("ชื่อมหาวิทยาลัย", className="fw-bold"),
            dcc.Dropdown(
                options=[{'label': i, 'value': i} for i in sorted(df['ชื่อมหาวิทยาลัย'].unique())],
                id='uni-filter',
                placeholder="เลือกมหาวิทยาลัย"
            ),
        ], md=4),

        dbc.Col([
            html.Label("คำค้นหา", className="fw-bold"),
            dcc.Input(
                id='search-input',
                type='text',
                placeholder='ค้นหาคำสำคัญ...',
                debounce=True,
                className='form-control'
            )
        ], md=4)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            html.H4("📋 ตารางข้อมูลหลักสูตร", className="text-secondary"),
            dash_table.DataTable(
                id='course-table',
                columns=[
                    {"name": i, "id": i, 'presentation': 'markdown' if i == 'URL' else 'input'}
                    for i in df.columns
                ],
                data=df.to_dict('records'),
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_data_conditional=[
                    {
                        'if': {'column_id': 'ค่าเทอมต่อเทอม_ประมาณ'},
                        'color': 'blue',
                        'fontWeight': 'bold'
                    }
                ]
            )
        ])
    ], className="mb-5"),

    dbc.Row([
        dbc.Col([
            html.H4("📊 ค่าเทอมเฉลี่ยตามประเภทหลักสูตร", className="text-secondary"),
            dcc.Graph(id='tuition-chart')
        ])
    ])
], fluid=True, style={'padding': '2rem'})


# Callback
@app.callback(
    [Output('course-table', 'data'),
     Output('tuition-chart', 'figure')],
    [Input('type-filter', 'value'),
     Input('uni-filter', 'value'),
     Input('search-input', 'value')]
)
def update_dashboard(selected_type, selected_uni, keyword):
    filtered = df.copy()

    if selected_type:
        filtered = filtered[filtered['ประเภทหลักสูตร'] == selected_type]
    if selected_uni:
        filtered = filtered[filtered['ชื่อมหาวิทยาลัย'] == selected_uni]
    if keyword:
        filtered = filtered[filtered.apply(lambda row: keyword.lower() in str(row).lower(), axis=1)]

    chart = px.bar(
        filtered.groupby("ประเภทหลักสูตร")["ค่าเทอมต่อเทอม_ประมาณ"].mean().reset_index(),
        x="ประเภทหลักสูตร",
        y="ค่าเทอมต่อเทอม_ประมาณ",
        labels={"ค่าเทอมต่อเทอม_ประมาณ": "ค่าเทอมเฉลี่ย"},
        title="ค่าเทอมเฉลี่ยต่อประเภทหลักสูตร"
    )
    chart.update_layout(template='plotly_white')

    return filtered.to_dict('records'), chart


if __name__ == '__main__':
    app.run(debug=True)
