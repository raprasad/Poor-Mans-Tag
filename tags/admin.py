from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from tags.models import Tag


class TagAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('name', 'note', )
    readonly_fields = ('date_added',)
    list_display = ('name', 'visible', 'slug', 'note', 'date_added',)
    list_filter = ('visible', )
admin.site.register(Tag, TagAdmin)
