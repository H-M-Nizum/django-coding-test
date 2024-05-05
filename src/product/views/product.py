from django.views import generic
from django.shortcuts import render
from product.models import Variant, Product, ProductVariantPrice
from product.forms import ProductUpdateForm, ProductVariantPriceUpdateForm
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(csrf_protect, name='dispatch')
class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context

class ProductlistView(generic.ListView):
    model =  Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(ProductlistView, self).get_context_data(**kwargs)
        context['variants'] = Variant.objects.all()
        # context['crunchy_kunafa'] = Crunchy_kunafa.objects.all()
        return context


    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtering based on product title
        title = self.request.GET.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        
        # Filtering based on product variant
        # variant = self.request.GET.get('variants')
        # # print("========================== ", variant)
        # if variant:
        #     queryset = queryset.filter(variant__title__icontains=variant)

        # Filtering based on price range
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        if price_from and price_to:
            queryset = queryset.filter(productvariantprice__price__range=(price_from, price_to))

        # Filtering based on date
        date = self.request.GET.get('date')
        print(date)
        if date:
            queryset = queryset.filter(created_at__date=date)
            print(queryset)
        
        return queryset





class UpdateProductView(generic.UpdateView):
    model = Product
    form_class = ProductUpdateForm  
    template_name = 'products/update.html' 
    success_url = '/product/list/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_instance = self.get_object()
        product_variant_price_instance, created = ProductVariantPrice.objects.get_or_create(product=product_instance)
        context['product_variant_price_instance'] = product_variant_price_instance
        context['product_variant_price_form'] = ProductVariantPriceUpdateForm(instance=product_variant_price_instance)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        product_variant_price_form = context['product_variant_price_form']
        if form.is_valid() and product_variant_price_form.is_valid():
            form.save()
            product_variant_price_form.save()
        return super().form_valid(form)