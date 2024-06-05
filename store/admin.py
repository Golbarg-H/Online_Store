from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from store import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [("<10", "Low")]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    models = models.Collection
    ordering = ('title',)
    list_display = ['title', 'products_count']
    search_fields = ['title']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(products_count=Count('product'))

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist') + '?' + urlencode(
            {'collection__id': str(collection.id)}))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {'slug': ['title']}
    list_display = ['title', 'unit_price', 'inventory', 'inventory_status', 'collection_name']
    list_editable = ['inventory']
    list_per_page = 10
    ordering = ('title',)
    list_select_related = ['collection']
    list_filter = ['collection', InventoryFilter]
    actions = ['clear_inventory']
    search_fields = ['title']

    # sort based on another field
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "Good"

    def collection_name(self, product):
        return product.collection.title

    @admin.action(description="Set inventory of selected products to zero")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated.',
                          messages.INFO)


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    ordering = ['user__first_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    autocomplete_fields = ['user']
    list_per_page = 10
    list_select_related = ['user']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(orders_count=Count('order'))

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (reverse('admin:store_order_changelist') + '?' + urlencode(
            {'customer__id': str(customer.id)}))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    min_num = 1
    autocomplete_fields = ['product']
    extra = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id', 'payment_status', 'placed_at', 'customer_name']
    # list_editable = ['inventory']
    list_per_page = 10
    ordering = ('placed_at',)
    list_select_related = ['customer']
    inlines = [OrderItemInline, ]

    def customer_name(self, order):
        return str(order.customer.first_name) + ' ' + str(order.customer.last_name)
