from django.contrib import admin
from .models import Country, DocumentSet, Customer, CustomerDocument

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(DocumentSet)
class DocumentSetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('countries',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'surname', 'nationality', 'gender', 'created_by')

@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at')
