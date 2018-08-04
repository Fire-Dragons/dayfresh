from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import View
from utils.minix_util import LoginRequiredMinix
from .models import Address



class address(LoginRequiredMinix,View):
    def get(self,request):
        context={}
        context['page'] = 'site'
        user=request.user
        context['input'] = '提交'
        if Address.objects.filter(user=user).exists():
            addres=Address.objects.filter (user=user)
            context['addres']=addres
        return render (request, 'user/user_center_site.html', context)

    def post(self,request):
        user=request.user
        receiver=request.POST['receiver']
        addr=request.POST['addr']
        zip_code=request.POST['zip_code']
        phone=request.POST['phone']

        if Address.objects.filter(user=user).exists():
            addres = Address.objects.filter(user=user)
            for add in addres:
                add.is_default=False
                add.save()

        Address.objects.create(user=user,receiver=receiver,addr=addr,zip_code=zip_code,phone=phone)

        addres = Address.objects.all()
        context = {}
        context['addres']=addres
        return redirect('/address')

#修改地址
class Update(LoginRequiredMinix,View):
    def get(self,request,adid):
        context={}
        user = request.user
        addres = Address.objects.filter (user=user)
        add = Address.objects.get (id=adid)
        context['addres'] = addres
        context['add']=add
        context['input']='修改'
        return render(request,'user/user_center_site.html', context)

    def post(self,request,adid):
        add = Address.objects.get(id=adid)
        add.receiver = request.POST['receiver']
        add.addr = request.POST['addr']
        add.zip_code = request.POST['zip_code']
        add.phone = request.POST['phone']
        add.save()
        return redirect('/address')

#删除地址
@login_required
def remove(request,adid):
    Address.objects.filter(id=adid).delete()
    return redirect('/address')

#设为默认地址
@login_required
def set_default(request,adid):
    addres=Address.objects.all()
    for add in addres:
        add.is_default=False
        add.save()
    add=Address.objects.get(id=adid)
    add.is_default=True
    add.save()
    return redirect('/address')