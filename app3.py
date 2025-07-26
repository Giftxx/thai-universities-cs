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

# Green Theme Color Palette
colors = {
    'primary': '#2E8B57',      # Sea Green
    'secondary': '#228B22',    # Forest Green
    'success': '#32CD32',      # Lime Green
    'info': '#20B2AA',         # Light Sea Green
    'light': '#F0FFF0',        # Honeydew
    'dark': '#006400',         # Dark Green
    'accent': '#90EE90',       # Light Green
    'gradient_primary': 'linear-gradient(135deg, #2E8B57 0%, #228B22 100%)',
    'gradient_card': 'linear-gradient(135deg, #F0FFF0 0%, #E8F5E8 100%)',
    'chart_green': ['#2E8B57', '#228B22', '#32CD32', '#20B2AA', '#90EE90', '#8FBC8F', '#98FB98']
}

# Enhanced Layout with Green Theme
app.layout = dbc.Container([
    # Animated Header Section
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.H1("🌿 ระบบข้อมูลหลักสูตรมหาวิทยาลัย", 
                           className="text-center text-white mb-2",
                           style={
                               'font-size': '2.8rem', 
                               'font-weight': 'bold',
                               'text-shadow': '2px 2px 4px rgba(0,0,0,0.3)',
                               'animation': 'fadeInDown 1s ease-in-out'
                           }),
                    html.P("🎓 ระบบติดตามและวิเคราะห์ข้อมูลหลักสูตรและค่าเทอมมหาวิทยาลัย",
                          className="text-center text-white-75 mb-0",
                          style={'font-size': '1.2rem'})
                ], style={'position': 'relative', 'z-index': '2'})
            ], style={
                'background': colors['gradient_primary'],
                'padding': '4rem 2rem',
                'border-radius': '20px',
                'box-shadow': '0 15px 35px rgba(46, 139, 87, 0.3)',
                'margin-bottom': '2rem',
                'position': 'relative',
                'overflow': 'hidden'
            }, id='header-section')
        ], width=12)
    ]),

    # Enhanced Statistics Cards with Animation
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-graduation-cap fa-2x text-success mb-2"),
                        html.H3(id='total-courses', className="text-success mb-0", style={'font-weight': 'bold'}),
                        html.P("หลักสูตรทั้งหมด", className="text-muted mb-0", style={'font-size': '0.9rem'})
                    ], className="text-center")
                ])
            ], className="shadow-lg border-0 h-100", 
               style={
                   'border-radius': '15px',
                   'background': colors['gradient_card'],
                   'transition': 'transform 0.3s ease-in-out',
                   'border-left': f'4px solid {colors["success"]}'
               })
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-university fa-2x text-primary mb-2"),
                        html.H3(id='total-universities', className="text-primary mb-0", style={'font-weight': 'bold'}),
                        html.P("มหาวิทยาลัยทั้งหมด", className="text-muted mb-0", style={'font-size': '0.9rem'})
                    ], className="text-center")
                ])
            ], className="shadow-lg border-0 h-100", 
               style={
                   'border-radius': '15px',
                   'background': colors['gradient_card'],
                   'transition': 'transform 0.3s ease-in-out',
                   'border-left': f'4px solid {colors["primary"]}'
               })
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-check-circle fa-2x text-info mb-2"),
                        html.H3(id='with-tuition', className="text-info mb-0", style={'font-weight': 'bold'}),
                        html.P("มีข้อมูลค่าเทอม", className="text-muted mb-0", style={'font-size': '0.9rem'})
                    ], className="text-center")
                ])
            ], className="shadow-lg border-0 h-100", 
               style={
                   'border-radius': '15px',
                   'background': colors['gradient_card'],
                   'transition': 'transform 0.3s ease-in-out',
                   'border-left': f'4px solid {colors["info"]}'
               })
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-question-circle fa-2x text-warning mb-2"),
                        html.H3(id='without-tuition', className="text-warning mb-0", style={'font-weight': 'bold'}),
                        html.P("ไม่ระบุค่าเทอม", className="text-muted mb-0", style={'font-size': '0.9rem'})
                    ], className="text-center")
                ])
            ], className="shadow-lg border-0 h-100", 
               style={
                   'border-radius': '15px',
                   'background': colors['gradient_card'],
                   'transition': 'transform 0.3s ease-in-out',
                   'border-left': '4px solid #ffc107'
               })
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-chart-line fa-2x text-danger mb-2"),
                        html.H3(id='avg-tuition', className="text-danger mb-0", style={'font-weight': 'bold'}),
                        html.P("ค่าเทอมเฉลี่ย", className="text-muted mb-0", style={'font-size': '0.9rem'})
                    ], className="text-center")
                ])
            ], className="shadow-lg border-0 h-100", 
               style={
                   'border-radius': '15px',
                   'background': colors['gradient_card'],
                   'transition': 'transform 0.3s ease-in-out',
                   'border-left': '4px solid #dc3545'
               })
        ], md=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-crown fa-2x text-dark mb-2"),
                        html.H3(id='most-expensive', className="text-dark mb-0", style={'font-weight': 'bold'}),
                        html.P("ค่าเทอมสูงสุด", className="text-muted mb-0", style={'font-size': '0.9rem'})
                    ], className="text-center")
                ])
            ], className="shadow-lg border-0 h-100", 
               style={
                   'border-radius': '15px',
                   'background': colors['gradient_card'],
                   'transition': 'transform 0.3s ease-in-out',
                   'border-left': '4px solid #343a40'
               })
        ], md=2)
    ], className="mb-4"),

    # Enhanced Filter Section with Green Theme
    dbc.Card([
        dbc.CardHeader([
            html.Div([
                html.I(className="fas fa-filter me-2"),
                html.H5("🔍 ตัวกรองข้อมูล", className="mb-0 d-inline", style={'color': colors['primary']})
            ])
        ], style={'background': colors['light'], 'border': 'none'}),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("ประเภทหลักสูตร", className="fw-bold mb-2", style={'color': colors['dark']}),
                    dcc.Dropdown(
                        options=[{'label': i, 'value': i} for i in sorted(df['ประเภทหลักสูตร'].unique())],
                        id='type-filter',
                        placeholder="เลือกประเภทหลักสูตร",
                        style={'border-radius': '10px'},
                        className="custom-dropdown",
                        maxHeight=300,
                        optionHeight=35
                    ),
                ], md=3),

                dbc.Col([
                    html.Label("ชื่อมหาวิทยาลัย", className="fw-bold mb-2", style={'color': colors['dark']}),
                    dcc.Dropdown(
                        options=[{'label': i, 'value': i} for i in sorted(df['ชื่อมหาวิทยาลัย'].unique())],
                        id='uni-filter',
                        placeholder="เลือกมหาวิทยาลัย",
                        style={'border-radius': '10px'},
                        className="custom-dropdown",
                        maxHeight=300,
                        optionHeight=35
                    ),
                ], md=3),

                dbc.Col([
                    html.Label("คำค้นหา", className="fw-bold mb-2", style={'color': colors['dark']}),
                    dcc.Input(
                        id='search-input',
                        type='text',
                        placeholder='🔍 ค้นหาคำสำคัญ...',
                        debounce=True,
                        className='form-control',
                        style={
                            'border-radius': '10px',
                            'border': f'2px solid {colors["accent"]}',
                            'box-shadow': f'0 0 0 0.2rem rgba(46, 139, 87, 0.25)'
                        }
                    )
                ], md=3),

                dbc.Col([
                    html.Label("ช่วงค่าเทอม (บาท)", className="fw-bold mb-2", style={'color': colors['dark']}),
                    dcc.RangeSlider(
                        id='tuition-range',
                        min=0,
                        max=100000,
                        step=5000,
                        value=[0, 100000],
                        marks={i: f'{i//1000}k' for i in range(0, 101000, 20000)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], md=3)
            ])
        ], style={'background': colors['light']})
    ], className="mb-4 shadow-lg", style={'border-radius': '15px', 'border': 'none'}),

    # Data Filter Toggle with Green Theme
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("🎯 แสดงข้อมูล:", 
                                     className="fw-bold mb-0", 
                                     style={'color': colors['primary'], 'font-size': '1.1rem'}),
                        ], md=2),
                        dbc.Col([
                            dbc.RadioItems(
                                id='data-filter',
                                options=[
                                    {'label': '📊 ทั้งหมด', 'value': 'all'},
                                    {'label': '💰 มีค่าเทอม', 'value': 'with_tuition'},
                                    {'label': '❓ ไม่ระบุค่าเทอม', 'value': 'without_tuition'}
                                ],
                                value='all',
                                inline=True,
                                style={'margin-left': '10px'},
                                className="custom-radio"
                            )
                        ], md=10)
                    ])
                ], style={'background': colors['light']})
            ], className="shadow-lg", style={'border-radius': '15px', 'border': 'none'})
        ])
    ], className="mb-4"),

    # Main Charts Section - Green Theme (First Row)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.I(className="fas fa-chart-bar me-2", style={'color': colors['primary']}),
                        html.H5("📊 ค่าเทอมเฉลี่ยตามประเภทหลักสูตร", className="mb-0 d-inline", 
                               style={'color': colors['primary']})
                    ])
                ], style={'background': colors['light'], 'border': 'none'}),
                dbc.CardBody([
                    dcc.Graph(id='tuition-chart')
                ], style={'background': colors['light']})
            ], className="shadow-lg h-100", style={'border-radius': '15px', 'border': 'none'})
        ], md=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.I(className="fas fa-pie-chart me-2", style={'color': colors['primary']}),
                        html.H5("🏫 สถิติข้อมูลค่าเทอม", className="mb-0 d-inline", 
                               style={'color': colors['primary']})
                    ])
                ], style={'background': colors['light'], 'border': 'none'}),
                dbc.CardBody([
                    dcc.Graph(id='tuition-status-chart')
                ], style={'background': colors['light']})
            ], className="shadow-lg h-100", style={'border-radius': '15px', 'border': 'none'})
        ], md=4)
    ], className="mb-4"),

    # New Enhanced Charts Section (Second Row)
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.I(className="fas fa-chart-area me-2", style={'color': colors['primary']}),
                        html.H5("🌊 การกระจายตัวของค่าเทอม", className="mb-0 d-inline", 
                               style={'color': colors['primary']})
                    ])
                ], style={'background': colors['light'], 'border': 'none'}),
                dbc.CardBody([
                    dcc.Graph(id='tuition-distribution-chart')
                ], style={'background': colors['light']})
            ], className="shadow-lg h-100", style={'border-radius': '15px', 'border': 'none'})
        ], md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.I(className="fas fa-chart-line me-2", style={'color': colors['primary']}),
                        html.H5("🏆 ค่าเทอมเฉลี่ยตามมหาวิทยาลัย (Top 10)", className="mb-0 d-inline", 
                               style={'color': colors['primary']})
                    ])
                ], style={'background': colors['light'], 'border': 'none'}),
                dbc.CardBody([
                    dcc.Graph(id='university-comparison-chart')
                ], style={'background': colors['light']})
            ], className="shadow-lg h-100", style={'border-radius': '15px', 'border': 'none'})
        ], md=6)
    ], className="mb-4"),

    # Additional New Charts Section (Third Row)
    dbc.Row([        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.I(className="fas fa-graduation-cap me-2", style={'color': colors['primary']}),
                        html.H5("🎓 จำนวนหลักสูตรตามมหาวิทยาลัย", className="mb-0 d-inline", 
                               style={'color': colors['primary']})
                    ])
                ], style={'background': colors['light'], 'border': 'none'}),
                dbc.CardBody([
                    dcc.Graph(id='courses-per-university-chart')
                ], style={'background': colors['light']})
            ], className="shadow-lg h-100", style={'border-radius': '15px', 'border': 'none'})
        ], md=12)
    ], className="mb-4"),

    # Statistics Section - Enhanced Green Theme
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.I(className="fas fa-calculator me-2", style={'color': colors['primary']}),
                        html.H5("📈 สถิติค่าเทอมละเอียด", className="mb-0 d-inline", 
                               style={'color': colors['primary']})
                    ])
                ], style={'background': colors['light'], 'border': 'none'}),
                dbc.CardBody([
                    html.Div(id='tuition-statistics')
                ], style={'background': colors['light']})
            ], className="shadow-lg", style={'border-radius': '15px', 'border': 'none'})
        ])
    ], className="mb-4"),

    # Data Table Section - Green Theme
    dbc.Card([
        dbc.CardHeader([
            html.Div([
                html.I(className="fas fa-table me-2", style={'color': colors['primary']}),
                html.H5("📋 ตารางข้อมูลหลักสูตร", className="mb-0 d-inline", 
                       style={'color': colors['primary']})
            ])
        ], style={'background': colors['light'], 'border': 'none'}),
        dbc.CardBody([
            dash_table.DataTable(
                id='course-table',
                columns=[
                    {"name": i, "id": i, 
                     'presentation': 'markdown' if i == 'URL' else 'input',
                     'type': 'text'}
                    for i in ['ชื่อมหาวิทยาลัย'] + [col for col in df.columns if col != 'ชื่อมหาวิทยาลัย']
                ],
                data=df.to_dict('records'),
                page_size=20,
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left', 
                    'padding': '15px',
                    'font-family': 'Arial, sans-serif',
                    'font-size': '14px',
                    'border': f'1px solid {colors["accent"]}'
                },
                style_header={
                    'backgroundColor': colors['primary'],
                    'color': 'white',
                    'fontWeight': 'bold',
                    'text-align': 'center',
                    'border': f'1px solid {colors["primary"]}'
                },
                style_data_conditional=[
                    {
                        'if': {'column_id': 'ค่าเทอมต่อเทอม_ประมาณ'},
                        'color': colors['dark'],
                        'fontWeight': 'bold',
                        'backgroundColor': colors['light']
                    },
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': colors['light']
                    },
                    {
                        'if': {'row_index': 'even'},
                        'backgroundColor': 'white'
                    }
                ],
                filter_action="native",
                sort_action="native",
                page_action="native",
                style_as_list_view=True
            )
        ], style={'background': 'white'})
    ], className="mb-4 shadow-lg", style={'border-radius': '15px', 'border': 'none'}),

    # Universities without tuition info - Green Theme
    dbc.Card([
        dbc.CardHeader([
            html.Div([
                html.I(className="fas fa-exclamation-triangle me-2", style={'color': '#ffc107'}),
                html.H5("🏛️ มหาวิทยาลัยที่ไม่ระบุค่าเทอม", className="mb-0 d-inline", 
                       style={'color': '#ffc107'})
            ])
        ], style={'background': colors['light'], 'border': 'none'}),
        dbc.CardBody([
            html.Div(id='universities-without-tuition')
        ], style={'background': colors['light']})
    ], className="shadow-lg", style={'border-radius': '15px', 'border': 'none'})

], fluid=True, style={
    'padding': '2rem', 
    'background': f'linear-gradient(135deg, {colors["light"]} 0%, #E8F5E8 100%)',
    'min-height': '100vh'
})


