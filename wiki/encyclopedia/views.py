from django.http.response import HttpResponse
from django.shortcuts import render, redirect

from . import util
import markdown2
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, subject):
    return render(request, "encyclopedia/entry.html", {
        "description": markdown2.markdown(util.get_entry(subject)),
        "title": subject,
    })

def error(request, errorType):
    # if request.method == "GET":
    #     return redirect("index")
    if errorType==1:
        notice = "entry does not exist!"
    if errorType==2:
        notice = "Entry already exists with this title!"
    return render(request, "encyclopedia/error.html", {
        "type": notice
    })

def randomPage(request):
    list = util.list_entries()
    rand_entry = random.sample(list, 1)
    # return redirect('entry', subject = rand_entry[0])
    return redirect('entry', rand_entry[0])

def search(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        list = util.list_entries()
        similar = []
        for item in list: 
            if subject.upper() == item.upper():
                return redirect('entry', item)
            if subject.upper() in item.upper():
                similar.append(item)
        else: 
            hasSimilar = False
            if len(similar) > 0:
                hasSimilar = True
                return render(request, "encyclopedia/search-error.html", {
                    "hasSimilar" : hasSimilar,
                    "similarList" : similar
                })
            return render(request, "encyclopedia/search-error.html", {
                    "hasSimilar" : hasSimilar,
                    "similarList" : similar
                })
    return redirect('index')

def newEntry(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        list = util.list_entries()
        for item in list:
            if title.upper() == item.upper():
                errorType = 2
                return redirect('error', errorType)
        util.save_entry(title, content)
        return redirect('index')
    return render(request, 'encyclopedia/new-entry.html')

def edit(request): 
    if request.method == "POST":
        return HttpResponse("edit")
    return redirect('index')

def editEntry(request, subject):
    if request.method== "POST": 
        return render(request, 'encyclopedia/edit-entry.html', {
            "title_data": subject,
            "content_data": util.get_entry(subject),
        })
    return HttpResponse(f"edit entry- {subject}")

def updateEntry(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
    return redirect('index')