from django.shortcuts import render
from pandas import read_csv
import numpy as np
import os

cities=[{'name':x[0].split("/")[-1], 'path': x[0]} for x in os.walk('static/csv_output/') if x[1]==[]]

dfs = ["df"+str(i) for i in range(1,9)]

def f():
    return 'function'

def home_view(request):
    print(cities)
    context = {'cities' : cities}
    # import pudb;pu.db()
    return render(request, 'divers/home_page.html', context=context)


def dashboard_view(request):
    citypath = request.GET["citypath"]
    cityname = request.GET["cityname"]
    if citypath not in [city['path'] for city in cities] or cityname not in [city['name'] for city in cities]:
        citypath = cities[0]['path']
        cityname = cities[0]['name']
    df = request.GET["df"]
    if df not in dfs:
        df = 'df1'
    file = open(f"{citypath}/{df}.csv")
    df = read_csv(file,encoding='latin')
    # df_html = df.to_html(classes="table table-striped table-sm", index=False, justify='left')
    series = np.array([df[column] for column in df.columns])
    series = np.transpose(series)
    context = {'df':df, 'series':series, 'citypath':citypath, 'cityname':cityname} #, 'df_html' : df_html
    return render(request, 'divers/dashboard_page.html', context=context)


def about_view(request):
    context = {'test' : 'test', 'function':f}
    # import pudb;pu.db()
    return render(request, 'divers/about_page.html', context=context)

def about_us_view(request):
    context = {'test' : 'test', 'function':f}
    # import pudb;pu.db()
    return render(request, 'divers/about_us_page.html', context=context)

