from django.shortcuts import render
from django.views import generic


def index(request):
    return render(request, 'index.html')


def tree(request):
    return render(request, 'tree.html')


def circletree(request):
    return render(request, 'circletree.html')
