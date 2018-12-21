from django.shortcuts import render,HttpResponse,redirect,reverse
from myadmin import models
import math
from django.views.decorators.csrf import csrf_exempt
from time import sleep
def test(request):
    return HttpResponse('Nihao')


# Create your views here.
#用户验证装饰器
def check_cookie(func):
    def return_res(*args,**kwargs):
        print(args)
        if not args[0].COOKIES.get('username'):
            return redirect('/myadmin/login')
        else:
            return func(*args,**kwargs)
    return return_res
#md5加密函数
def str_jiami(mystr):
    #导入hashlib模块
    import hashlib
    #实例化md5对象
    md5=hashlib.md5()
    #调用update方式加密mystr字符串，需要将mystr转化为utf-8
    md5.update(mystr.encode())
    #返回加密码后的内容
    return md5.hexdigest()
#后台首页
@check_cookie#装饰器检查用户是否登陆
def index(request):
    # if request.COOKIES.get('username'):
    return render(request,'myadmin/index.html')
    #return  redirect('/myadmin/login')
#---------------------------用户登陆start-------------
#登陆方法
def login(request):
        #如果用户已经登陆，直接跳转到后台首页
        if request.COOKIES.get('username'):
            return redirect('/myadmin/')
        return render(request,'myadmin/login.html')

def check_login(request):
    # 取得参数
    username = request.POST.get('username')
    password = request.POST.get('password')
    code = request.POST.get('code')
    # 验证验证码
    # 返回0-账号信息正确  返回1---账号信息错误 2-验证码错误
    if code.upper() != request.session.get('code').upper():
        return HttpResponse(2)
    password = str_jiami(password)
    res = models.admin.objects.filter(username=username, password=password).count()
    if res:
        response = HttpResponse(0)
        response.set_cookie('username', username, max_age=3600)
        return response
    else:
        return HttpResponse(1)
#退出操作
def login_out(request):
    response=redirect('/myadmin/login')
    #删除cookie
    response.delete_cookie('username')
    return response
#检查验证码
def check_code(request):
    code=request.GET.get('code')
    if code.upper() == request.session.get('code').upper():
        return HttpResponse(0)
    else:
        return HttpResponse(1)
def get_code(request):
    from . import check_code  # 将Monaco.ttf字体文件放到根目录下
    # 调用create_validate_code生成验证码,返回一个image对象，一个随机验证码
    img, code = check_code.create_validate_code()
    # 将生成的验证码存储到session里
    request.session['code'] = code
    # 使用img对象的save方法（参数1：保存图片地址）
    img_addr = 'static/11.png'
    img.save(img_addr)
    return HttpResponse(open(img_addr,'rb').read())
#---------------------------用户登陆end-------------

#----------------------------用户管理start------------
#管理员列表
@check_cookie
def admin_list(request):
    #查询管理员信息
    #取得当前页数
    cur_page=int(request.GET.get('p',1))#第一次展示列表页数据时没有，p参数。默认为1
    NUM=10#每页显示的个数
    COUNT=models.admin.objects.count()#总记录数
    page =math.ceil(COUNT/NUM)#页数
    #页数的样式
    page_html=''
    for i in range(1,page+1):
        #当
        if i == cur_page:
            page_html += '<a class="curpage" href="/myadmin/admin_list?p=%d">%d</a>'%(i,i)
        else:
            page_html += '<a href="/myadmin/admin_list?p=%d">%d</a>' % (i, i)
    res=models.admin.objects.all().order_by('-id')[(cur_page-1)*NUM:cur_page*NUM]
    return render(request,'myadmin/admin_list.html',{'res':res,'page_html':page_html})

