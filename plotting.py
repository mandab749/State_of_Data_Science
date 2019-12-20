from flask import render_template, request
from theapp import app
import matplotlib
import os
matplotlib.use('Agg')
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from flask import url_for, jsonify, render_template



#in_ss = request.args.get('subset_by', default = None, type = str)
#in_pp = request.args.get('proportions', default = None, type = str)
#in_ss = 'Age'
#in_pp = 'Gender'
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

top_countries = ('India', 'United States of America', 'Brazil', 'Japan', 'Russia',
                 'China', 'Germany', 'United Kingdom of Great Britain and Northern Ireland',
                 'Canada', 'Spain')



# Initialization code to be able to query the database
def query_generator_and_data_grabber(input_sub, input_prop):
    conn = psycopg2.connect("dbname=kaggle user=abucklin")
    cur = conn.cursor()
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
    subset = formatted_to_name[input_sub]
    proportion = formatted_to_name[input_prop]
    basic = "SELECT " + subset + ", " + proportion + ", " + "count(*) FROM less_mcq "
    conditions = ''
    top_countries = ('India', 'United States of America', 'Brazil', 'Japan', 'Russia',
                     'China', 'Germany', 'United Kingdom of Great Britain and Northern Ireland',
                     'Canada', 'Spain')
    if subset == 'Country' or proportion == 'Country':
        conditions = "WHERE Country in " + str(top_countries)
    group = "GROUP BY "+ subset + ", " + proportion
    order = "ORDER BY " + proportion + ", " + subset
    query = basic + conditions + group + ";"
    cur.execute(query)
    data = cur.fetchall()
    return data

def raw_data_to_histogram(data, header):
    df = pd.DataFrame(data, columns = header)
    pivot_df = df.pivot(index = header[0], columns = header[1], values = header[2]).fillna(value=0)
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#C0C0C0", "#800000", "#808000", "#008000", "#800080", "#008080", "#000080", "#F08080", "#FF8C00", "#FFD700", "#B8860B", "#DAA520", "#F0E68C", "#90EE90", "#6495ED", "#1E90FF", "#0000CD", "#4169E1", "#FF1493", "#9932CC"]
           #There is also a stacked = True possibility
    bar = pivot_df.plot.bar(stacked=True, color=colors, rot=1 ,  figsize=(10,7))
    #go.Bar(pivot_df)
    bar.plot()
    plt.show()
    strFile = '/var/www/DSSurvey/static/'+ formatted_to_name[header[0]] + '_'+formatted_to_name[header[1]] + '.png'
    if os.path.isfile(strFile):
        print("hell yeah boiiii")
        os.remove(strFile)
    plt.savefig(strFile)
    #data = pd.DataFrame(raw_data, columns = [in_ss , in_pp])

for key1 in formatted_to_name:
    for key2 in formatted_to_name:
        if key1 == key2 :
            continue
        else:
            header = [key1, key2 , "value"]
            data = query_generator_and_data_grabber(key1, key2)
            raw_data_to_histogram(data = data, header = header)



'''
@app.route('/')
def index():
    in_ss = request.args.get('subset_by', default = "Age", type = str)
    in_pp = request.args.get('proportions', default = "Gender", type = str)
    headers = [in_ss, in_pp, 'Values']
    raw_data = query_generator_and_data_grabber(in_ss, in_pp)
    raw_data_to_histogram(raw_data, headers)
    #plt.savefig('/var/www/DSSurvey/static/plot.png')
   # return render_template('index.html', plot=bar) #this has changed
    return render_template('index.html', name = 'new_plot', url ='./static/plot.png')

'''

'''
@app.route('/background_process_test')
def background_process_test():
    print("Hello")
    x = "nothing"
    return x
'''

'''
@app.route('/foo', methods=['GET', 'POST'])
def foo():
    in_ss = request.args.get('subset_by', default = "Age", type = str)
    in_pp = request.args.get('proportions', default = "Gender", type = str)
    headers = [in_ss, in_pp, 'Values']
    raw_data = query_generator_and_data_grabber(in_ss, in_pp)
    raw_data_to_histogram(raw_data, headers)
    plt.savefig('/var/www/DSSurvey/static/plot.png')
    #return render_template('index.html', plot=bar) #this has changed
    return render_template('index.html', name = 'new_plot', url ='/var/www/DSSurvey/static/plot.png')
    #return

'''

