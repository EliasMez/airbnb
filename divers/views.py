from django.shortcuts import render
from pandas import read_csv


# input_path = '/csv_output/netherlands/amsterdam'

def f():
    return 'function'

def home_view(request):
    cities = ["Amsterdam","Rotterdam","The Hague"]
    context = {'cities' : cities,}
    # import pudb;pu.db()
    return render(request, 'divers/home_page.html', context=context)

def dashboard_view(request):
    file = open("static/netherlands/amsterdam/df1.csv")
    df = read_csv(file,encoding='latin')
    df_html = df.to_html()
    context = {'df_html':df_html, 'df1':df, 'line0':df.iloc[0]}
    return render(request, 'divers/dashboard_page.html', context=context)


def about_view(request):
    context = {'test' : 'test', 'function':f}
    # import pudb;pu.db()
    return render(request, 'divers/about_page.html', context=context)

def about_us_view(request):
    context = {'test' : 'test', 'function':f}
    # import pudb;pu.db()
    return render(request, 'divers/about_us_page.html', context=context)

