
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpResponseServerError,JsonResponse
from .models import *
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.crypto import get_random_string
from datetime import datetime
from django.utils import timezone
from django.db.models import Count 
import qrcode
# Create your views here.
#Đăng nhập
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = loginForm(request.POST)
            error_message = ""
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    error_message = "Tài khoản hoặc mật khẩu không đúng"
                    context={'rf': form,'er':error_message}
                    return render(request,'app/dn.html',context)
            else:
                context={'rf': form,'er':error_message}
                return render(request,'app/dn.html',context)
        else:
            form = loginForm()
        context={'rf': form}
        return render(request,'app/dn.html',context)
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            form=customuser(request.POST)
            error_message = ""
            if form.is_valid():        
                user = form.save()
                user = authenticate(request, username=username, password=password1)
                if user is not None:
                    login(request, user)
                    return redirect('home')
            elif User.objects.filter(username=username).exists():
                # Thông báo lỗi cho người dùng
                error_message = "Tài khoản đã tồn tại"
                context = {'rf': form,'er': error_message}
                return render(request, 'app/dk.html', context)
            elif password1!=password2:
                # Thông báo lỗi cho người dùng
                error_message = "Mật khẩu nhập lại không trùng khớp"
                context = {'rf': form,'er': error_message}
                return render(request, 'app/dk.html', context)
        else:
            form=customuser()
            error_message =None
        context={'rf':form,'er':error_message}
        return render(request,'app/dk.html',context)
def dangxuat(request):
    logout(request)
    return JsonResponse({'status': 'ok'})
