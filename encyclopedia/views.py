from django.forms import widgets
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . import util
import random
import markdown2
from django import forms
from django.urls import reverse


class NewArticleForm(forms.Form):
    article = forms.CharField(label='Article Name',
                              min_length=3, max_length=255)
    content = forms.CharField(widget=forms.Textarea, min_length=10)


def index(request):
    # search
    if len(request.GET) > 0 and 'q' in request.GET:
        articles = util.list_entries()
        article_name = request.GET['q']

        # search localized page
        if article_name in articles:
            article_content = util.get_entry(article_name)
            return render(request, 'encyclopedia/articles/article.html', {
                'article_content': article_content,
                'article_name': article_name
            })
        else:
            # match pages
            articles_matches_words = []
            for art in articles:
                if(article_name.upper() in art.upper()):
                    articles_matches_words.append(art)

            print(articles_matches_words)
            if len(articles_matches_words) > 0:
                return render(request, "encyclopedia/search.html", {
                    "articles": articles_matches_words,
                })
            else:
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()
                })

    else:
        # index
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def article(request, article_name):
    articles_list = util.list_entries()
    if article_name in articles_list:
        article_content = util.get_entry(article_name)
        return render(request, 'encyclopedia/articles/article.html', {
            'article_content': article_content,
            'article_name': article_name
        })
    else:
        return render(request, 'encyclopedia/error.html', {
            'error_message': f'Article {article_name} does not exists!',
            'error_code': 404
        })


def new_article(request):
    # POST
    if request.method == 'POST':
        form = NewArticleForm(request.POST)

        if form.is_valid():
            # article already exists
            if article_already_exists(form.cleaned_data['article']) == True:
                return HttpResponse('Error, Article already exists!')
            article_name = form.cleaned_data['article']

            article_content = markdown2.markdown(form.cleaned_data['content'])
            util.save_entry(article_name, article_content)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse('Error')

    # GET
    else:
        return render(request, 'encyclopedia/new_article.html', {
            'form': NewArticleForm()
        })


def random_article(request):
    articles = util.list_entries()
    random_index = random.randint(0, len(articles) - 1)
    article_content = util.get_entry(articles[random_index])
    article_name = articles[random_index]
    return render(request, 'encyclopedia/articles/article.html', {
        'article_content': article_content,
        'article_name': article_name
    })


def edit_article(request, article_name):
    if request.method == 'GET':
        articles_list = util.list_entries()
        if article_name in articles_list:
            article_content = util.get_entry(article_name)
            return render(request, 'encyclopedia/articles/edit.html', {
                'form': NewArticleForm(initial={'article': article_name, 'content': article_content})
            })
        else:
            return render(request, 'encyclopedia/error.html', {
                'error_message': f'Article {article_name} does not exists!',
                'error_code': 404
            })
    elif request.method == 'POST':
        form = NewArticleForm(request.POST)

        if form.is_valid():
            # article already exists
            article_name = form.cleaned_data['article']
            article_content = markdown2.markdown(form.cleaned_data['content'])
            util.save_entry(article_name, article_content)
            return HttpResponseRedirect(reverse('article', kwargs={'article_name': article_name}))
        else:
            return HttpResponse('Error')


def article_already_exists(article_name):
    if article_name in util.list_entries():
        return True
    else:
        return False
