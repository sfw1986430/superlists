from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm

User = get_user_model()
# Create your views here.
# render(request, template_name, context=None, content_type=None, status=None, using=None)方法
# 此方法的作用---结合一个给定的模板和一个给定的上下文字典，并返回一个渲染后的 HttpResponse 对象。通俗的讲就是把context的内容, 加载进templates中定义的文件, 并通过浏览器渲染呈现.
# 1.request: 是一个固定参数, 没什么好讲的。2.template_name: templates 中定义的文件, 要注意路径名. 比如'templates\polls\index.html', 参数就要写‘polls\index.html’
# 3 context: 要传入文件中用于渲染呈现的数据, 默认是字典格式
# 4 测试
def home_page(request):
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_text'])
    #     return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'lists/home.html', {'form':ItemForm()})

# def new_list(request):
#     form = ItemForm(data=request.POST)
#     if form.is_valid():
#         list_ = List()
#         if request.user.is_authenticated:
#             list_.owner = request.user
#         list_.save()
#         form.save(for_list=list_)
#         return redirect(list_)
#     else:
#         return render(request, 'lists/home.html',{"form": form})

def new_list(request):
    form = NewListForm(data = request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, 'lists/home.html', {"form": form})

# def add_item(request, list_id):
#     list_ = List.objects.get(id=list_id)
#     new_item_text = request.POST['item_text']
#     Item.objects.create(text=new_item_text, list=list_)
#     return redirect(f'/lists/{list_.id}/')

def view_list(request,list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    # error = None
    # items = Item.objects.filter(list=list_)
    if request.method == 'POST':
       form = ExistingListItemForm(for_list=list_, data=request.POST)
       if form.is_valid():
           form.save()
           return redirect(list_)
    return render(request, 'lists/list.html', {'list': list_, "form":form})

def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'lists/my_lists.html', {'owner':owner})

def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    list_.shared_with.add(request.POST['sharee'])
    return redirect(list_)
