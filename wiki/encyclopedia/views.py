from django.shortcuts import render
from markdown import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        content= "#Error: Page not found"
        title='Error' 
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {'content': content,'title':title})
