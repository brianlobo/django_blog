from django.shortcuts import render

posts = [
    {
        'author': 'Brian',
        'title': 'Post 1',
        'content': 'First Post data',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Kiara',
        'title': 'Post 2',
        'content': 'First Post data',
        'date_posted': 'August 28, 2018'
    }
]

def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', { 'title': 'About'})
