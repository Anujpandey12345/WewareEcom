import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Product, Cart, CartItem, Order, OrderItem, Feedback
from .forms import SellerRegistrationForm, BuyerRegistrationForm, ProductForm

# Import recommender system
from .recommender.recommender import Recommender
recommender = Recommender()


def home(request):
    return render(request, 'shop/home.html')


def register_seller(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop:login')
    else:
        form = SellerRegistrationForm()
    return render(request, 'shop/register_seller.html', {'form': form})


def register_buyer(request):
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shop:login')
    else:
        form = BuyerRegistrationForm()
    return render(request, 'shop/register_buyer.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('shop:home')
    return render(request, 'shop/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('shop:home')


@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        messages.error(request, "Only sellers can access this page.")
        return redirect('shop:product_list')

    products = Product.objects.filter(seller=request.user)
    return render(request, 'shop/seller_dashboard.html', {'products': products})


@login_required
def product_add(request):
    if not request.user.is_seller:
        return HttpResponseForbidden('You are not a seller')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('shop:seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'shop/product_add.html', {'form': form})


def product_list(request):
    """Show all products and user-specific recommendations based on likes only."""
    products = Product.objects.filter(is_active=True)
    recommended = []

    if request.user.is_authenticated:
        liked_products = Feedback.objects.filter(user=request.user, value=1).values_list('product_id', flat=True)
        if liked_products:
            try:
                rec_ids = recommender.recommend_for_user(request.user.id, n=6)
                recommended = Product.objects.filter(id__in=rec_ids, is_active=True)
            except Exception:
                recommended = []
        else:
            recommended = []  # No liked products → no recommendations

    return render(request, 'shop/product_list.html', {
        'products': products,
        'recommended': recommended
    })


def product_detail(request, slug):
    """Show single product details + recommendations + user feedback."""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    recommended = []
    user_feedback = 0

    if request.user.is_authenticated:
        # Get user feedback on this product
        feedback_obj = Feedback.objects.filter(user=request.user, product=product).first()
        if feedback_obj:
            user_feedback = feedback_obj.value

        # Recommend only from liked products
        liked_products = Feedback.objects.filter(user=request.user, value=1).values_list('product_id', flat=True)
        if liked_products:
            try:
                rec_ids = recommender.recommend_for_user(request.user.id, n=6, seed_product=product.id)
                recommended = Product.objects.filter(id__in=rec_ids, is_active=True)
            except Exception:
                recommended = []

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'recommended': recommended,
        'user_feedback': user_feedback
    })


@require_POST
def cart_add(request, product_id):
    """Add product to cart."""
    product = get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += 1
            item.save()
    else:
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
    return redirect('shop:cart')


def cart_view(request):
    """Display user’s cart with subtotal."""
    items = []
    subtotal = 0

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.items.select_related('product')
        subtotal = cart.subtotal
    else:
        session_cart = request.session.get('cart', {})
        product_ids = [int(pid) for pid in session_cart.keys()]
        products = Product.objects.filter(id__in=product_ids)
        for p in products:
            q = session_cart[str(p.id)]
            items.append({'product': p, 'quantity': q, 'total_price': p.price * q})
        subtotal = sum(i['total_price'] for i in items)

    return render(request, 'shop/cart.html', {'items': items, 'subtotal': subtotal})


@login_required
def checkout(request):
    """Checkout and create an order."""
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address', '')
        cart, _ = Cart.objects.get_or_create(user=request.user)

        order = Order.objects.create(
            user=request.user,
            total=cart.subtotal,
            shipping_address=shipping_address,
            paid=False
        )

        for ci in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=ci.product,
                quantity=ci.quantity,
                price=ci.product.price
            )

        cart.items.all().delete()
        messages.success(request, "Order placed successfully!")
        return redirect('shop:home')

    return render(request, 'shop/checkout.html')


def api_recommendations(request):
    """Return recommendations in JSON format."""
    user_id = request.GET.get('user_id')
    n = int(request.GET.get('n', 8))
    seed = request.GET.get('seed_product')
    seed_product = int(seed) if seed else None

    if not user_id:
        return JsonResponse({'error': 'user_id required'}, status=400)

    try:
        recs = recommender.recommend_for_user(int(user_id), n=n, seed_product=seed_product)
    except Exception:
        recs = []

    return JsonResponse({'recommendations': recs})


@csrf_exempt
@require_POST
def api_feedback(request):
    """Save feedback (like/dislike) and update recommendations."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=403)

    data = json.loads(request.body)
    product_id = data.get('product_id')
    value = int(data.get('value', 0))

    if product_id is None:
        return JsonResponse({'error': 'product_id required'}, status=400)

    product = get_object_or_404(Product, pk=product_id)
    Feedback.objects.update_or_create(
        user=request.user,
        product=product,
        defaults={'value': value}
    )

    return JsonResponse({'ok': True, 'message': 'Feedback saved successfully!'})
