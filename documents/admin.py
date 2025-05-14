from django.contrib import admin
from .models import UrlDocument, DocumentStage, DocumentType, Carrer, FileDocument

# Filtro personalizado por ID
class DocumentIDFilter(admin.SimpleListFilter):
    title = 'Document ID'
    parameter_name = 'id'

    def lookups(self, request, model_admin):
        # Opcional: Podrías devolver IDs recientes o los primeros 10 por rendimiento
        ids = UrlDocument.objects.order_by('-id').values_list('id', flat=True)[:10]
        return [(id, str(id)) for id in ids]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id=self.value())
        return queryset

class UrlDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url', 'year')
    search_fields = ('id', 'title', 'url', 'year')
    list_filter = ('title', 'url', 'year')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Si en la URL hay ?id= , filtra por ID exacto
        doc_id = request.GET.get('id')
        if doc_id:
            qs = qs.filter(id=doc_id)
        return qs


admin.site.register(UrlDocument, UrlDocumentAdmin)
admin.site.register(FileDocument)
admin.site.register(DocumentStage)
admin.site.register(DocumentType)
admin.site.register(Carrer)
