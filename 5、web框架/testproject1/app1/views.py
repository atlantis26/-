from django.shortcuts import render, HttpResponse, redirect
# Create your views here.


def index(request):
    return HttpResponse("index")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        u = request.post.get("username")
        p = request.post.get("password")
        if u == "alex" and p == "123":
            return redirect("/index/")
        else:
            return render(request, "login.html")
    else:
        return redirect("/index/")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    elif request.method == "POST":
        u = request.POST.get("username")
        p1 = request.POST.get("pwd1")
        p2 = request.POST.get("pwd2")
        p3 = request.POST.get("gender")
        p4 = request.POST.get("gen")
        file_obj = request.FILES.get("file1")
        print(u, p1, p2, p3, p4)
        print(file_obj.name)
        return redirect("/register/")
    else:
        return redirect("/register/")
