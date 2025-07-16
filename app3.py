import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
import numpy as np

# Load data
df = pd.read_excel('final_data.xlsx')

# Initialize Dash app with Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define color palette
colors = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#F18F01',
    'info': '#C73E1D',
    'light': '#F8F9FA',
    'dark': '#343A40',
    'gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
}

# Layout with enhanced styling
app.layout = dbc.Container([
    # Header Section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("🎓 ระบบข้อมูลหลักสูตรมหาวิทยาลัย", 
                       className="text-center text-white mb-0",
                       style={'font-size': '2.5rem', 'font-weight': 'bold'}),
                html.P("ระบบติดตามและวิเคราะห์ข้อมูลหลักสูตรและค่าเทอมมหาวิทยาลัย",
                      className="text-center text-white-50 mb-0")
            ], style={
                'background': colors['gradient'],
                'padding': '3rem 2rem',
                'border-radius': '15px',
                'box-shadow': '0 10px 30px rgba(0,0,0,0.1)',
                'margin-bottom': '2rem'
            })
        ], width=12)
    ]),

    # Statistics Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id='total-courses', className="text-primary mb-0"),
                    html.P("หลักสูตรทั้งหมด", className="text-muted mb-0")
                ])
            ], className="shadow-sm", style={'border-radius': '10px'})
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id='total-universities', className="text-success mb-0"),
                    html.P("มหาวิทยาลัยทั้งหมด", className="text-muted mb-0")
                ])
            ], className="shadow-sm", style={'border-radius': '10px'})
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id='with-tuition', className="text-info mb-0"),
                    html.P("มีข้อมูลค่าเทอม", className="text-muted mb-0")
                ])
            ], className="shadow-sm", style={'border-radius': '10px'})
        ], md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id='without-tuition', className="text-warning mb-0"),
                    html.P("ไม่ระบุค่าเทอม", className="text-muted mb-0")
                ])
            ], className="shadow-sm", style={'border-radius': '10px'})
        ], md=3)
    ], className="mb-4"),

    # Filter Section
    dbc.Card([
        dbc.CardHeader([
            html.H5("🔍 ตัวกรองข้อมูล", className="mb-0 text-primary")
        ]),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("ประเภทหลักสูตร", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        options=[{'label': i, 'value': i} for i in sorted(df['ประเภทหลักสูตร'].unique())],
                        id='type-filter',
                        placeholder="เลือกประเภทหลักสูตร",
                        style={'border-radius': '8px'}
                    ),
                ], md=4),

                dbc.Col([
                    html.Label("ชื่อมหาวิทยาลัย", className="fw-bold mb-2"),
                    dcc.Dropdown(
                        options=[{'label': i, 'value': i} for i in sorted(df['ชื่อมหาวิทยาลัย'].unique())],
                        id='uni-filter',
                        placeholder="เลือกมหาวิทยาลัย",
                        style={'border-radius': '8px'}
                    ),
                ], md=4),

                dbc.Col([
                    html.Label("คำค้นหา", className="fw-bold mb-2"),
                    dcc.Input(
                        id='search-input',
                        type='text',
                        placeholder='ค้นหาคำสำคัญ...',
                        debounce=True,
                        className='form-control',
                        style={'border-radius': '8px'}
                    )
                ], md=4)
            ])
        ])
    ], className="mb-4 shadow-sm", style={'border-radius': '10px'}),

    # Toggle for NaN data
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("แสดงข้อมูล:", className="fw-bold mb-0"),
                        ], md=3),
                        dbc.Col([
                            dbc.RadioItems(
                                id='data-filter',
                                options=[
                                    {'label': 'ทั้งหมด', 'value': 'all'},
                                    {'label': 'มีค่าเทอม', 'value': 'with_tuition'},
                                    {'label': 'ไม่ระบุค่าเทอม', 'value': 'without_tuition'}
                                ],
                                value='all',
                                inline=True,
                                style={'margin-left': '10px'}
                            )
                        ], md=9)
                    ])
                ])
            ], className="shadow-sm", style={'border-radius': '10px'})
        ])
    ], className="mb-4"),

    # Data Table Section
    dbc.Card([
        dbc.CardHeader([
            html.H5("📋 ตารางข้อมูลหลักสูตร", className="mb-0 text-primary")
        ]),
        dbc.CardBody([
            dash_table.DataTable(
                id='course-table',
                columns=[
                    {"name": i, "id": i, 'presentation': 'markdown' if i == 'URL' else 'input'}
                    for i in ['ชื่อมหาวิทยาลัย'] + [col for col in df.columns if col != 'ชื่อมหาวิทยาลัย']
                ],
                data=df.to_dict('records'),
                page_size=15,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left', 
                    'padding': '12px',
                    'font-family': 'Arial, sans-serif',
                    'font-size': '14px'
                },
                style_header={
                    'backgroundColor': colors['primary'],
                    'color': 'white',
                    'fontWeight': 'bold',
                    'text-align': 'center'
                },
                style_data_conditional=[
                    {
                        'if': {'column_id': 'ค่าเทอมต่อเทอม_ประมาณ'},
                        'color': colors['info'],
                        'fontWeight': 'bold'
                    },
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgba(248, 249, 250, 0.5)'
                    }
                ],
                filter_action="native",
                sort_action="native",
                page_action="native"
            )
        ])
    ], className="mb-4 shadow-sm", style={'border-radius': '10px'}),

    # Charts Section
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("📊 ค่าเทอมเฉลี่ยตามประเภทหลักสูตร", className="mb-0 text-primary")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='tuition-chart')
                ])
            ], className="shadow-sm", style={'border-radius': '10px'})
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H5("🏫 สถิติข้อมูลค่าเทอม", className="mb-0 text-primary")
                ]),
                dbc.CardBody([
                    dcc.Graph(id='tuition-status-chart')
                ])
            ], className="shadow-sm", style={'border-radius': '10px'})
        ], md=6)
    ], className="mb-4"),

    # Universities without tuition info
    dbc.Card([
        dbc.CardHeader([
            html.H5("🏛️ มหาวิทยาลัยที่ไม่ระบุค่าเทอม", className="mb-0 text-warning")
        ]),
        dbc.CardBody([
            html.Div(id='universities-without-tuition')
        ])
    ], className="shadow-sm", style={'border-radius': '10px'})

], fluid=True, style={'padding': '2rem', 'background-color': '#F8F9FA'})


