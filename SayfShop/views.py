from django.contrib.auth.decorators import login_required
from django.shortcuts import render ,redirect ,get_object_or_404
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib.auth import login, logout , authenticate
from .models import Product , Basket
from .forms import ProductForm

CATEGORIS = [
    'мобильные телефоны',
    'телевизоры',
    'ноутбуки',
    'компьютерные детали',
    'игровые приставки',
    'наушники',
]


def main(request):
    if request.method == 'GET':
        products = Product.objects.all().order_by('-createdDate')[:10]
        return render(request ,'main.html',{'user':request.user ,'products':products,'categorys':CATEGORIS})
    else:
        data = request.POST
        products = Product.objects.all().order_by('-createdDate')
        try:
            if data['name'] != '':
                products = products.filter(name__icontains=data['name'])
            if data['manufacturer'] != '':
                products = products.filter(manufacturer__icontains=data['manufacturer'])
            if data['min'] != '':
                products = products.filter(price__gte=int(data['min']))
            if data['max'] != '':
                products = products.filter(price__lte=int(data['max']))
            if data['category'] in CATEGORIS:
                products = products.filter(category=data['category'])

            name = data['name']
            manufacturer = data['manufacturer']
            min = data['min']
            max = data['max']
            category = data['category']
            if products.count() > 0:

                return render(request, 'main.html', {'user': request.user, 'products': products, 'name':name,'manufacturer':manufacturer,'min':min,'max':max,'category':category,'categorys':CATEGORIS})
            else:
                return render(request, 'main.html', {'user': request.user, 'products': products, 'categorys': CATEGORIS ,'error':'Не найдено ни одного товара','search':data, 'name':name,'manufacturer':manufacturer,'min':min,'max':max,'category':category})
        except:
            return render(request, 'main.html', {'user': request.user, 'products': products, 'categorys': CATEGORIS,'error':'Невалидные данные'})


def signup(request):
    if request.method == "GET":
        if request.user.is_authenticated:
           return redirect('home')
        return render(request , 'signup.html')
    else:
        username = request.POST["username"]
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'error': 'Пользователь с таким именем уже существует'})
            else:
                person = User.objects.create_user(username=username, password=password)
                person.save()
                login(request, person)
                return redirect('home')

        else:
            return render(request, 'signup.html', {'error': 'Пароли не совпадают'})


def loginuser(request):
    if request.method == 'POST':
        Person = authenticate(request,password = request.POST['password'],username=request.POST['username'])

        if Person is None:
            return render(request, 'login.html', {'error': 'Неверные данные для входа'})
        else:
            login(request,Person)
            return redirect('home')
    else:
        if request.user.is_authenticated:
           return redirect('home')
        return render(request,'login.html')

@login_required
def logoutuser(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request,'login.html')

@login_required
def createProduct(request):
    if request.method == 'GET':
        return render(request,'create.html' ,{'form':ProductForm() ,"categorys":CATEGORIS})
    else:
        if  request.POST['category'].lower() in CATEGORIS:
            form = ProductForm(request.POST,request.FILES)
            if form.is_valid():
                product = form.save()
                product.user = request.user
                product.save()

                return redirect('home')
            else:
                return render(request, 'create.html', {'form': ProductForm(), 'error': 'Данный формат фото не поддерживается.Попробуйте еще раз',"categorys":CATEGORIS})

        else:
            return render(request, 'create.html', {'form': ProductForm() ,'error':'Неверные данные'})


def  viewproduct(request ,product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'GET':
        return render(request,'productview.html' , {'product':product})
    else:
        if request.user.is_authenticated:
            if product.count>=1:
                request.user.basket_set.create(product=product)
                return render(request, 'productview.html', {'product': product})
            else:
                return redirect('home')
        else:
            return redirect('login')


@login_required
def basket(request):
    if request.method == 'GET':
        me = User.objects.get(pk=request.user.pk)
        baskets = me.basket_set.all()
        baskets_sum = 0
        for basket in baskets:
            baskets_sum +=basket.product.price
        return render(request ,'basket.html',{'baskets' : baskets ,'sum':baskets_sum})
@login_required
def deleteBasket(request,basket_id):
    basket = get_object_or_404(Basket, pk=basket_id)
    if request.user.basket_set.filter(pk=basket_id).exists():
        Basket.delete(basket)
        return redirect('basket')
    else:
        redirect('basket')
@login_required
def buyBasket(request):
    baskets = Basket.objects.filter(user=request.user)
    if baskets.count() > 0:
        deletedCount = 0
        for basket in baskets:
            productCount = (get_object_or_404(Product,pk=basket.product.pk))
            basketCount = baskets.filter(product=basket.product)
            if basketCount.count() > productCount.count:
                basket.delete()
                deletedCount +=1

        baskets = Basket.objects.filter(user=request.user)
        baskets_sum = 0
        for basket in baskets:
            baskets_sum +=basket.product.price
        if deletedCount > 0:
            return render(request, 'basket.html', {'baskets': baskets, 'sum': baskets_sum,'error':'Некоторые из товаров в корзине были удалены'})

        print(baskets.count())
        for basket in baskets:
            product = Product.objects.get(pk=basket.product.pk)
            product.count -=1
            product.save()

        baskets.delete()


        return redirect('home')
    else:
        redirect('home')
@login_required
def myProducts(request):
    products = request.user.product_set.all().order_by('-createdDate')
    return render(request, 'myproducts.html', {'products':products})

@login_required
def change(request,product_id):
    product = get_object_or_404(Product,pk=product_id,user=request.user)
    if request.method == 'GET':
        form =ProductForm(instance=product)
        return render(request,'changeproduct.html',{'product':product ,'categorys':CATEGORIS ,'form':form})
    else:
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('myProducts')
        else:
            return render(request, 'myproducts.html', {'error': "Невалидные данные.Попробуйте еще раз"})

@login_required
def deleteProduct(request,product_id):
    if request.method == 'POST':
        if request.user.product_set.filter(pk=product_id).exists():
            Product.delete(request.user.product_set.get(pk=product_id))
            return redirect('myProducts')
        else:
            return redirect('home')
    return HttpResponseNotFound()


















