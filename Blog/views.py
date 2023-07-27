from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import User
# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect('/login')
    blogs = Post.objects.all()
    return render(request,'home.html',{'blogs':blogs})
def login(request):
    if(request.method=="POST"):
        email = request.POST.get('email')
        password = request.POST.get('password')
        valid_user = authenticate(request,username=email,password=password)
        print(email,password)
        second= None
        if valid_user is None:
            try:
                second =  User.objects.get(email=email)
            except:
                messages.error(request,"Invalid credentials")
                return redirect('/login')
           
            is_password = second.check_password(password)
            if is_password is False:
                messages.error(request,"Invalid credentials")
                return redirect('/login')
            else:
                valid_user = second
                print("line 30",valid_user)
                auth_login(request,valid_user)
                messages.success(request,"Login successfull")
                return redirect('/blog')
            
        else:
            messages.success(request,"Login successfull")
            print("line 32",valid_user)
            auth_login(request,valid_user)
            return redirect('/blog')
    if request.user.is_anonymous:
        return render(request,'login.html')
    else:
        return redirect('/blog')

def viewpost(request,id):
    if request.user.is_anonymous:
        return redirect('/login')
    post = Post.objects.filter(id=id).first()
    if post is None:
        messages.error(request,"No such blog found")
        return redirect('/blog')
    return render(request,'blog.html',{'Post':post})


def editpost(request,id):
    if request.user.is_anonymous:
        return redirect('/login')
    
    post = Post.objects.filter(id=id).first()
    if post is None:
            messages.error(request,"No such blog found")
            return redirect('/blog')
    elif request.method=="POST":
        post.title = request.POST.get('title')
        post.name = request.POST.get('name')
        post.desc = request.POST.get('desc')
        post.save()
        messages.success(request,"Your blog has been updated successfully")
        return redirect('/blog')
    
    # if request.user.pk != id:
    #     messages.error(request,"You are not authorized to edit this blog")
    #     return redirect('/blog')

    return render(request,'editblog.html',{'blog':post})

def addblog(request):
    if request.user.is_anonymous:
        return redirect('/login')
    if request.method=="POST":
        title = request.POST.get('title')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        print(title,name,desc)
        post = Post(title=title,name=name,desc=desc)
        post.save()
        messages.success(request,"Your blog has been added successfully")
        return redirect('/blog')
    return render(request,'addblog.html')
def logoutblog(request):
    if request.user.is_anonymous:
        return redirect('/login')
    logout(request)
    messages.success(request,"Logout successfull")
    return redirect('/login')

def signup(request):
    if request.method=="POST":
        username = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if username=="" or email=="" or password=="":
            messages.error(request,"Please fill all the fields")
            return render(request,'signup.html')
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return render(request,'signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return render(request,'signup.html')
        user = authenticate(request,username=username,password=password)
        second = authenticate(request,email=email,password=password)
        if user or second is not None:
            messages.error(request,"User already exists")
        else:
            user = User.objects.create_user(username,email,password)
            user.save()
            messages.success(request,"User created successfully")
            return redirect('/login')
    return render(request,'signup.html')