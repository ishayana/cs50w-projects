from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.storage import default_storage
from . import util
from .forms import CreateForm, EditForm
from markdown2 import Markdown
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, article):
    content = util.get_entry(article)
    title = 'Not found!'
    if content is not None:
        title = article
        markdowner = Markdown()
        content = markdowner.convert(content)

    return render(request, "encyclopedia/article.html", {'content' : content, 'title' : title})

def search(request):
    if request.method == 'GET':
        query = request.GET['q']
        content = util.get_entry(query)
        articles = util.list_entries()
        matched_list = []
        if content is not None:
            markdoner = Markdown()
            content = markdoner.convert(content)
            title = query
        else:
            for article in articles:
                article_lower = article.lower()
                if query in article_lower:
                    matched_list.append(article)
            title = 'Not found!'
               
    return render(request, "encyclopedia/article.html", {'content' : content,'title': title, 'matched_list':matched_list})

def create(request):
    form = CreateForm()
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd['title']
            description = cd['description']
            util.save_entry(title=title, content=description)
            messages.success(request, f'Article "{title}" was successfully created!', 'success')
            return redirect('encyclopedia:article', article=title)

    return render(request, "encyclopedia/create.html", {'form': form})
        

def edit(request, article):
    content = util.get_entry(article)
    initial_data = {
        'title' : article,
        'description' : content
    }
    form = EditForm(initial=initial_data)
    if request.method == 'POST':
        form = EditForm(request.POST, initial=initial_data)
        if form.is_valid():
            cd = form.cleaned_data
            title = cd['title']
            description = cd['description']
            util.save_entry(title=title ,content=description)
            messages.success(request, f'Article "{title}" was successfully updated!')
            return redirect('encyclopedia:article', article=title)
    return render(request, 'encyclopedia/edit.html', {'form':form})

def randompage(request):
    article_counter = len(util.list_entries())
    random_int = random.randint(0, article_counter-1)
    rand_article = util.list_entries()[random_int]
    return redirect('encyclopedia:article', article=rand_article)