def quenmk(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            new_password = get_random_string(length=8)
            user.set_password(new_password)
            user.save()
            send_mail(
                'Reset Password',
                f'Your new password is {new_password}',
                'your_email_address',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Please check your email for new password')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist with this email')
    return render(request, 'app/quenmk.html')
#Trang chủ
def home(request):
    if request.user.is_authenticated:
        thongtin = Thongtin.objects.get_or_create(user=request.user)
        thongtin = get_object_or_404(Thongtin,user=request.user)
        if thongtin:
            sdt=thongtin.sdt
            diachi=thongtin.diachi
            tenquan=thongtin.tenquan
            email = request.user.email
            fullname=request.user.get_full_name()
            context={'email':email,'ten':fullname,'sdt':sdt,'diachi':diachi,'tenquan':tenquan}
            return render(request,'app/home.html',context)
        else:
            context={}
            return render(request,'app/home.html',context)
    else:
        return redirect('login')
def chinhsua(request):
    if request.user.is_authenticated:
        user = request.user
        mymodel = get_object_or_404(Thongtin, user=user)
        if request.method == 'POST':
            ttform=TTForm(request.POST or None,instance=mymodel)
            form = MyUserChangeForm(request.POST, instance=user)
            if form.is_valid():
                ttform.save()
                form.save()
                return redirect('home')
        else:
            form = MyUserChangeForm(instance=user)
            ttform=TTForm(instance=mymodel)
        context={'rf': form,'tf':ttform}
        return render(request,'app/suathongtin.html',context)
    else:
        return redirect('login')
#Xử lý Order
def cuahang(request):
    if request.user.is_authenticated:
        user=request.user
        
        if request.method == 'POST':
            if 'goimonid' in request.POST:
                goimon_id=request.POST['goimonid']
                
                if goimon_id:
            
                    if Goimon.objects.filter(user=user,mon_id=goimon_id).exists():
                        kt=Goimon.objects.get(user=user,mon_id=goimon_id)
                        kt.soluong+=1
                        kt.save()
                    else:
                
                        goimon=Goimon(
                        user=user,
                        mon_id=goimon_id,
                        soluong=1
                        )
                        goimon.save()
                    return redirect('cuahang')
                else:
                    return redirect('cuahang')
            elif 'checkin' in request.POST:
                id=request.POST['checkin']
                nhanvien=Nhanvien.objects.get(user=user,pk=id)
                nhanvien.danglam=True
                
                vaocalam=Calamviec(
                    user=user,
                    vaoca=datetime.now(),
                    nhanvien=nhanvien,
                )
                nhanvien.save()
                vaocalam.save()
                return redirect('cuahang')
            elif 'checkout' in request.POST:
                id=request.POST['checkout']
                nhanvien=Nhanvien.objects.get(user=user,pk=id)
                nhanvien.danglam=False
                cacu=Calamviec.objects.get(user=user,nhanvien_id=id)
                ketca=datetime.now()
                ketca=ketca.replace(tzinfo=timezone.utc)
                gio=float(((ketca-cacu.vaoca).total_seconds())/3600)
                print(gio)
                nhanvien.giocong+=gio
                nhanvien.save()
                cacu.delete()
                return redirect('cuahang')

        goimons=Goimon.objects.filter(user=user)
        nhanvienins=Nhanvien.objects.filter(user=user,danglam=False)
        nhanvienouts=Nhanvien.objects.filter(user=user,danglam=True)
        sum=0
        for goimon in goimons:
            sum+=goimon.gia
        loaimons=Loaimon.objects.filter(user=user)
        thucdons=Thucdon.objects.filter(user=user)
        context={'thucdons':thucdons,'goimons':goimons,'loaimons':loaimons,'nhanvienins':nhanvienins,'nhanvienouts':nhanvienouts,'sum':sum}
        return render(request,'app/cuahang.html',context)
    else:
        return redirect('login')
#Xử lý món ăn
def thucdon(request):
    #thiết lập mặc định
    sualoai=LoaiForm()
    er=""
    form = LoaiForm()
    formmon=MonForm()
    #kiểm tra đăng nhập
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            #Thêm loại món ăn
            if 'themloai' in request.POST:
                form = LoaiForm(request.POST)
                if form.is_valid():
                    loai = Loaimon(
                        user=user,
                        tenloai=form.cleaned_data['tenloai'],
                    )
                    if Loaimon.objects.filter(user=request.user,tenloai=form.cleaned_data['tenloai']).exists():
                        er="Món đã tồn tại"
                    else:
                        loai.save()
                        return redirect('thucdon')
            #Thêm món ăn
            elif 'themmon' in request.POST:
                ktloai=Loaimon.objects.filter(user=request.user)
                #Kiểm tra đã có loại nào hay chưa, không trả về thông báo er
                if ktloai:
                    formmon=MonForm(request.POST,request.FILES)
                    loai=request.POST.get("loai-select")
                    if formmon.is_valid():
                        mon = Thucdon(
                            user=user,
                            anh=formmon.cleaned_data['anh'],
                            tenmon=formmon.cleaned_data['tenmon'],
                            loaimon=Loaimon.objects.get(id=loai),
                            giatien=formmon.cleaned_data['giatien']
                        )
                        #Kiểm tra món đã có hay chưa trước khi thêm
                        if Thucdon.objects.filter(user=request.user,tenmon=formmon.cleaned_data['tenmon']).exists():
                            er="Món đã tồn tại"
                        else:
                            mon.save()
                            return redirect('thucdon')
                    else:
                        return HttpResponseServerError("Lỗi")
                else:
                    er="Nên thêm loại trước"
            #Sửa thông tin của loại món       
            elif 'sualoai' in request.POST:
                objloai= Loaimon.objects.get(user=request.user,id=request.POST['sua-loai'])
                sualoai=LoaiForm(request.POST or None,instance=objloai)
                if form.is_valid():
                    sualoai.save()
                    return redirect('thucdon')
                else:
                    return redirect('cuahang')
            elif 'xoaloai' in request.POST:
                id=request.POST['xoa-loai']
                obj = Loaimon.objects.get(user=user,pk=id)
                obj.delete()
                return redirect('thucdon')
            elif 'xoamon' in request.POST:
                id=request.POST['xoa-mon']
                print(id)
                obj = Thucdon.objects.get(user=user,pk=id)
                obj.delete()
                return redirect('thucdon')
            else:
                return redirect('cuahang')
        else:
            form = LoaiForm()
            formmon=MonForm()
            
            
          
        loaimons = Loaimon.objects.filter(user=request.user)
        thucdons = Thucdon.objects.filter(user=request.user)
        return render(request, 'app/thucdon.html', {'form': form,'formmon':formmon,'sualoai':sualoai,'loaimons':loaimons,'monans':thucdons,'er':er})
    else:
        return redirect('login')
def suamon(request,monan_id):
    if request.user.is_authenticated:
        user = request.user
        monan = get_object_or_404(Thucdon, user=user,pk=monan_id)
        loaimons=""
        if request.method == 'POST':
            formnvl=MonForm(request.POST or None,instance=monan)
            if formnvl.is_valid():
                formnvl.save()
                return redirect('thucdon')
        else:
            formnvl = MonForm(instance=monan)
            loaimons = Loaimon.objects.filter(user=request.user)

        return render(request,'app/suamonan.html',{'forms':formnvl,'loaimons':loaimons})
    else:
        return redirect('login')
def sualoai(request,loai_id):
    if request.user.is_authenticated:
        user = request.user
        loai = get_object_or_404(Loaimon, user=user,pk=loai_id)
        loaimons=""
        if request.method == 'POST':
            formnvl=LoaiForm(request.POST or None,instance=loai)
            if formnvl.is_valid():
                formnvl.save()
                return redirect('thucdon')
        else:
            formnvl = LoaiForm(instance=loai)

        return render(request,'app/sualoai.html',{'forms':formnvl})
    else:
        return redirect('login')
#Xử lý thanh toán
def thanhtoan(request):
    if request.user.is_authenticated:
        user=request.user
        if Goimon.objects.filter(user=user).exists():
            goimons=Goimon.objects.filter(user=user)
            sum=0
            for goimon in goimons:
                sum+=goimon.gia
            if request.method == 'POST':
                trangthai=request.POST['loai']
                goimon=Goimon.objects.filter(user=user)
                donhang=Donhang(
                    user=user,
                    loai=trangthai,
                    thanhtien=sum
                )
                donhang.save()
                for cart in goimon:
                    thanhtoan=CtDonhang(
                        user=user,
                        donhang=donhang,
                        mon=cart.mon,
                        soluong=cart.soluong
                    )
                    thanhtoan.save()
                goimon.delete()
                return redirect('cuahang')
        
            
            context={'goimons':goimons,'sum':sum}
            return render(request,'app/thanhtoan.html',context)
        else:
            return redirect('cuahang')
    else:
        return redirect('login')
def thanhtoanmomo():
    profile_url = f'https://www.facebook.com/profile.php?id=100009327356134'
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(profile_url)
    qr.make(fit=True)

    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.show()


#Xử lý QL nhân viên
def nhanvien(request):
    er=""
    if request.user.is_authenticated:
        user = request.user 
        if request.method == 'POST':
            #Thêm nhân viên
            if 'themnv' in request.POST:
                form = nhanvienForm(request.POST)
                if form.is_valid():
                    nhanvien = Nhanvien(
                            user=user,
                            hoten=form.cleaned_data['hoten'],
                            namsinh=form.cleaned_data['namsinh'],
                            diachi=form.cleaned_data['diachi'],
                            giocong=0,
                            sdt=form.cleaned_data['sdt'],
                            mucluong=form.cleaned_data['mucluong'],
                        )
                    nhanvien.save()
                    return redirect('nhanvien')
            elif 'xoanhanvien' in request.POST:
                id=request.POST['xoa-nhanvien']
                obj = Nhanvien.objects.get(user=user,pk=id)
                obj.delete()                
                return redirect('nhanvien')
            
        else:
            form = nhanvienForm()
        nhanviens=Nhanvien.objects.filter(user=user)     
        return render(request, 'app/nhanvien.html', {'form': form,'nhanviens':nhanviens,'er':er})
    else:
        return redirect('login')
def suanhanvien(request,nv_id):
    if request.user.is_authenticated:
        user = request.user
        nv = get_object_or_404(Nhanvien, user=user,pk=nv_id)
        
        if request.method == 'POST':
            formnv=nhanvienForm(request.POST or None,instance=nv)
            if formnv.is_valid():
                formnv.save()
                return redirect('nhanvien')
        else:
            formnv = nhanvienForm(instance=nv)
        return render(request,'app/suanhanvien.html',{'forms':formnv})
    else:
        return redirect('login')
#Xử lý doanh thu
def doanhthu(request):
    if request.user.is_authenticated:
        user=request.user
        ngay=""
        sum=0
        kieu=""
        thangdt=""
        thang=""
        top_10_san_pham_ban_chay =""
        if request.method == 'POST':
            ngayrq=request.POST.get('ngay',None)
            loai=request.POST.get('loaitim-select',None)
            
            if ngayrq:
                if loai=="ngay":
                    kieu="Ngày"
                    datetime_ngay = datetime.strptime(ngayrq, '%Y-%m-%d')
                    # Lấy giá trị tháng từ đối tượng datetime
                    ngay = ngayrq
                    doanhthu=Donhang.objects.filter(user=user,thoigiantao__date=ngayrq)
                    for don in doanhthu:
                        sum+=don.thanhtien
                    
                else:
                    kieu="Tháng"
                    datetime_ngay = datetime.strptime(ngayrq, '%Y-%m-%d')
                    # Lấy giá trị tháng từ đối tượng datetime
                    thangdt = datetime_ngay.month
                    doanhthu=Donhang.objects.filter(user=user,thoigiantao__month=thangdt)
                    for don in doanhthu:
                        sum+=don.thanhtien
                datetime_thang = datetime.strptime(ngayrq, '%Y-%m-%d')
                thang = datetime_thang.month
                # Truy vấn để lấy top 10 sản phẩm bán chạy nhất trong tháng
                top_10_san_pham_ban_chay = (
                    CtDonhang.objects.filter(donhang__thoigiantao__month=thang)
                    .select_related('mon')
                    .values('mon_id', 'mon__tenmon','mon__anh')
                    .annotate(sold_count=Count('mon_id'))
                    .order_by('-sold_count')[:10])
                
                
            else:
                return redirect('doanhthu')
        return render(request,'app/doanhthu.html',{'tongtien':sum,'kieu':kieu,'thangdt':thangdt,'thang':thang,'ngay':ngay,'top10': top_10_san_pham_ban_chay})
    else:
        return redirect('login')  
#Xử lý kho
def khohang(request):
    er=""
    if request.user.is_authenticated:
        user = request.user 
        if request.method == 'POST':
            #Thêm loại món ăn
            if 'themhang' in request.POST:
                trangthai=request.POST['trangthaithem']
                if trangthai=="themmoi":
                    form = hangForm(request.POST)
                    if form.is_valid():
                        hang = Khohang(
                            user=user,
                            tennvl=form.cleaned_data['tennvl'],
                            mota=form.cleaned_data['mota'],
                            dvt=form.cleaned_data['dvt'],
                            soluong=form.cleaned_data['soluong'],
                            giatien=form.cleaned_data['giatien'],
                        )
                        tt=ThongtinKho(
                            user=user,
                            nvl=hang,
                            soluongnhap=form.cleaned_data['soluong'],
                            kieunhap='Thêm mới',
                            ngaynhap=datetime.now()
                        )
                        if Khohang.objects.filter(user=request.user,tennvl=form.cleaned_data['tennvl']).exists():
                            er="Món đã tồn tại"
                        else:
                            hang.save()
                            tt.save()
                            return redirect('khohang')
                else:
                    hang=Khohang.objects.get(user=request.user,pk=request.POST['ma'])
                    slmoi=int(request.POST['soluongmoi'])
                    hang.soluong+=slmoi
                    tt=ThongtinKho(
                            user=user,
                            nvl=hang,
                            soluongnhap=slmoi,
                            kieunhap="Thêm số lượng",
                            ngaynhap=datetime.now()
                        )
                    hang.save()
                    tt.save()
                    return redirect('khohang')
            elif 'xoakho' in request.POST:
                id=request.POST['xoa-kho']
                obj = Khohang.objects.get(user=user,pk=id)
                obj.delete()
                return redirect('khohang')
            elif 'trunvl' in request.POST:
                id=request.POST['matru']
                obj = Khohang.objects.get(user=user,pk=id)
                slban=int(request.POST['soluongban'])
                obj.soluong-=slban
                ngayban=request.POST.get('ngayban',None)
                if ngayban:
                    datetime_ngay = datetime.strptime(ngayban, '%Y-%m-%d')
                else:
                    datetime_ngay=datetime.now()
                tt=ThongtinKho(
                            user=user,
                            nvl=obj,
                            soluongnhap=slban,
                            kieunhap="Trừ số lượng bán",
                            ngaynhap=datetime_ngay
                        )
                obj.save()
                tt.save()
                return redirect('khohang')
        else:
            form = hangForm()
        khohangs=Khohang.objects.filter(user=user)  
        return render(request, 'app/khohang.html', {'form': form,'khohangs':khohangs,'er':er})
    else:
        return redirect('login')
def suakho(request,kho_id):
    if request.user.is_authenticated:
        user = request.user
        nvl = get_object_or_404(Khohang, user=user,pk=kho_id)
        if request.method == 'POST':
            formnvl=hangsuaForm(request.POST or None,instance=nvl)
            if formnvl.is_valid():
                formnvl.save()
                return redirect('khohang')
        else:
            formnvl = hangsuaForm(instance=nvl)
        return render(request,'app/suakho.html',{'forms':formnvl})
    else:
        return redirect('login')
def ttnhaphang(request):
    if request.user.is_authenticated:
        user=request.user

        tts=ThongtinKho.objects.filter(user=user).order_by('-ngaynhap')
        return render(request, 'app/ttnhaphang.html', {'tts': tts})
    else:
        return redirect('login')

#Xử lý đơn hàng
def donhang(request):
    if request.user.is_authenticated:
        user=request.user
        if request.method == 'POST':
            id=request.POST['xoa-don']
            donhang=Donhang.objects.get(user=user,pk=id)
            donhang.delete()
        donhangs=Donhang.objects.filter(user=user)
        return render(request, 'app/donhang.html', {'donhangs': donhangs})
    else:
        return redirect('login')
def ctdonhang(request,donhang_id):
    if request.user.is_authenticated:
        user=request.user
        ctdonhangs=CtDonhang.objects.filter(user=user,donhang_id=donhang_id)
        return render(request, 'app/ctdonhang.html', {'ctdonhangs': ctdonhangs,'id':donhang_id})
    else:
        return redirect('login')