# Enhanced Callbacks with Additional Charts
@app.callback(
    [Output('total-courses', 'children'),
     Output('total-universities', 'children'),
     Output('with-tuition', 'children'),
     Output('without-tuition', 'children'),
     Output('avg-tuition', 'children'),
     Output('most-expensive', 'children'),
     Output('course-table', 'data'),
     Output('tuition-chart', 'figure'),
     Output('tuition-status-chart', 'figure'),
     Output('tuition-distribution-chart', 'figure'),
     Output('university-comparison-chart', 'figure'),
     Output('courses-per-university-chart', 'figure'),
     Output('tuition-statistics', 'children'),
     Output('universities-without-tuition', 'children')],
    [Input('type-filter', 'value'),
     Input('uni-filter', 'value'),
     Input('search-input', 'value'),
     Input('data-filter', 'value'),
     Input('tuition-range', 'value')]
)
def update_dashboard(selected_type, selected_uni, keyword, data_filter, tuition_range):
    filtered = df.copy()

    # Apply filters
    if selected_type:
        filtered = filtered[filtered['ประเภทหลักสูตร'] == selected_type]
    if selected_uni:
        filtered = filtered[filtered['ชื่อมหาวิทยาลัย'] == selected_uni]
    if keyword:
        filtered = filtered[filtered.apply(lambda row: keyword.lower() in str(row).lower(), axis=1)]
    
    # Apply tuition range filter
    if tuition_range:
        tuition_filtered = filtered[filtered['ค่าเทอมต่อเทอม_ประมาณ'].notna()]
        tuition_filtered = tuition_filtered[
            (tuition_filtered['ค่าเทอมต่อเทอม_ประมาณ'] >= tuition_range[0]) &
            (tuition_filtered['ค่าเทอมต่อเทอม_ประมาณ'] <= tuition_range[1])
        ]
        no_tuition = filtered[filtered['ค่าเทอมต่อเทอม_ประมาณ'].isna()]
        filtered = pd.concat([tuition_filtered, no_tuition])

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
    
    # Additional statistics
    tuition_data = filtered[filtered['ค่าเทอมต่อเทอม_ประมาณ'].notna()]
    avg_tuition = tuition_data['ค่าเทอมต่อเทอม_ประมาณ'].mean() if len(tuition_data) > 0 else 0
    max_tuition = tuition_data['ค่าเทอมต่อเทอม_ประมาณ'].max() if len(tuition_data) > 0 else 0

    # 1. Enhanced Tuition chart with Green Theme
    if len(tuition_data) > 0:
        tuition_avg = tuition_data.groupby("ประเภทหลักสูตร")["ค่าเทอมต่อเทอม_ประมาณ"].mean().reset_index()
        
        tuition_chart = px.bar(
            tuition_avg,
            x="ประเภทหลักสูตร",
            y="ค่าเทอมต่อเทอม_ประมาณ",
            labels={"ค่าเทอมต่อเทอม_ประมาณ": "ค่าเทอมเฉลี่ย (บาท)"},
            title="💰 ค่าเทอมเฉลี่ยต่อประเภทหลักสูตร",
            color="ค่าเทอมต่อเทอม_ประมาณ",
            color_continuous_scale=[[0, colors['success']], [0.5, colors['primary']], [1, colors['dark']]]
        )
        
        tuition_chart.update_layout(
            template='plotly_white',
            title_font_size=18,
            title_x=0.5,
            showlegend=False,
            plot_bgcolor=colors['light'],
            paper_bgcolor=colors['light'],
            font=dict(size=12),
            title_font_color=colors['primary'],
            xaxis=dict(gridcolor=colors['accent']),
            yaxis=dict(gridcolor=colors['accent'])
        )
        
        tuition_chart.update_traces(
            hovertemplate='<b>%{x}</b><br>ค่าเทอมเฉลี่ย: %{y:,.0f} บาท<extra></extra>',
            marker_line_color=colors['primary'],
            marker_line_width=2
        )
    else:
        tuition_chart = go.Figure()
        tuition_chart.add_annotation(
            text="ไม่มีข้อมูลค่าเทอมในตัวกรองที่เลือก",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=colors['primary'])
        )
        tuition_chart.update_layout(
            template='plotly_white',
            plot_bgcolor=colors['light'],
            paper_bgcolor=colors['light']
        )

    # 2. Enhanced Tuition status chart with Green Theme
    status_data = pd.DataFrame({
        'สถานะ': ['✅ มีข้อมูลค่าเทอม', '❓ ไม่ระบุค่าเทอม'],
        'จำนวน': [with_tuition, without_tuition]
    })
    
    tuition_status_chart = px.pie(
        status_data,
        values='จำนวน',
        names='สถานะ',
        title="🎯 สัดส่วนข้อมูลค่าเทอม",
        color_discrete_sequence=[colors['success'], '#ffc107']
    )
    
    tuition_status_chart.update_layout(
        template='plotly_white',
        title_font_size=16,
        title_x=0.5,
        plot_bgcolor=colors['light'],
        paper_bgcolor=colors['light'],
        title_font_color=colors['primary']
    )
    
    tuition_status_chart.update_traces(
        hovertemplate='<b>%{label}</b><br>จำนวน: %{value} หลักสูตร<br>สัดส่วน: %{percent}<extra></extra>',
        textfont_size=14,
        marker=dict(line=dict(color=colors['primary'], width=2))
    )

    # 3. NEW: Tuition Distribution Chart (Histogram + KDE-like)
    if len(tuition_data) > 0:
        tuition_distribution_chart = px.histogram(
            tuition_data,
            x="ค่าเทอมต่อเทอม_ประมาณ",
            nbins=20,
            title="🌊 การกระจายตัวของค่าเทอม",
            labels={"ค่าเทอมต่อเทอม_ประมาณ": "ค่าเทอม (บาท)", "count": "จำนวนหลักสูตร"},
            color_discrete_sequence=[colors['primary']]
        )
        
        # Add mean line
        tuition_distribution_chart.add_vline(
            x=avg_tuition, 
            line_dash="dash", 
            line_color=colors['dark'],
            annotation_text=f"เฉลี่ย: {avg_tuition:,.0f} บาท",
            annotation_position="top"
        )
        
        tuition_distribution_chart.update_layout(
            template='plotly_white',
            title_font_size=16,
            title_x=0.5,
            plot_bgcolor=colors['light'],
            paper_bgcolor=colors['light'],
            title_font_color=colors['primary'],
            xaxis=dict(gridcolor=colors['accent']),
            yaxis=dict(gridcolor=colors['accent'])
        )
        
        tuition_distribution_chart.update_traces(
            hovertemplate='<b>ช่วงค่าเทอม:</b> %{x} บาท<br><b>จำนวนหลักสูตร:</b> %{y}<extra></extra>',
            marker_line_color=colors['dark'],
            marker_line_width=1
        )
    else:
        tuition_distribution_chart = go.Figure()
        tuition_distribution_chart.add_annotation(
            text="ไม่มีข้อมูลค่าเทอมสำหรับแสดงการกระจาย",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=colors['primary'])
        )
        tuition_distribution_chart.update_layout(
            template='plotly_white',
            plot_bgcolor=colors['light'],
            paper_bgcolor=colors['light']
        )

    # 4. NEW: University Comparison Chart (Top 10)
    if len(tuition_data) > 0:
        uni_avg = tuition_data.groupby("ชื่อมหาวิทยาลัย")["ค่าเทอมต่อเทอม_ประมาณ"].agg(['mean', 'count']).reset_index()
        uni_avg = uni_avg[uni_avg['count'] >= 2]  # At least 2 courses
        uni_avg = uni_avg.nlargest(10, 'mean')
        
        university_comparison_chart = px.bar(
            uni_avg,
            x="mean",
            y="ชื่อมหาวิทยาลัย",
            orientation='h',
            title="🏆 ค่าเทอมเฉลี่ยสูงสุด 10 อันดับ",
            labels={"mean": "ค่าเทอมเฉลี่ย (บาท)", "ชื่อมหาวิทยาลัย": "มหาวิทยาลัย"},
            color="mean",
            color_continuous_scale=[[0, colors['success']], [0.5, colors['info']], [1, colors['dark']]]
        )
        
        university_comparison_chart.update_layout(
            template='plotly_white',
            title_font_size=16,
            title_x=0.5,
            showlegend=False,
            plot_bgcolor=colors['light'],
            paper_bgcolor=colors['light'],
            title_font_color=colors['primary'],
            height=400,
            xaxis=dict(gridcolor=colors['accent']),
            yaxis=dict(gridcolor=colors['accent'])
        )
        
        university_comparison_chart.update_traces(
            hovertemplate='<b>%{y}</b><br>ค่าเทอมเฉลี่ย: %{x:,.0f} บาท<extra></extra>',
            marker_line_color=colors['primary'],
            marker_line_width=1
        )
    else:
        university_comparison_chart = go.Figure()
        university_comparison_chart.add_annotation(
            text="ไม่มีข้อมูลเพียงพอสำหรับเปรียบเทียบมหาวิทยาลัย",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=colors['primary'])
        )
        university_comparison_chart.update_layout(
            template='plotly_white',
            plot_bgcolor=colors['light'],
            paper_bgcolor=colors['light']
        )

    # 5. NEW: Courses per University Chart
    courses_per_uni = filtered['ชื่อมหาวิทยาลัย'].value_counts().head(15).reset_index()
    courses_per_uni.columns = ['ชื่อมหาวิทยาลัย', 'จำนวนหลักสูตร']
    
    courses_per_university_chart = px.bar(
        courses_per_uni,
        x="จำนวนหลักสูตร",
        y="ชื่อมหาวิทยาลัย",
        orientation='h',
        title="🎓 มหาวิทยาลัยที่มีหลักสูตรมากที่สุด (Top 15)",
        labels={"จำนวนหลักสูตร": "จำนวนหลักสูตร", "ชื่อมหาวิทยาลัย": "มหาวิทยาลัย"},
        color="จำนวนหลักสูตร",
        color_continuous_scale=[[0, colors['accent']], [0.5, colors['success']], [1, colors['primary']]]
    )
    
    courses_per_university_chart.update_layout(
        template='plotly_white',
        title_font_size=16,
        title_x=0.5,
        showlegend=False,
        plot_bgcolor=colors['light'],
        paper_bgcolor=colors['light'],
        title_font_color=colors['primary'],
        height=600,
        xaxis=dict(gridcolor=colors['accent']),
        yaxis=dict(gridcolor=colors['accent'])
    )
    
    courses_per_university_chart.update_traces(
        hovertemplate='<b>%{y}</b><br>จำนวนหลักสูตร: %{x}<extra></extra>',
        marker_line_color=colors['primary'],
        marker_line_width=1
    )

    # 7. Enhanced Tuition statistics with Green Theme
    if len(tuition_data) > 0:
        median_tuition = tuition_data['ค่าเทอมต่อเทอม_ประมาณ'].median()
        std_tuition = tuition_data['ค่าเทอมต่อเทอม_ประมาณ'].std()
        min_tuition = tuition_data['ค่าเทอมต่อเทอม_ประมาณ'].min()
        q1_tuition = tuition_data['ค่าเทอมต่อเทอม_ประมาณ'].quantile(0.25)
        q3_tuition = tuition_data['ค่าเทอมต่อเทอม_ประมาณ'].quantile(0.75)
        
        tuition_statistics = html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(f"{avg_tuition:,.0f}", className="text-success mb-1"),
                            html.P("📊 ค่าเฉลี่ย (บาท)", className="mb-0 text-muted")
                        ], className="text-center")
                    ], style={'background': colors['light'], 'border': f'2px solid {colors["success"]}', 'border-radius': '10px'})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(f"{median_tuition:,.0f}", className="text-primary mb-1"),
                            html.P("📈 ค่ามัธยฐาน (บาท)", className="mb-0 text-muted")
                        ], className="text-center")
                    ], style={'background': colors['light'], 'border': f'2px solid {colors["primary"]}', 'border-radius': '10px'})
                ], md=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(f"{std_tuition:,.0f}", className="text-info mb-1"),
                            html.P("📏 ส่วนเบี่ยงเบน (บาท)", className="mb-0 text-muted")
                        ], className="text-center")
                    ], style={'background': colors['light'], 'border': f'2px solid {colors["info"]}', 'border-radius': '10px'})
                ], md=4)
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{min_tuition:,.0f}", className="text-success mb-1"),
                            html.P("💚 ต่ำสุด", className="mb-0 text-muted")
                        ], className="text-center")
                    ], style={'background': colors['light'], 'border': f'1px solid {colors["success"]}', 'border-radius': '10px'})
                ], md=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{q1_tuition:,.0f}", className="text-warning mb-1"),
                            html.P("📊 Q1 (25%)", className="mb-0 text-muted")
                        ], className="text-center")
                    ], style={'background': colors['light'], 'border': '1px solid #ffc107', 'border-radius': '10px'})
                ], md=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{q3_tuition:,.0f}", className="text-warning mb-1"),
                            html.P("📈 Q3 (75%)", className="mb-0 text-muted")
                        ], className="text-center")
                    ], style={'background': colors['light'], 'border': '1px solid #ffc107', 'border-radius': '10px'})
                ], md=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{max_tuition:,.0f}", className="text-danger mb-1"),
                            html.P("🔥 สูงสุด", className="mb-0 text-muted")
                        ], className="text-center")
                    ], style={'background': colors['light'], 'border': '1px solid #dc3545', 'border-radius': '10px'})
                ], md=3)
            ])
        ])
    else:
        tuition_statistics = html.Div([
            dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                "ไม่มีข้อมูลค่าเทอมในตัวกรองที่เลือก"
            ], color="warning", className="text-center")
        ])

    # 8. Universities without tuition info - Enhanced Green Theme
    no_tuition_unis = filtered[filtered['ค่าเทอมต่อเทอม_ประมาณ'].isna()]['ชื่อมหาวิทยาลัย'].value_counts()
    if len(no_tuition_unis) > 0:
        unis_cards = []
        for i, (uni, count) in enumerate(no_tuition_unis.head(12).items()):
            color_variants = ['warning', 'info', 'secondary']
            card_color = color_variants[i % len(color_variants)]
            
            unis_cards.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="fas fa-university fa-2x mb-2", style={'color': '#ffc107'}),
                                html.H6(f"{uni}", className="card-title mb-2", style={'color': colors['dark']}),
                                html.P([
                                    html.Span("📊 จำนวนหลักสูตร: ", className="fw-bold"),
                                    html.Span(f"{count} หลักสูตร", className="text-danger fw-bold")
                                ], className="mb-0")
                            ], className="text-center")
                        ])
                    ], className="shadow h-100", 
                       style={
                           'border-radius': '12px',
                           'background': colors['light'],
                           'border': f'2px solid #ffc107',
                           'transition': 'transform 0.3s ease-in-out'
                       })
                ], md=4, className="mb-3")
            )
        
        if len(no_tuition_unis) > 12:
            unis_cards.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.I(className="fas fa-plus-circle fa-3x mb-2", style={'color': colors['info']}),
                                html.H5(f"+ อีก {len(no_tuition_unis) - 12}", className="text-info mb-1"),
                                html.P("มหาวิทยาลัย", className="mb-0 text-muted")
                            ], className="text-center")
                        ])
                    ], className="shadow h-100", 
                       style={
                           'border-radius': '12px',
                           'background': colors['light'],
                           'border': f'2px dashed {colors["info"]}',
                           'transition': 'transform 0.3s ease-in-out'
                       })
                ], md=4, className="mb-3")
            )
        
        unis_without_tuition = dbc.Row(unis_cards)
    else:
        unis_without_tuition = dbc.Alert([
            html.I(className="fas fa-check-circle me-2"),
            "🎉 ไม่มีมหาวิทยาลัยที่ไม่ระบุค่าเทอมในตัวกรองที่เลือก"
        ], color="success", className="text-center")

    # Format table data to show NaN values nicely
    table_data = filtered.copy()
    table_data['ค่าเทอมต่อเทอม_ประมาณ'] = table_data['ค่าเทอมต่อเทอม_ประมาณ'].fillna('❌ ไม่ระบุ')
    
    # Reorder columns to put university name first
    columns_ordered = ['ชื่อมหาวิทยาลัย'] + [col for col in table_data.columns if col != 'ชื่อมหาวิทยาลัย']
    table_data = table_data[columns_ordered]
    
    return (
        f"{total_courses:,}",
        f"{total_universities:,}",
        f"{with_tuition:,}",
        f"{without_tuition:,}",
        f"฿{avg_tuition:,.0f}" if avg_tuition > 0 else "ไม่มีข้อมูล",
        f"฿{max_tuition:,.0f}" if max_tuition > 0 else "ไม่มีข้อมูล",
        table_data.to_dict('records'),
        tuition_chart,
        tuition_status_chart,
        tuition_distribution_chart,
        university_comparison_chart,
        courses_per_university_chart,
        tuition_statistics,
        unis_without_tuition
    )


