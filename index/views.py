from django.shortcuts import render, redirect
from .models import Category, Product
from .forms import RegForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views import View


# Create your views here.
# Главная страница
def home_page(request):
    # Вывод всех данных из БД
    categories = Category.objects.all()
    products = Product.objects.all()

    # Передаем данные на фронт
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'home.html', context)


# Вывод товаров по категории
def category_page(request, pk):
    # Достаем данные из БД
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(product_category=category)

    # Передаем данные на фронт
    context = {
        'category': category,
        'products': products
    }

    return render(request, 'category.html', context)

# Вывод определенного товара
def product_page(request, pk):
    # Достаем данные из БД
    product = Product.objects.get(id=pk)

    # Отправляем данные на фронт
    context = {
        'product': product
    }

    return render(request, 'product.html', context)

# Регистрация
class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {'form': RegForm}

        return render(request, self.template_name, context)


    def post(self, request):
        form = RegForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')

            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()

            login(request, user)
            return redirect('/')


# Поиск продукта
def search_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')
        searched_product = Product.objects.filter(product_name__iregex=get_product)

        if searched_product:
            context = {'products': searched_product}
            return render(request, 'result.html', context)
        else:
            return redirect('/')


# Log out
def logout_view(request):
    logout(request)
    return redirect('/')
