from django.shortcuts import render

def f():
    return 'function'

def home_view(request):
    cities = ["Amsterdam","Rotterdam","The Hague"]
    context = {'cities' : cities,}
    # import pudb;pu.db()
    return render(request, 'divers/home_page.html', context=context)

def dashboard_view(request):
    context = {}
    return render(request, 'divers/dashboard_page.html', context=context)


def about_view(request):
    context = {'test' : 'test', 'function':f}
    # import pudb;pu.db()
    return render(request, 'divers/about_page.html', context=context)

def about_us_view(request):
    context = {'test' : 'test', 'function':f}
    # import pudb;pu.db()
    return render(request, 'divers/about_us_page.html', context=context)

