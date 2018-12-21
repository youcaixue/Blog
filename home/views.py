from django.shortcuts import render,HttpResponse,redirect
from myadmin import models
import math
# Create your views here.
def index(request):
    res =models.article.objects.all()
    return render(request,'home/index.html',{'res':res})
def about(request):
    return render(request,'home/about.html')
def article(request):
    res =models.article.objects.all()
    return render(request,'home/article.html',{'res':res})
def article_detail(request):
    # res =models.article.objects.all()
    cur_page=int(request.GET.get('p',1))#第一次展示列表页数据时没有，p参数。默认为1
    NUM=1#每页显示的个数
    COUNT=models.article.objects.count()#总记录数
    page =math.ceil(COUNT/NUM)#页数
    #页数的样式
    page_html=''
    for i in range(1,page+1):
        #当
        if i == cur_page:
            page_html += '<a class="curpage" href="/article_detail.html?p=%d">%d</a>'%(i,i)
        else:
            page_html += '<a href="/article_detail.html?p=%d">%d</a>' % (i, i)
    res=models.article.objects.all().order_by('-id')[(cur_page-1)*NUM:cur_page*NUM]
    return render(request,'home/article_detail.html',{'res':res,'page_html':page_html})
    # return render(request,'home/article_detail.html',{'res':res})
def mood(request):
    res = models.article.objects.all()
    return render(request, 'home/mood.html', {'res': res})
def board(request):
    return render(request,'home/board.html')
def gbook(request):
    res=models.message.objects.all()
    return render(request,'home/board.html',{'res':res})
#留言添加
def board_add(request):
    data={}
    data['name']=request.POST.get('name')
    data['content']=request.POST.get('content')
    models.message.objects.create(**data)
    return redirect('/gbook')
def article_detail_board(request):
    res_board=models.message.objects.all()
    return render(request,'home/article_detail.html',{'res_board':res_board})