# Add custom CSS for enhanced styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            @keyframes fadeInDown {
                from {
                    opacity: 0;
                    transform: translate3d(0, -100%, 0);
                }
                to {
                    opacity: 1;
                    transform: translate3d(0, 0, 0);
                }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translate3d(0, 100%, 0);
                }
                to {
                    opacity: 1;
                    transform: translate3d(0, 0, 0);
                }
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 40px rgba(46, 139, 87, 0.2) !important;
            }
            
            .custom-dropdown .Select-control {
                border: 2px solid #90EE90 !important;
                border-radius: 10px !important;
            }
            
            .custom-dropdown .Select-menu {
                max-height: 300px !important;
                overflow-y: auto !important;
                z-index: 9999 !important;
            }
            
            .custom-dropdown .Select-option {
                padding: 10px 12px !important;
                font-size: 14px !important;
            }
            
            .custom-dropdown .Select-option:hover {
                background-color: #E8F5E8 !important;
                color: #2E8B57 !important;
            }
            
            .custom-radio input[type="radio"]:checked + label {
                color: #2E8B57 !important;
                font-weight: bold !important;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table {
                border-collapse: separate !important;
                border-spacing: 0 2px !important;
            }
            
            .dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner tr {
                box-shadow: 0 2px 4px rgba(46, 139, 87, 0.1);
                border-radius: 8px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)