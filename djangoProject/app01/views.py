from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html')

def user_list(request):
    name = '234455'
    role = ['11','22','333']
    return render(request, 'User_list.html',
                  {"n1":name,"n2":role})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        print(request.POST)
        return HttpResponse("登录成功")

