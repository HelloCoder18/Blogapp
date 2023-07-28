from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib import messages
from .models import Post
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
# Create your views here.

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        blogs = Post.objects.all()
        return render(request, 'home.html', {'blogs': blogs, 'user': request.user.is_superuser})

class SignupView(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        print(email, password, name)
        try:
            user = User.objects.get(email=email)
            user_exists = User.objects.filter(username=name)
            if user_exists is not None:
                messages.error(request, "Username already exists")
            elif user is not None:
             messages.error(request, "Email already exists")

            return redirect('/signup')
        except User.DoesNotExist:
            user = User.objects.create_user(email, email, password)
            user.first_name = name
            user.save()
            messages.success(request, "Your account has been created successfully")
            return redirect('/login')


class LoginView(View):
    def get(self, request):
        if request.user.is_anonymous:
            return render(request, 'login.html')
        else:
            return redirect('/blog')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        valid_user = authenticate(request, username=email, password=password)
        print(email, password)
        second = None
        if valid_user is None:
            try:
                second = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "Invalid credentials")
                return redirect('/login')

            is_password = second.check_password(password)
            if not is_password:
                messages.error(request, "Invalid credentials")
                return redirect('/login')
            else:
                valid_user = second
                print("line 30", valid_user)
                auth_login(request, valid_user)
                messages.success(request, "Welcome to the blog "+valid_user.get_username())
                return redirect('/blog')

        else:
            messages.success(request,  "Welcome to the blog "+valid_user.get_username())
            print("line 32", valid_user.is_anonymous)
            auth_login(request, valid_user)
            return redirect('/blog')

class ViewPostView(LoginRequiredMixin, View):
     def get(self, request, id):
        post = Post.objects.filter(id=id).first()
        if post is None:
            messages.error(request, "No such blog found")
            return redirect('/blog')
        
        post.views += 1
        post.save()

        return render(request, 'blog.html', {'blog': post})


class EditPostView(LoginRequiredMixin,UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
    def get(self, request, id):
        post = Post.objects.filter(id=id).first()
        if post is None:
            messages.error(request, "No such blog found")
            return redirect('/blog')
        
        if request.user.username != post.author_id.username and not request.user.is_superuser:
            messages.error(request, "You are not authorized to edit this blog")
            return redirect('/blog')

        return render(request, 'editblog.html', {'blog': post, 'user': request.user.is_superuser})

    def post(self, request, id):
        post = Post.objects.filter(id=id).first()
        if post is None:
            messages.error(request, "No such blog found")
            return redirect('/blog')
        
        if request.user.username != post.author_id.username and not request.user.is_superuser:
            messages.error(request, "You are not authorized to edit this blog")
            return redirect('/blog')

        post.title = request.POST.get('title')
        post.name = request.POST.get('name')
        post.desc = request.POST.get('desc')
        post.save()

        messages.success(request, "Your blog has been updated successfully")
        return redirect('/blog')

class AddBlogView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        return render(request, 'addblog.html')

    def post(self, request):
        title = request.POST.get('title')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        print(title, name, desc)
        post = Post(title=title, name=name, desc=desc, author_id=request.user)
        post.save()
        messages.success(request, "Your blog has been added successfully")
        return redirect('/blog')

class LogoutBlogView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logout successful")
        return redirect('/login')
    
# def signup(request):
#     if request.method=="POST":
#         username = request.POST.get('name')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         if username=="" or email=="" or password=="":
#             messages.error(request,"Please fill all the fields")
#             return render(request,'signup.html')
#         if User.objects.filter(username=username).exists():
#             messages.error(request,"Username already exists")
#             return render(request,'signup.html')
#         if User.objects.filter(email=email).exists():
#             messages.error(request,"Email already exists")
#             return render(request,'signup.html')
#         user = authenticate(request,username=username,password=password)
#         second = authenticate(request,email=email,password=password)
#         if user or second is not None:
#             messages.error(request,"User already exists")
#         else:
#             user = User.objects.create_user(username,email,password)
#             user.save()
#             messages.success(request,"User created successfully")
#             return redirect('/login')
#     return render(request,'signup.html')