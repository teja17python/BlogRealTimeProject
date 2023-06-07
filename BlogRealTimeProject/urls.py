"""BlogRealTimeProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from BlogApp import views
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('post/',views.Postview),
    path('postlogin/',views.post_view),
    path('signup/', views.signup_view),
    path('thankyou/',views.thankyou_view),
    path('logout/',views.logoutview),
    path('tag/',views.post_list_view),
    path('homepage/',views.homepageview),
    path('<pk>/delete/',views.commentdeleteview.as_view(),name='delete'),
    path('<pk>/delete1/',views.postdeleteview.as_view(),name='delete'),
    path('succ/',views.succview,name='succ'),
    path('postsucc',views.postsuccview,name='postsucc'),
    path('<year>/<month>/<day>/<post>', views.post_detail_view,name='post_detail'),
    path('<id>/share/', views.mail_send_view),
    path('<tag_slug>/',views.post_list_view,name='post_list_by_tag_name'),

    re_path('^$', views.homepageview),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

