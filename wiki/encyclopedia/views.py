from django.shortcuts import render
from markdown2 import Markdown
from . import util
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)
    
def entry(request, title):
    html_entry = convert_md_to_html(title)
    if html_entry == None:
        return render(request, "encyclopedia/error.html", {
            "message": "Could not find the page you are looking for."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_entry
        })
    
def search(request):
    if request.method == "POST":
        search_query = request.POST["q"]
        html_content = convert_md_to_html(search_query)
        if html_content is not None:
                return render(request, "encyclopedia/entry.html", {            
                "title": search_query,
                "content": html_content,})
        else:
            entries = util.list_entries()
            recommendation = []
            for entry in entries:
                if search_query.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/results.html", {
                "recommendation": recommendation
            })

def newpage(request):
    if request.method =="GET":
        return render(request, "encyclopedia/newpage.html")
    else:
        title = request.POST["titlepage"]
        content = request.POST["content"]
        title_isvalid = util.get_entry(title)
        if title_isvalid is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Page already Exists"})
            
        else:
            util.save_entry(title, content)
            html_content= convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content,
            })

def edit(request):
    if request.method =='POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",     {
            "content": content,
            "title": title
        })
    
def save_edit(request):
    if request.method == 'POST':
        edited_title = request.POST['edit_title']
        edited_content = request.POST['edit_content']
        util.save_entry(edited_title, edited_content)
        html_content= convert_md_to_html(edited_title)
        return render(request, "encyclopedia/entry.html", {
            "title": edited_title,
            "content": html_content,
        })
    
def random(request):
    random_page = choice(util.list_entries())
    html_content= convert_md_to_html(random_page)
    return render(request, f"encyclopedia/entry.html", {
        'title': random_page,
        'content': html_content
    })