#管理员添加
@check_cookie
def admin_add(request):
    if request.method=='GET':
        return render(request,'myadmin/admin_add.html')
    else:
        username=request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if password == repassword:
            count=models.admin.objects.filter(username=username).count()
            #对用户不能重复进行判断
            if not count:
                password=str_jiami(password)#md5加密密码
                models.admin.objects.create(username=username,password=password)
                #return redirect('myadmin/admin_list')
                return redirect(reverse('admin_list'))
            else:
                error = '用户名已存在'
                return render(request, 'myadmin/error.html', {'error': error})
        else:
            error='两次输入密码不一致'
            return render(request,'myadmin/error.html',{'error':error})

#用户修改：
@check_cookie
def admin_edit(request):
    if request.method == 'GET':
        #取得参数
        id=request.GET.get('id')
        #查询用户信息
        res=models.admin.objects.get(id=id)
        return render(request,'myadmin/admin_edit.html',{'res':res})
    else:
        #取得参数
        id = request.POST.get('id')
        password=request.POST.get('password')
        repassword = request.POST.get('repassword')
        #判断2次密码是否一致
        if password == repassword:
            #修改密码
            password=str_jiami(password)#密码加密
            models.admin.objects.filter(id=id).update(password=password)
            return redirect('/myadmin/admin_list')
        else:
            error = '两次输入密码不一致'
            return render(request, 'myadmin/error.html', {'error': error})
def admin_del(request):
    id=request.GET.get('id')
    models.admin.objects.filter(id=id).delete()
    return redirect('/myadmin/admin_list')

#检查用户是否存在
def check_user(request):
    username = request.GET.get('username')
    count= models.admin.objects.filter(username=username).count()
    return HttpResponse(count)
# ----------------------------用户管理end------------

#--------------------文章分类start
 #分类列表
@check_cookie
def article_cat_list(request):
    res =models.article_cat.objects.all()
    return render(request,'myadmin/article_cat_list.html',{'res':res})

@csrf_exempt
def article_cat_add(request):
    #取得参数
    cat_name =request.POST.get('cat_name')
    #插入到article_cat数据库中
    models.article_cat.objects.create(cat_name=cat_name)
    return redirect('/myadmin/article_cat_list')
#删除操作
@check_cookie
def article_cat_del(request):
    #取得参数
    id=request.GET.get('id')
    #数据库操作
    models.article_cat.objects.filter(id=id).delete()
    #页面重定向
    return redirect('/myadmin/article_cat_list')

@check_cookie
def article_cat_edit(request):
    id=request.GET.get('id')
    cat_name=request.GET.get('cat_name')
    models.article_cat.objects.filter(id=id).update(cat_name=cat_name)
    return HttpResponse('操作成功')
#----------------文章分类end

#-----------------------文章start-------
def article_list(request):
    # res =models.article.objects.all()
    # return render(request,'myadmin/article_list.html',{'res':res})
    cur_page=int(request.GET.get('p',1))#第一次展示列表页数据时没有，p参数。默认为1
    NUM=10#每页显示的个数
    COUNT=models.article.objects.count()#总记录数
    page =math.ceil(COUNT/NUM)#页数
    #页数的样式
    page_html=''
    for i in range(1,page+1):
        #当
        if i == cur_page:
            page_html += '<a class="curpage" href="/myadmin/article_list?p=%d">%d</a>'%(i,i)
        else:
            page_html += '<a href="/myadmin/article_list?p=%d">%d</a>' % (i, i)
    res=models.article.objects.all().order_by('-id')[(cur_page-1)*NUM:cur_page*NUM]
    return render(request,'myadmin/article_list.html',{'res':res,'page_html':page_html})
def article_add(request):
    if request.method == 'GET':
        cat_res =models.article_cat.objects.all()
        return render(request,'myadmin/article_add.html',{'cat_res':cat_res})
    else:
        data={}
        data['title']=request.POST.get('title')
        data['desc'] = request.POST.get('desc')
        data['cat_id'] = request.POST.get('cat_id')
        data['content']= request.POST.get('content')
        data['sort']= request.POST.get('sort')
        data['count']= request.POST.get('count')
        image=request.FILES.get('image')
        #判断是否上传图片
        if image:
            #取得原图片名
            img_name=image.name
            #取得图片后缀
            img_type=img_name.split('.')[-1]
            #图片新图片名
            import uuid
            new_img_name = str(uuid.uuid1())+'.'+img_type
            #存储路径
            image_addr='static/upload/'+new_img_name
            with open(image_addr,'wb') as f:
                f.write(image.read())
            #将图片地址赋值给添加的图片字段
            data['image']='/'+image_addr
        #print(image.read())
        models.article.objects.create(**data)
        return redirect('/myadmin/article_list')
