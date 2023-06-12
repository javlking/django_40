from django.shortcuts import render, redirect
from . import models
# Create your views here.


def main_page(request):
    # получаем все данные о категориях из базы
    all_categories = models.Category.objects.all()
    all_products = models.Product.objects.all()

    # Получить переменную из фронта части, если оно есть
    search_value_from_front = request.GET.get('pr')
    if search_value_from_front:
        all_products = models.Product.objects.filter(name__contains=search_value_from_front)

    # передача переменных из бэка на фронт
    context = {'all_categories': all_categories, 'all_products': all_products}
    return render(request, 'index.html', context)


# Получить продукты из конкретной категории
def get_category_products(request, pk):
    # Получить все товары из конкретной категории
    exact_category_products = models.Product.objects.filter(category_name__id=pk)

    # передача переменных из бэка на фронт
    context = {'category_products': exact_category_products}

    # указать html
    return render(request, 'category.html', context)


# функция получения определенного продукта
def get_exact_product(request, name, pk):
    # Находим из базы продукт
    exact_product = models.Product.objects.get(name=name, id=pk)

    # Передача переменных из бэка на фронт
    context = {'product': exact_product}

    # вывод html
    return render(request, 'product.html', context)


# Функция добавления продукта в корзину
def add_pr_to_cart(request, pk):
    # Получить выбранное количество продукта из front части
    quantity = request.POST.get('pr_count')

    # Находим сам продукт
    product_to_add = models.Product.objects.get(id=pk)

    # Добавление данных
    models.UserCart.objects.create(user_id=request.user.id,
                                   user_product=product_to_add,
                                   user_product_quantity=quantity)

    return redirect('/')


# Получить корзину пользователя
def get_user_cart(request):
    products_from_cart = models.UserCart.objects.filter(user_id=request.user.id)

    context = {'cart_products': products_from_cart}

    return render(request, 'user_cart.html', context)
