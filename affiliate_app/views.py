from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .models import Product, Category
from .forms import ProductForm, CategoryForm, StaffLoginForm
from .utils import staff_required
    
# Public Views
def public_home(request):
    # Debug info
    print("=== DEBUG: Memulai query produk ===")
    
    products = Product.objects.filter(
        is_active=True,
        category__is_active=True  
    ).select_related('category').order_by('-created_at')
    
    print(f"Jumlah produk aktif: {products.count()}")
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query))
        print(f"Setelah pencarian '{search_query}': {products.count()} produk")
    
    # Category filter
    category_slug = request.GET.get('category', '')
    if category_slug:
        products = products.filter(category__slug=category_slug)
        print(f"Setelah filter kategori '{category_slug}': {products.count()} produk")
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,  
        'page_obj': page_obj,  
        'categories': Category.objects.filter(is_active=True),
        'search_query': search_query,
        'selected_category': category_slug,
    }
    return render(request, 'affiliate_app/public/home.html', context)

def public_product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Update meta title and description if empty
    if not product.meta_title:
        product.meta_title = product.name
    if not product.meta_description:
        product.meta_description = product.description[:200]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'affiliate_app/public/product_detail.html', context)

def public_category(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Debug output
    print(f"DEBUG: Category '{category.name}' found")
    
    products = Product.objects.filter(
        category=category,
        is_active=True
    ).select_related('category').order_by('-created_at')
    
    print(f"DEBUG: Found {products.count()} active products in this category")
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
        'page_obj': page_obj,
    }
    return render(request, 'affiliate_app/public/category.html', context)

# Dashboard Views
class DashboardLoginView(LoginView):
    template_name = 'affiliate_app/dashboard/login.html'
    form_class = StaffLoginForm
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)

class DashboardLogoutView(LogoutView):
    next_page = 'dashboard_login'

@staff_required
def dashboard_home(request):
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    total_categories = Category.objects.count()
    active_categories = Category.objects.filter(is_active=True).count()
    recent_products = Product.objects.order_by('-created_at')[:5]
    categories = Category.objects.filter(is_active=True).order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'active_products': active_products,
        'total_categories': total_categories,
        'active_categories': active_categories,
        'recent_products': recent_products,
        'categories': categories,
    }
    return render(request, 'affiliate_app/dashboard/home.html', context)

@method_decorator(staff_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'affiliate_app/dashboard/product_list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

@staff_required
def dashboard_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.is_active = True 
            product.save()
            messages.success(request, 'Produk berhasil ditambahkan!')
            return redirect('dashboard_product_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Tambah Produk Baru'
    }
    return render(request, 'affiliate_app/dashboard/product_form.html', context)

@staff_required
def dashboard_product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.updated_by = request.user
            product.save()
            messages.success(request, 'Produk berhasil diperbarui!')
            return redirect('dashboard_product_list')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': 'Edit Produk'
    }
    return render(request, 'affiliate_app/dashboard/product_form.html', context)

@staff_required
def dashboard_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produk berhasil dihapus!')
        return redirect('dashboard_product_list')
    
    context = {'product': product}
    return render(request, 'affiliate_app/dashboard/product_confirm_delete.html', context)

@staff_required
def dashboard_product_toggle_active(request, pk):
    if request.method == 'POST' and request.is_ajax():
        product = get_object_or_404(Product, pk=pk)
        product.is_active = not product.is_active
        product.save()
        return JsonResponse({
            'success': True,
            'is_active': product.is_active
        })
    return JsonResponse({'success': False}, status=400)

@method_decorator(staff_required, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'affiliate_app/dashboard/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.all().annotate(
            product_count=Count('products', filter=Q(products__is_active=True))).order_by('name')

@staff_required
def dashboard_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori berhasil ditambahkan!')
            return redirect('dashboard_category_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Tambah Kategori Baru'
    }
    return render(request, 'affiliate_app/dashboard/category_form.html', context)

@staff_required
def dashboard_category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kategori berhasil diperbarui!')
            return redirect('dashboard_category_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': 'Edit Kategori'
    }
    return render(request, 'affiliate_app/dashboard/category_form.html', context)

@staff_required
def dashboard_category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategori berhasil dihapus!')
        return redirect('dashboard_category_list')
    
    context = {'category': category}
    return render(request, 'affiliate_app/dashboard/category_confirm_delete.html', context)

@staff_required
def dashboard_category_toggle_active(request, pk):
    if request.method == 'POST' and request.is_ajax():
        category = get_object_or_404(Category, pk=pk)
        category.is_active = not category.is_active
        category.save()
        return JsonResponse({
            'success': True,
            'is_active': category.is_active
        })
    return JsonResponse({'success': False}, status=400)

def public_category_list(request):
    categories = Category.objects.filter(is_active=True).annotate(
        active_product_count=Count('products', filter=Q(products__is_active=True))
    )
    context = {
        'categories': categories
    }
    return render(request, 'affiliate_app/public/category_list.html', context)