#修改文章
def article_edit(request):
    if request.method =="GET":
        #取得id参数
        id=request.GET.get('id')
        res=models.article.objects.get(id=id)
        #取得所有的分类
        cat_res =models.article_cat.objects.all()
        return render(request,'myadmin/article_edit.html',{'res':res,'cat_res':cat_res})
    else:
        # 取得id参数
        id = request.POST.get('id')
        data = {}
        data['title'] = request.POST.get('title')
        data['desc'] = request.POST.get('desc')
        data['cat_id'] = request.POST.get('cat_id')
        data['content'] = request.POST.get('content')
        data['sort'] = request.POST.get('sort')
        data['count'] = request.POST.get('count')
        image = request.FILES.get('image')
        # 判断是否上传图片
        if image:
            # 取得原图片名
            img_name = image.name
            # 取得图片后缀
            img_type = img_name.split('.')[-1]
            # 图片新图片名
            import uuid
            new_img_name = str(uuid.uuid1()) + '.' + img_type
            # 存储路径
            image_addr = 'static/upload/' + new_img_name
            with open(image_addr, 'wb') as f:
                f.write(image.read())
            # 将图片地址赋值给添加的图片字段
            data['image'] = '/' + image_addr
        models.article.objects.filter(id=id).update(**data)
        return redirect('/myadmin/article_list')
            # print(image.read())
def article_del(request):
    id=request.GET.get('id')
    models.article.objects.filter(id=id).delete()
    return redirect('/myadmin/article_list')
#--------------文章end

#--------------网站配置start
def config(request):
 
    if request.method == 'GET':
        count =models.config.objects.all().count()
        if not count:
            #由于我config表中其他字段都可以为空，所以只给id赋值
            models.config.objects.create(id=2)
        res=models.config.objects.get(id=2)
        return render(request,'myadmin/config.html',{'res':res})
    else:
        data={}#保存修改的内容
        id=request.POST.get('id')
        data['title']=request.POST.get('title')
        data['keywords'] = request.POST.get('keywords')
        data['description'] = request.POST.get('description')
        data['about_us'] = request.POST.get('about_us')
        data['connect_us'] = request.POST.get('connect_us')
        logo = request.FILES.get('logo')
        # 判断是否上传图片
        if logo:
            # 取得原图片名
            img_name = logo.name
            # 取得图片后缀
            img_type = img_name.split('.')[-1]
            # 图片新图片名
            new_img_name = 'logo.' + img_type
            # 存储路径
            image_addr = 'static/' + new_img_name
            with open(image_addr, 'wb') as f:
                f.write(logo.read())
            # 将图片地址赋值给添加的图片字段
            data['logo'] = '/' + image_addr
        #修改操作
        models.config.objects.filter(id=id).update(**data)
  
        return redirect('/myadmin/config')


# def config(request):
#     if request.method == 'GET':
#         count = models.config.objects.all().count()
#         if not count:
#             #由于我config表中其他字段都可以为空，所以只给id赋值
#             models.config.objects.create(id=2)
#         res = models.config.objects.get(id=2)
#         return render(request, 'myadmin/config.html', {'res': res})
    
 
#--------------网站配置end
#--------------留言板查查————————


def message_board(request):
    res= models.message.objects.all()
    return render(request,'myadmin/message_board.html',{'res':res})


def message_board_del(request):
    id=request.GET.get('id')
    print(id)
    models.message.objects.filter(id=id).delete()
    return redirect('/myadmin/message_board')
