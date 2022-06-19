'''
This file contains code to deploy a fully-interactive dashboard for HR Dataset using Plotly Dash.
For detail analysis, please go through the hr.ipynb file present in the same folder.
'''

# ******************************************************************************************************


# Import the important Libraries

from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
import scipy
import plotly.figure_factory as ff

# *******************************************************************************************************

# Initialize the Dash App with an externsl CSS stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# *******************************************************************************************************

# Load the Dataset
hr = pd.read_csv('HRDataset_v14.csv')

# Data Preprocessing, details in hr.ipynb file
hr['Department'] = hr['Department'].str.strip()
hr['DOB'] = pd.to_datetime(hr['DOB'])
hr['DateofHire'] = pd.to_datetime(hr['DateofHire'])
hr['DateofTermination'] = pd.to_datetime(hr['DateofTermination'])
hr['DOB'] = hr['DOB'].astype(str).str.replace(r'^\d{2}', '19', regex=True)
hr['DOB'] = pd.to_datetime(hr['DOB'])
hr['Age'] = 2022 - hr['DOB'].dt.year

# *******************************************************************************************************

# Generating the static plots
total_emp = hr['EmpID'].count()
fig1 = go.Figure(data=[go.Indicator(mode='number', value=total_emp,)],
                 layout=go.Layout(title=dict(text='Total Employees', x=0.5,), ))
fig1.update_layout(paper_bgcolor="#000080", font_color='yellow', font_size = 14)

present_emp = len(hr[hr['DateofTermination'].isna()])
fig2 = go.Figure(data=[go.Indicator(mode='number', value=present_emp)],
                 layout=go.Layout(title=dict(text='Present Employees', x=0.5)))
fig2.update_layout(paper_bgcolor="#000080", font_color='yellow', font_size = 14)

total_dep = hr['Department'].nunique()
fig3 = go.Figure(data=[go.Indicator(mode='number', value=total_dep)],
                 layout=go.Layout(title=dict(text='Total Departments', x=0.5)))
fig3.update_layout(paper_bgcolor="#000080", font_color='yellow', font_size = 14)

fig4= go.Figure(data=[go.Indicator(mode='number', value=hr['PerfScoreID'].mean())],
                 layout=go.Layout(title=dict(text='Mean Performance Score', x=0.5)))
fig4.update_layout(paper_bgcolor="#000080", font_color='yellow', font_size = 14)

fig5 = go.Figure(data=[go.Indicator(mode='number', value=hr['EmpSatisfaction'].mean())],
                 layout=go.Layout(title=dict(text='Mean Emp Satisfaction', x=0.5)))
fig5.update_layout(paper_bgcolor="#000080", font_color='yellow', font_size = 14)

emp_per_dep = hr.groupby('Department')['EmpID'].count()
fig6 = go.Figure(data=[go.Bar(x=emp_per_dep.index, y=emp_per_dep.values, marker_color='yellow')],
                 layout=go.Layout(title=dict(text='Total Employees per Department', x=0.5), yaxis=dict(range=[0, 220])))
fig6.update_layout(paper_bgcolor="#000080", font_color='yellow', font_size = 14)

emp_per_sex = hr.groupby('Sex')['EmpID'].count()
fig7 = go.Figure(data=[go.Pie(labels=['Females', 'Males'], values=emp_per_sex.values, marker = dict(colors = ['yellow','green']))],
                 layout=go.Layout(title=dict(text='Employees by Gender', x=0.5)))
fig7.update_layout(paper_bgcolor="#000080", font_color='yellow', font_size = 14)

dep_options = []
for dep in hr['Department'].unique():
    dep_options.append({'label': dep, 'value': dep})

# *******************************************************************************************************

#markdown text
markdown_text = '''
This dashboard present the analysis of HR Dataset. The dataset is taken from [Kaggle](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set).
It contains 311 rows and 35 columns. 
'''

# *******************************************************************************************************


# Structure the layout for the Dashboard
app.layout = html.Div(children=[html.Div([

    html.Div([

        html.H1(children='HR DATASET ANALYSIS',
                style={'textAlign': 'center',
                       'fontSize': '30px',
                       'fontWeight': 'bold',
                       'color': '#000080',
                       }),

        html.Div([
            dcc.Markdown(children = markdown_text,
                style = {'textAlign': 'center',
                       'fontSize': '20px',
                       'color': '#0000CD',})
        ]),

        html.Div([
            dcc.Graph(id='total_emp',
                      figure=fig1,
                      style={'width': '30vh',
                             'height': '30vh',
                            }),
        ],  className='two columns'),

        html.Div([
            dcc.Graph(id='present_emp',
                      figure=fig2,
                      style={'width': '30vh',
                             'height': '30vh',
                             }),
        ], className='two columns'),

        html.Div([
            dcc.Graph(id='total_dep',
                      figure=fig3,
                      style={'width': '30vh',
                             'height': '30vh',
                             }),
        ], className='two columns'),

        html.Div([
            dcc.Graph(id='mean_perf',
                      figure=fig4,
                      style={'width': '30vh',
                             'height': '30vh',
                             }),
        ], className='two columns'),

        html.Div([
            dcc.Graph(id='mean_emp',
                      figure=fig5,
                      style={'width': '30vh',
                             'height': '30vh',
                             }),
        ], className='two columns'),

    ], className='row'),

    html.Div([

        html.H1(children='',
                ),

        html.Div([
            dcc.Graph(id='emp_per_dep',
                      figure=fig6,
                      style={'width': '90vh',
                             'height': '70vh',
                             }),
        ],  className='five columns'),

        html.Div([
            dcc.Graph(id='emp_per_sex',
                      figure=fig7,
                      style={'width': '85vh',
                             'height': '70vh',
                             }),
        ],  className='six columns'),
    ],  className='row'),


    html.Div([

        html.H1(children='',
                ),

        html.Div([
            dcc.Graph(id='age_distribution',
                      style={'width': '90vh',
                             'height': '70vh',
                             }),
            dcc.Dropdown(id='dep-picker', options=dep_options,
                         value='Production')
        ], className='five columns'),

        html.Div([
            dcc.Graph(id='salary_distribution',
                      style={'width': '85vh',
                             'height': '70vh',
                             }),
            dcc.Dropdown(id='dep-picker1', options=dep_options,
                         value='Production')
        ], className='six columns'),

    ], className='row'),



])
])

# *******************************************************************************************************

# Generate the interactive Plots

# Plot to show Age Distribution wrt each Department


@app.callback(Output('age_distribution', 'figure'),
              [Input('dep-picker', 'value')])
def update_age_histogram(selected_dep):

    filtered_df = hr[hr['Department'] == selected_dep]
    hist_data = [go.Histogram(x=filtered_df['Age'],
                              marker=dict(color='yellow'))]
    layout = go.Layout(title=dict(
        text='Age Distirbution in Departments', x=0.5), font_color='yellow', paper_bgcolor='#000080')
    return {'data': hist_data, 'layout': layout}

# Plot to show Salary Distribution wrt each Department


@app.callback(Output('salary_distribution', 'figure'),
              [Input('dep-picker1', 'value')])
def update_salary_histogram(selected_dep):

    filtered_df = hr[hr['Department'] == selected_dep]
    hist_data = [go.Histogram(x=filtered_df['Salary'],
                              marker=dict(color='yellow'))]
    layout = go.Layout(title=dict(
        text='Salary Distirbution in Departments', x=0.5), font_color='yellow', paper_bgcolor='#000080')
    return {'data': hist_data, 'layout': layout}

# *******************************************************************************************************


# Run the Server
if __name__ == '__main__':
    app.run_server(debug=True)
