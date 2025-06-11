from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.read_csv('cleaned_df.csv')
col_hist = ['age', 'experience_years', 'loan_amount', 'loan_interest_rate']
df_hist = df[col_hist]


def create_correlation_matrix():
    numeric_data = df.select_dtypes(include=[np.number])
    correlation_matrix = numeric_data.corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            showscale=True,
            text=correlation_matrix.values,
            texttemplate="%{text:.2f}",
            colorbar=dict(title="Correlation"),
        )
    )

    fig.update_layout(
        xaxis_title="Features",
        yaxis_title="Features",
        autosize=True,
        height=455,
    )

    return fig


def create_histogram(data, feature):
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=data[feature],
        nbinsx=30,
        marker=dict(color='teal', opacity=0.7, line=dict(color='black', width=1)),
    ))

    fig.update_layout(
        title=f"Histogram of {feature}",
        xaxis_title=feature,
        yaxis_title="Frequency",
        template="plotly_white",
        bargap=0.2,
        height=400,
    )

    return fig


app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f9f9f9", "padding": "20px"},
    children=[
        html.H1(
            "Loan Data Dashboard",
            style={"textAlign": "center", "color": "#444", "marginBottom": "20px"}
        ),

        html.Div([
            html.Div([
                html.Label('Select Feature for Histogram:', style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id='hist-dropdown',
                    options=[{'label': col, 'value': col} for col in df_hist.columns],
                    value=df.columns[0],
                    style={"marginBottom": "10px"}
                ),
                dcc.Graph(id='histogram', style={"boxShadow": "0 2px 4px rgba(0,0,0,0.1)", "borderRadius": "5px"}),
            ], style={"width": "48%", "display": "inline-block", "padding": "10px"}),

            html.Div([
                html.Label('Select Scatter Plot:', style={"fontWeight": "bold", "marginBottom": "5px"}),
                dcc.Dropdown(
                    id='scatter-dropdown',
                    options=[
                        {'label': 'Age vs Experience Years', 'value': 'age_experience_years'},
                        {'label': 'Age vs Credit Length', 'value': 'age_credit_length'}
                    ],
                    value='age_experience_years',
                    style={"marginBottom": "10px"}
                ),
                dcc.Graph(id='scatter-plot', style={"boxShadow": "0 2px 4px rgba(0,0,0,0.1)", "borderRadius": "5px"}),
            ], style={"width": "48%", "display": "inline-block", "padding": "10px"}),
        ], style={"display": "flex", "justifyContent": "space-between"}),

        html.Div([
            html.Div([
                html.Label('Select Feature for Pie Chart:', style={"fontWeight": "bold"}),
                dcc.Dropdown(
                    id='pie-dropdown',
                    options=[
                        {'label': 'Gender', 'value': 'gender'},
                        {'label': 'Education Level', 'value': 'education_level'},
                        {'label': 'Previous Loan', 'value': 'previous_loan'},
                        {'label': 'Home Status', 'value': 'home_status'}
                    ],
                    value='gender',
                    style={"marginBottom": "10px"}
                ),
                dcc.Graph(id='pie-chart', style={"boxShadow": "0 2px 4px rgba(0,0,0,0.1)", "borderRadius": "5px"}),
            ], style={"width": "48%", "display": "inline-block", "padding": "10px"}),

            html.Div([
                html.H2("Correlation Matrix:", style={"textAlign": "inline-block", "marginBottom": "10px"}),
                html.Div(style={"textAlign": "center", "marginBottom": "10px", "color": "#555"}), 
                dcc.Graph(id='correlation-matrix', style={"boxShadow": "0 2px 4px rgba(0,0,0,0.1)", "borderRadius": "5px"}),
            ], style={"width": "48%", "display": "inline-block", "padding": "10px"}),
        ], style={"display": "flex", "justifyContent": "space-between"}), 
    ]
)


@app.callback(
    Output('histogram', 'figure'),
    Input('hist-dropdown', 'value')
)
def update_histogram(selected_feature):
    return create_histogram(df, selected_feature)


@app.callback(
    Output('pie-chart', 'figure'),
    [Input('pie-dropdown', 'value')]
)
def update_pie_chart(selected_feature):
    fig = px.pie(
        df,
        names=selected_feature,
        title=f"Distribution of {selected_feature}",
        hole=0.4
    )
    return fig


@app.callback(
    Output('correlation-matrix', 'figure'),
    Input('hist-dropdown', 'value')
)
def update_correlation_matrix(_):
    return create_correlation_matrix()


@app.callback(
    Output('scatter-plot', 'figure'),
    Input('scatter-dropdown', 'value')
)
def update_scatter_plot(selected_value):
    scatter_mapping = {
        'age_experience_years': ('age', 'experience_years', 'Age vs Experience Years'),
        'age_credit_length': ('age', 'credit_length', 'Age vs Credit Length')
    }
    x_col, y_col, title = scatter_mapping[selected_value]
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color='gender',
        title=title,
        height=400,
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)




