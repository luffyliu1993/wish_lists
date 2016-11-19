from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, AddItem

# Create your views here.
def index(request):
    return render(request,'exam/index.html')

def login_check(request):
    login_messages = User.userManager.login(request.session,str(request.POST['user_name']),str(request.POST['password']))
    if login_messages[0]:
        return redirect('/dashboard')
    for message in login_messages[1]['errors']:
        messages.add_message(request,messages.ERROR,message,extra_tags='login')
    return redirect('/main')

def register(request):
    register_messages = User.userManager.register_check(request.session,str(request.POST['name']),\
            str(request.POST['user_name']),str(request.POST['password']),str(request.POST['conf_pw']))
    if register_messages[0]:
        return redirect('/dashboard')
    for message in register_messages[1]['errors']:
        messages.add_message(request,messages.ERROR,message,extra_tags='register')
    return redirect('/main')

def add_item(request):
    return render(request,'exam/create.html')

def process_add(request):
    item = str(request.POST['item'])
    result = AddItem.addItemManager.add_item(request.session,item)
    if result[0]:
        return redirect('/dashboard')
    messages.add_message(request,messages.ERROR,result[1])
    return redirect('/wish_items/create')

def show_dashboard(request):
    user = User.userManager.get(id=request.session['id'])
    my_wish_list = AddItem.addItemManager.filter(wish_users=user)
    other_wish_list = AddItem.addItemManager.exclude(wish_users=user)
    data = {
        'user': user,
        'my_wish_list' : my_wish_list,
        'other_wish_list':other_wish_list
    }
    return render(request,'exam/show_wish_lists.html',data)

def show_item(request,item_id):
    item = AddItem.addItemManager.get(id=item_id)
    data = {
        'item':item,
        'wish_lists':item.wish_users.all()
    }
    return render(request,'exam/show_item.html',data)

def add_wish(request,item_id):
    item = AddItem.addItemManager.get(id=item_id)
    user = User.userManager.get(id=request.session['id'])
    item.wish_users.add(user)
    return redirect('/dashboard')

def delete(request,item_id):
    AddItem.addItemManager.get(id=item_id).delete()
    return redirect('/dashboard')

def remove_wish(request,item_id):
    item = AddItem.addItemManager.get(id=item_id)
    user = User.userManager.get(id=request.session['id'])
    item.wish_users.remove(user)
    return redirect('/dashboard')
    
def logout(request):
    request.session.pop('id')
    #AddItem.addItemManager.all().delete()
    return redirect('/main')
