from flask import render_template, request
from theapp import app
​
import matplotlib
matplotlib.use('Agg')
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
​
"""
in_ss = request.args.get('subset_by', default = None, type = str)
in_pp = request.args.get('proportions', default = None, type = str)
​
#in_ss = 'Age'
#in_pp = 'Gender'
​
name_to_formatted = {'Age': 'Age',
                     'Gender': 'Gender',
                     'Country': 'Country',
                     'yearly_compensation': 'Yearly Compensation',
                     'experience_coding' : 'Number of Years Coding',
                     'recommended_language': 'Beginner Language Recommendation'}
formatted_to_name = {'Age' : 'Age',
                     'Gender' : 'Gender',
                     'Country' : 'Country',
                     'Yearly Compensation' : 'yearly_compensation',
                     'Number of Years Coding' : 'experience_coding',
                     'Beginner Language Recommendation' : 'recommended_language'}
​
sql_sub = formatted_to_name[in_ss]
sql_prop = formatted_to_name[in_pp]
​
top_countries = ('India', 'United States of America', 'Brazil', 'Japan', 'Russia',
                 'China', 'Germany', 'United Kingdom of Great Britain and Northern Ireland',
                 'Canada', 'Spain')

"""

# Initialization code to be able to query the database​
def query_generator_and_data_grabber(input_sub, input_prop):
    conn = psycopg2.connect("dbname=kaggle user=abucklin")
    cur = conn.cursor()
    ​
    name_to_formatted = {'Age': 'Age',
                         'Gender': 'Gender',
                         'Country': 'Country',
                         'yearly_compensation': 'Yearly Compensation',
                         'experience_coding' : 'Number of Years Coding',
                         'recommended_language': 'Beginner Language Recommendation'}
    formatted_to_name = {'Age' : 'Age',
                         'Gender' : 'Gender',
                         'Country' : 'Country',
                         'Yearly Compensation' : 'yearly_compensation',
                         'Number of Years Coding' : 'experience_coding',
                         'Beginner Language Recommendation' : 'recommended_language'}
    ​
    subset = formatted_to_name[in_ss]
    proportion = formatted_to_name[in_pp]
    basic = "SELECT " + subset + ", " + proportion + ", " + "count(*) FROM less_mcq "
    conditions = ''
    top_countries = ('India', 'United States of America', 'Brazil', 'Japan', 'Russia',
                     'China', 'Germany', 'United Kingdom of Great Britain and Northern Ireland',
                     'Canada', 'Spain')
    if subset == 'Country' or proportion == 'Country':
        conditions = "WHERE Country in " + top_countries
    group = "GROUP BY "+ subset + ", " + proportion
    order = "ORDER BY " + proportion + ", " + subset
    query = basic + conditions + group + ";"
    cur.execute(query)
    data = cur.fetchall()
    return data
​
def raw_data_to_histogram(data, header):
    df = pd.DataFrame(raw_data, columns = header)
    pivot_df = df.pivot(index = header[0], columns = header[1], values = header[2])
    colors = ["#FF0000", '#0C0EF2', '#1BA107', '#E52FDD',
          '#8D2FE5' , '#900C3F', "#00CBFF", '#7E9598',
           "#FF9E00", '#1BA107' ,'#FFAD00', '#1ECE38', '#FFF300']​
           #There is also a stacked = True possibility
    bar = pivot_df.plot.bar(stacked=True, color=colors, rot=1 ,  figsize=(10,7))
    #go.Bar(pivot_df)
    bar.plot()
    plt.show()
    plt.savefig('/var/www/DSSurvey/static/plot.png')
    #data = pd.DataFrame(raw_data, columns = [in_ss , in_pp])
​
@app.route('/')
def index():
    in_ss = request.args.get('subset_by', default = None, type = str)
    in_pp = request.args.get('proportions', default = None, type = str)
    headers = [in_ss, in_pp, 'Values']
    raw_data = query_generator_and_data_grabber(in_ss, in_pp)
    raw_data_to_histogram(raw_data, headers)
    #plt.savefig('/var/www/DSSurvey/static/plot.png')
   # return render_template('index.html', plot=bar) #this has changed
    return render_template('index.html', name = 'new_plot', url ='./static/plot.png')
