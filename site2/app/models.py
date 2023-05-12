from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.db.models import Sum, F, ExpressionWrapper
from django.db.models import Sum

# Create your models here.
# Tài khoản
class Thongtin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sdt=models.CharField(max_length=20,null=True) 
    diachi=models.CharField(max_length=100,null=True) 
    tenquan=models.CharField(max_length=50,null=True)
    
class TTForm(forms.ModelForm):
    sdt=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 
    diachi=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) 
    tenquan=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model =Thongtin
        fields = ('sdt', 'diachi', 'tenquan')
class loginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Tài khoản'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Mật khẩu'}))
class MyUserChangeForm(UserChangeForm):
    first_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Tên'}))
    last_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Họ'}))
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Email'}))
    class Meta:
        model =User
        fields = ('email', 'first_name', 'last_name')
        labels = {
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
class customuser(UserCreationForm):
    first_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Tên'}))
    last_name=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Họ'}))
    username=forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Tài khoản'}))
    password1 = forms.CharField(max_length=128,widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Mật khẩu'}))
    password2 = forms.CharField(max_length=128,widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Nhập lại mật khẩu'}))
    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Email'}))
    class Meta:
        model=User
        fields=['username','last_name','first_name','email', 'password1', 'password2']

class Nhanvien(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    hoten=models.CharField(max_length=50,null=True)
    namsinh=models.CharField(max_length=50,null=True)
    diachi=models.CharField(max_length=50,null=True) 
    giocong=models.FloatField(null=True) 
    sdt=models.CharField(max_length=50,null=True)
    mucluong=models.FloatField(null=True)
    luong=models.FloatField(null=True)
    danglam=models.BooleanField(default=False)
class nhanvienForm(forms.ModelForm):
    hoten=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Tên nhân viên'}))
    namsinh=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Năm sinh'}))
    diachi=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Địa chỉ'})) 
    sdt=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Số điện thoại'}))
    mucluong=forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Mức lương'}))
    class Meta:
        model=Nhanvien
        fields=['hoten','namsinh','diachi','sdt','mucluong']
#Cửa hàng
class Loaimon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    tenloai=models.CharField(max_length=50,null=True)  
class LoaiForm(forms.ModelForm):
    tenloai=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Tên loại'}))
    class Meta:
        model=Loaimon
        fields=['tenloai']

class Khohang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    tennvl=models.CharField(max_length=50,null=True) 
    mota=models.CharField(max_length=50,null=True)  
    dvt=models.CharField(max_length=50,null=True)
    soluong=models.IntegerField(null=True)
    giatien=models.FloatField()
    def calculate_sum():
        total_sum = Khohang.giatien*Khohang.soluong
        return total_sum
class hangForm(forms.ModelForm):
    tennvl=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'id':'tenthem','class': 'form-control','placeholder':'Tên nguyên vật liệu'})) 
    mota=forms.CharField(max_length=50,widget=forms.Textarea(attrs={'id':'motathem','class': 'form-control','placeholder':'Mô tả'}))  
    dvt=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'id':'dvtthem','class': 'form-control','placeholder':'Đơn vị tính'}))
    soluong=forms.IntegerField(widget=forms.TextInput(attrs={'id':'soluongthem','class': 'form-control','placeholder':'Số lượng'}))
    giatien=forms.FloatField(widget=forms.TextInput(attrs={'id':'giatienthem','class': 'form-control','placeholder':'Giá tiền'}))
    class Meta:
        model=Khohang
        fields=['tennvl','mota','dvt','soluong','giatien']
class hangsuaForm(forms.ModelForm):
    tennvl=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Tên nguyên vật liệu'})) 
    mota=forms.CharField(max_length=50,widget=forms.Textarea(attrs={'class': 'form-control','placeholder':'Mô tả'}))  
    dvt=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Đơn vị tính'}))
    soluong=forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Số lượng'}))
    giatien=forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Giá tiền'}))
    class Meta:
        model=Khohang
        fields=['tennvl','mota','dvt','soluong','giatien']
class Thucdon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    anh=models.ImageField(upload_to='',null=True) 
    tenmon=models.CharField(max_length=50,null=True)
    loaimon=models.ForeignKey(Loaimon,on_delete=models.CASCADE,null=True)  
    giatien=models.FloatField(null=True) 
    
class MonForm(forms.ModelForm):
    tenmon=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Tên Món'}))  
    anh=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    giatien=forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Giá tiền'})) 
    class Meta:
        model=Thucdon
        fields=['tenmon','anh','giatien']
        
class Goimon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    mon=models.ForeignKey(Thucdon,on_delete=models.CASCADE,null=True)
    soluong=models.IntegerField(null=True)
    @property
    def gia(self):
        return self.mon.giatien*self.soluong
    @staticmethod
    def thanhtien():
        total_price = Goimon.objects.aggregate(total=Sum('soluong'))['total']
        return total_price
class Donhang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    loai=models.CharField(max_length=50,null=True)
    thoigiantao=models.DateTimeField(auto_now_add=True)
    thanhtien=models.FloatField(null=True)
class CtDonhang(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    donhang=models.ForeignKey(Donhang, on_delete=models.CASCADE,null=True)
    mon=models.ForeignKey(Thucdon,on_delete=models.CASCADE,null=True)
    soluong=models.IntegerField(null=True)
    @property
    def gia(self):
        return self.mon.giatien*self.soluong
class Calamviec(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    nhanvien=models.ForeignKey(Nhanvien, on_delete=models.CASCADE,null=True)
    vaoca=models.DateTimeField()
class ThongtinKho(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    nvl= models.ForeignKey(Khohang, on_delete=models.CASCADE,null=True)
    soluongnhap=models.IntegerField(null=True)
    ngaynhap=models.DateTimeField()
    kieunhap=models.CharField(max_length=20,null=True)