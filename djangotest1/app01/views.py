from django.shortcuts import render
from django.http import HttpResponse

# 如果是urls是/page/1,那pg=1
def testview(request):
    return HttpResponse("我在测试中1")

# Create your views here.
def test_render(request):
    a = 1
    b = 2  
    # locals 可以把 a,b这些值都可以传回到前端页面，然后使用 {{a}}{{b}}来渲染出这些变量
    return render(request,'appindex.html',locals())