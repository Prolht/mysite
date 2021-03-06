from django.shortcuts import render
from . models import Article,Comment,Poll,NewUser
from . forms import CommentForm,LoginForm,RegisterForm,SetInfoForm,SearchForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from urllib.parse import urljoin
import markdown2

# Create your views here.

def index(request): #request is a key param ,it include all the request from users
    latest_article_list = Article.objects.query_by_time()
    loginform = LoginForm()
    context = {'latest_article_list':latest_article_list,'loginform':loginform}
    return render(request,'index.html',context)
def article(request,article_id):
    '''
    	try:   # since visitor input a url with invalid id
    		article = Article.objects.get(pk=article_id)  # pk??? 
    	except Article.DoesNotExist:
    		raise Http404("Article does not exist")
    	'''  # shortcut:
    article = get_object_or_404(Article,id=article_id)
    content = markdown2.markdown(article.content,extras=["code-friendly",
            "fenced-code-blocks","header-ids","toc","metadata"])
    commentform = CommentForm()
    loginform =LoginForm()
    comments = article.comment_set.all

    return render(request,'article_page.html',{
        'articel':article,
        'loginform':loginform,
        'commentform':commentform,
        'content':content,
        'comment':comments
    })

@login_required
def comment(request,article_id):
    form = CommentForm(request.POST)
    url = urljoin('/myblog/',article_id)
    if form.is_valid():
        user = request.user
        article = Article.objects.get(id=article_id)
        new_comment = form.cleaned_data['comment']
        c = Comment(content=new_comment,article_id=article_id)
        c.user = user
        c.save()
        article.comment_num +=1
    return redirect(url)

@login_required
def get_keep(request,article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    articles = logged_user.article_set.all()
    if article not in article:
        article.user.add(logged_user)
        article.keep_num += 1
        article.save()
        return redirect(url)

@login_required
def get_poll_article(request,article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    polls = logged_user.poll_set.all()
    articles = []
    for poll in polls:
        articles.append(poll.article)

    if article in articles:
        url = urljoin('/myblog/',article_id)
        return redirect(url)
    else:
        article.poll_num += 1
        article.save()
        poll = Poll(user=logged_user,article=article)
        poll.save()
        data = {}
        return redirect('/myblog/')
def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username,password=password)
            if user is None:
                login(request,user)
                url = request.POST.get('source_url','/myblog')
                return redirect(url)
            else:
                return render(request,'login.html',{'form':form,'error':"password or username is not true!"})
        else:
            return render(request,'login.html',{'form':form})

@login_required
def log_out(request):
    url = request.POST.get('source_url','/myblog/')
    logout(request)
    return redirect(url)

def register(request):
    error1 = "this name is already exist"
    valid = "this name is valid"

    if request.method == 'GET':
        form = RegisterForm()
        return render(request,'register.html',{'form':form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if request.POST.get('raw_username','erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi': #if ajax
            try:
                user = NewUser.objects.get(username=request.POST.get('raw_username',''))
            except ObjectDoesNotExist:
                return render(request,'register.html',{'form':form,'msg':valid})
            else:
                return render(request,'register.html',{'form':form,'msg':error1})
        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    return render(request,'register.html',{'form':form,'msg':"two password is not equal"})
                else:
                    user = NewUser(username=username,email=email,password=password1)
                    user.save()
                    return redirect('/myblog/login')
            else:
                return render(request,'register.html',{'form':form})