from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import *
from .utils import cookieCart, cartData, guestOrder
from tech import helpers
from tech.decorators import *
from django.contrib.auth.decorators import login_required, permission_required
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#from taggit.models import Taggit
from .forms import *
import json
import datetime

# Create your views here.

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all().order_by('-id')
    products = helpers.pg_records(request, products, 12)
    cat_menu_list = ProductCategory.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = (
            Q(name__icontains=query)|
            Q(price__icontains=query)
            )
        products = Product.objects.filter(queryset).distinct()
    else:
        queryset = Product.objects.all()

    context = {'products': products, 'cartItems': cartItems, 'cat_menu_list': cat_menu_list, 'query': query}
    return render(request, 'ecommerce/store.html', context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    cat_menu_list = ProductCategory.objects.all()

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'cat_menu_list': cat_menu_list}
    return render(request, 'ecommerce/cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    cat_menu_list = ProductCategory.objects.all()

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'cat_menu_list': cat_menu_list}
    return render(request, 'ecommerce/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)

def ProductCategoryView(request, category_slug):
    data = cartData(request)
    cartItems = data['cartItems']

    category = get_object_or_404(ProductCategory, slug=category_slug)
    product = get_list_or_404(Product.objects.order_by('-id'), category=category)
    product = helpers.pg_records(request, product, 12)
    cat_menu_list = ProductCategory.objects.all()
        
    template = 'ecommerce/product_category.html'
    context = {'product': product, 'category': category, 'cat_menu_list': cat_menu_list, 'cartItems': cartItems}
    
    return render(request, template, context)

def ProductDetailView(request, pk, slug):
    data = cartData(request)
    cartItems = data['cartItems']

    product = get_object_or_404(Product, pk=pk, slug=slug)
    product_related = product.tags.similar_objects()[:6]
    cat_menu_list = ProductCategory.objects.all()

    context = {
        'product': product,
        'product_related': product_related,
        'cartItems': cartItems,
        'cat_menu_list': cat_menu_list
    }

    return render(request, 'ecommerce/product_detail.html', context)

@login_required
@admin_only
def ProductCreateView(request):
    ImageFormset = modelformset_factory(ProductImages, fields=('image',), extra=4)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()

            for f in formset:
                try:
                    photo = ProductImages(product=product, image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break
            
            messages.success(request, 'Post created successfully.')
            return HttpResponseRedirect(product.get_absolute_url())
    else:
        form = ProductForm()
        formset = ImageFormset(queryset=ProductImages.objects.none())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'ecommerce/product_form.html', context)

@login_required
@admin_only
def ProductImageUpdate(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug)
    ImageFormset = modelformset_factory(ProductImages, fields=('image',), extra=4, max_num=4)
    if product.author != request.user:
        raise Http404()

    if request.method == 'POST':
#        form = ForumUpdateForm(request.POST or None, instance=product)
        formset = ImageFormset(request.POST or None, request.FILES or None)
#        if form.is_valid() and formset.is_valid():
        if formset.is_valid():
#            formset.save()
            print(formset.cleaned_data)
            data = ProductImages.objects.filter(product=product)
            for index, f in enumerate(formset):
                if f.cleaned_data:
                    if f.cleaned_data['id'] is None:
                        photo = ProductImages(product=product, image=f.cleaned_data.get('image'))
                        photo.save()
                    elif f.cleaned_data['image'] is False:
                        photo = ProductImages.objects.get(id=request.POST.get('form-' + str(index) + '-id'))
                        photo.delete()
                    else:
                        photo = ProductImages(product=product, image=f.cleaned_data.get('image'))
                        d = ProductImages.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()
            
            messages.success(request, 'Image uploaded successfully.')
            return HttpResponseRedirect(product.get_absolute_url())
#            return redirect('forum_detail')
    else:
#        form = ForumUpdateForm()
        formset = ImageFormset(queryset=ProductImages.objects.filter(product=product))
    context = {
#        'form': form,
        'product': product,
        'formset': formset,
    }
    return render(request, 'ecommerce/product_update_image.html', context)



class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    model = Product
    template_name = 'ecommerce/product_form.html'
    fields = ['name', 'category', 'image', 'description', 'price', 'digital', 'tags']
    slug_field ='slug'
    query_pk_and_slug = True
    success_message = 'Post updated successfully.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False

    
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    model = Product
    template_name = 'ecommerce/product_delete.html'
    slug_field ='slug'
    query_pk_and_slug = True
    success_url = 'store'

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.author:
            return True
        return False

    def get_success_url(self):
        messages.warning(self.request, 'Post deleted successfully.')
        return reverse('store')


class StoreCategory(generic.ListView):
    model = Product
    template_name = 'ecommerce/store_category.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = ProductCategory.objects.all()
        context = super(StoreCategory, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context