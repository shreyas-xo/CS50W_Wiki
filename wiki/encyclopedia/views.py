from django.shortcuts import redirect, render
from markdown import markdown
from random import randint
from requests import request
from responses import POST
from . import util
import encyclopedia


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        content= "#Error 404: Page not found"
        title='Error 404' 
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {'content': content,'title':title})

def search(request):
    q=request.GET.get('q')
    if q in util.list_entries():
        return redirect("entry",title=q)
    list=util.list_entries()
    list=[entry for entry in list if q in entry]
    return render(request,"encyclopedia/search.html", {"entries":list,"q":q})

def random(request):
    list=util.list_entries()
    return redirect("entry",list[randint(0,len(list)-1)])

def new(request):
    if request.method == "POST":
        title=request.POST.get("title")
        content=request.POST.get("content")
        if title == "" or content == "":
            return render(request, "encyclopedia/new.html", {"message": "Invalid input. Fields cannot be left empty!"})
        if title in util.list_entries():
            return render(request,"encyclopedia/new.html",{"message":"Error: A page with the same title already exists!", "title":title, "content":content})
        util.save_entry(title,content)
        return redirect("entry",title=title)
    return render(request,"encyclopedia/new.html")

def edit(request,title):
    content = util.get_entry(title.strip())
    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":    
            return render(request, "encyclopedia/edit.html", {"message": "Invalid input. Fields cannot be left empty!"})
        util.save_entry(title,content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})