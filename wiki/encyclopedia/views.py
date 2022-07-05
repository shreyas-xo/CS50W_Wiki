from django.shortcuts import redirect, render
from markdown import markdown
from random import randint
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
