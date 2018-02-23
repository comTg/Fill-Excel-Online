from django.contrib import admin

from .models import PostCount,Table

class PostCountAdmin(admin.ModelAdmin):
    list_display = ('ip','title','times',)

class TableAdmin(admin.ModelAdmin):
    list_display = ('title','field','show','count')


admin.site.register(PostCount,PostCountAdmin)
admin.site.register(Table,TableAdmin)

# Register your models here.

# admin.site.register(Article)