# Callbacks
@app.callback(
    [Output('total-courses', 'children'),
     Output('total-universities', 'children'),
     Output('with-tuition', 'children'),
     Output('without-tuition', 'children'),
     Output('course-table', 'data'),
     Output('tuition-chart', 'figure'),
     Output('tuition-status-chart', 'figure'),
     Output('universities-without-tuition', 'children')],
    [Input('type-filter', 'value'),
     Input('uni-filter', 'value'),
     Input('search-input', 'value'),
     Input('data-filter', 'value')]
)
def update_dashboard(selected_type, selected_uni, keyword, data_filter):
    filtered = df.copy()

    # Apply filters
    if selected_type:
        filtered = filtered[filtered['ประเภทหลักสูตร'] == selected_type]
    if selected_uni:
        filtered = filtered[filtered['ชื่อมหาวิทยาลัย'] == selected_uni]
    if keyword:
        filtered = filtered[filtered.apply(lambda row: keyword.lower() in str(row).lower(), axis=1)]

    # Apply data filter based on tuition info
    if data_filter == 'with_tuition':
        filtered = filtered[filtered['ค่าเทอมต่อเทอม_ประมาณ'].notna()]
    elif data_filter == 'without_tuition':
        filtered = filtered[filtered['ค่าเทอมต่อเทอม_ประมาณ'].isna()]

    # Statistics
    total_courses = len(filtered)
    total_universities = filtered['ชื่อมหาวิทยาลัย'].nunique()
    with_tuition = len(filtered[filtered['ค่าเทอมต่อเทอม_ประมาณ'].notna()])
    without_tuition = len(filtered[filtered['ค่าเทอมต่อเทอม_ประมาณ'].isna()])

    # Tuition chart (only for courses with tuition data)
    tuition_data = filtered[filtered['ค่าเทอมต่อเทอม_ประมาณ'].notna()]
    if len(tuition_data) > 0:
        tuition_avg = tuition_data.groupby("ประเภทหลักสูตร")["ค่าเทอมต่อเทอม_ประมาณ"].mean().reset_index()
        tuition_chart = px.bar(
            tuition_avg,
            x="ประเภทหลักสูตร",
            y="ค่าเทอมต่อเทอม_ประมาณ",
            labels={"ค่าเทอมต่อเทอม_ประมาณ": "ค่าเทอมเฉลี่ย (บาท)"},
            title="ค่าเทอมเฉลี่ยต่อประเภทหลักสูตร",
            color="ค่าเทอมต่อเทอม_ประมาณ",
            color_continuous_scale="viridis"
        )
        tuition_chart.update_layout(
            template='plotly_white',
            title_font_size=16,
            title_x=0.5,
            showlegend=False
        )
        tuition_chart.update_traces(
            hovertemplate='<b>%{x}</b><br>ค่าเทอมเฉลี่ย: %{y:,.0f} บาท<extra></extra>'
        )
    else:
        tuition_chart = go.Figure()
        tuition_chart.add_annotation(
            text="ไม่มีข้อมูลค่าเทอมในตัวกรองที่เลือก",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        tuition_chart.update_layout(template='plotly_white')

    # Tuition status chart
    status_data = pd.DataFrame({
        'สถานะ': ['มีข้อมูลค่าเทอม', 'ไม่ระบุค่าเทอม'],
        'จำนวน': [with_tuition, without_tuition],
        'สี': [colors['success'], colors['secondary']]
    })
    
    tuition_status_chart = px.pie(
        status_data,
        values='จำนวน',
        names='สถานะ',
        title="สัดส่วนข้อมูลค่าเทอม",
        color_discrete_sequence=[colors['success'], colors['secondary']]
    )
    tuition_status_chart.update_layout(
        template='plotly_white',
        title_font_size=16,
        title_x=0.5
    )
    tuition_status_chart.update_traces(
        hovertemplate='<b>%{label}</b><br>จำนวน: %{value} หลักสูตร<br>สัดส่วน: %{percent}<extra></extra>'
    )

    # Universities without tuition info
    no_tuition_unis = filtered[filtered['ค่าเทอมต่อเทอม_ประมาณ'].isna()]['ชื่อมหาวิทยาลัย'].value_counts()
    if len(no_tuition_unis) > 0:
        unis_without_tuition = dbc.Row([
            dbc.Col([
                dbc.Alert([
                    html.H6(f"🏛️ {uni}", className="alert-heading mb-1"),
                    html.P(f"จำนวนหลักสูตรที่ไม่ระบุค่าเทอม: {count} หลักสูตร", className="mb-0")
                ], color="warning", className="mb-2")
            ], md=6) for uni, count in no_tuition_unis.head(10).items()
        ])
        if len(no_tuition_unis) > 10:
            unis_without_tuition.children.append(
                dbc.Col([
                    dbc.Alert([
                        html.P(f"... และอีก {len(no_tuition_unis) - 10} มหาวิทยาลัย", className="mb-0 text-center")
                    ], color="info")
                ], md=12)
            )
    else:
        unis_without_tuition = dbc.Alert(
            "ไม่มีมหาวิทยาลัยที่ไม่ระบุค่าเทอมในตัวกรองที่เลือก",
            color="success"
        )

    # Format table data to show NaN values nicely
    table_data = filtered.copy()
    table_data['ค่าเทอมต่อเทอม_ประมาณ'] = table_data['ค่าเทอมต่อเทอม_ประมาณ'].fillna('ไม่ระบุ')
    
    # Reorder columns to put university name first
    columns_ordered = ['ชื่อมหาวิทยาลัย'] + [col for col in table_data.columns if col != 'ชื่อมหาวิทยาลัย']
    table_data = table_data[columns_ordered]
    
    return (
        f"{total_courses:,}",
        f"{total_universities:,}",
        f"{with_tuition:,}",
        f"{without_tuition:,}",
        table_data.to_dict('records'),
        tuition_chart,
        tuition_status_chart,
        unis_without_tuition
    )


if __name__ == '__main__':
    app.run(debug=True)