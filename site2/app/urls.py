from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage,name="login"),
    path('register/', views.register,name="register"),
    path('home/', views.home,name="home"),
    path('sua/', views.chinhsua,name="sua"),
    path('quenmatkhau/', views.quenmk,name="quenmk"),
    path('cuahang/', views.cuahang,name="cuahang"),
    path('thanhtoan/', views.thanhtoan,name="thanhtoan"),
    path('dangxuat/', views.dangxuat,name="dangxuat"),
    path('thucdon/', views.thucdon,name="thucdon"),
    path('khohang/', views.khohang,name="khohang"),
    path('nhanvien/', views.nhanvien,name="nhanvien"),
    path('doanhthu/', views.doanhthu,name="doanhthu"),
    path('donhang/', views.donhang,name="donhang"),
    path('chitietdonhang/<int:donhang_id>/', views.ctdonhang,name="ctdonhang"),
    path('suanguyenlieu/<int:kho_id>/', views.suakho,name="suakho"),
    path('suanhanvien/<int:nv_id>/', views.suanhanvien,name="suanhanvien"),
    path('suamonan/<int:monan_id>/', views.suamon,name="suamon"),
    path('sualoaimon/<int:loai_id>/', views.sualoai,name="sualoai"),
    path('thongtinnhaphang/', views.ttnhaphang,name="nhaphang"),
    path('thanhtoanmomo/', views.thanhtoanmomo,name="momo"),
]