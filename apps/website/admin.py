from django.contrib import admin
from .models import WebSite, TipoProducto, Producto, Horario, CararteristicaProducto, BannerPrincipal, Email, Telefono, \
    EnlacesGubernamentales, SubCategoriaSobreNosotros, CategoriaSobreNosotros

admin.site.register(WebSite)
admin.site.register(TipoProducto)
admin.site.register(Producto)
admin.site.register(Horario)
admin.site.register(CararteristicaProducto)
admin.site.register(BannerPrincipal)
admin.site.register(Email)
admin.site.register(EnlacesGubernamentales)
admin.site.register(Telefono)


class CategoriaAdmin(admin.TabularInline):
    model = SubCategoriaSobreNosotros


class SubcategoriaAdmin(admin.ModelAdmin):
    inlines = (CategoriaAdmin,)


admin.site.register(CategoriaSobreNosotros,SubcategoriaAdmin)