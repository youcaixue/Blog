"""ai4_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from home import views
from myadmin import views as admin_views
from myadmin.uploads import upload_image
urlpatterns = [
    #home应用路由
    url(r'^$',views.index,name='index'),
    url(r'^index.html$',views.index),
    url(r'^about.html$',views.about,name='about'),
    url(r'^mood.html$',views.mood,name='mood'),
    url(r'^board.html$',views.board,name='board'),
     url(r'^article.html$',views.article,name='article'),
    url(r'^article_detail.html$',views.article_detail,name='article_detail'),
    # url(r'^board_message$',views.board_message,name='board_message'),
    url(r'^myadmin/test$',admin_views.test),
    url(r'^gbook$', views.gbook, name='gbook'),
    url(r'^article_detail_board', views.article_detail_board, name='article_detail_board'),
    url(r'^board_add$', views.board_add, name='board_add'),


    #后台admin应用路由
    url(r'^myadmin/$',admin_views.index),
    url(r'^myadmin/login$',admin_views.login,name='login'),#登陆路由
    url(r'^myadmin/check_login$',admin_views.check_login,name='check_login'),#登陆ajax验证
    url(r'^myadmin/login_out$', admin_views.login_out,name='login_out'),
    url(r'^myadmin/check_code$', admin_views.check_code,name='check_code'),
    url(r'^myadmin/get_code$', admin_views.get_code, name='get_code'),


    url(r'^myadmin/admin_list$', admin_views.admin_list,name='admin_list'),
    url(r'^myadmin/admin_add$', admin_views.admin_add,name='admin_add'),
    url(r'^myadmin/admin_edit$', admin_views.admin_edit,name='admin_edit'),
    url(r'^myadmin/admin_del$', admin_views.admin_del,name='admin_del'),
    #文章分类
    url(r'^myadmin/article_cat_list$',admin_views.article_cat_list,name='article_cat_list'),
    url(r'^myadmin/article_cat_add$', admin_views.article_cat_add, name='article_cat_add'),
    url(r'^myadmin/article_cat_del$', admin_views.article_cat_del, name='article_cat_del'),
    url(r'^myadmin/article_cat_edit$', admin_views.article_cat_edit, name='article_cat_edit'),
    #文章
    url(r'^myadmin/article_list$',admin_views.article_list,name='article_list'),
    url(r'^myadmin/article_add$',admin_views.article_add,name='article_add'),
    url(r'^myadmin/article_edit$',admin_views.article_edit,name='article_edit'),
    url(r'^myadmin/check_user$', admin_views.check_user, name='check_user'),
    url(r'^myadmin/article_del$', admin_views.article_del,name='article_del'),
    #留言板
    url(r'^myadmin/message_board$', admin_views.message_board,name='message_board'),
    url(r'^myadmin/message_board_del$', admin_views.message_board_del, name='message_board_del'),
    #配置
    url(r'^myadmin/config$', admin_views.config, name='config'),
    #富文本编辑器图片上传路由
    url(r'^upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
]
