from django.contrib import admin

from .models import PostCount, Table


class PostCountAdmin(admin.ModelAdmin):
    list_display = (
        'ip',
        'title',
        'rows',
        'counts',
        'pub_time',
    )
    list_filter = ('pub_time', )


class TableAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'field', 'show', 'expired')


admin.site.register(PostCount, PostCountAdmin)
admin.site.register(Table, TableAdmin)

# Register your models here.

# admin.site.register(Article)
