from django.contrib import admin

from .models import Term, Definition


# Register your models here.
admin.site.register(Term)


class DefinitionForm(admin.ModelAdmin):
    list_display = ["term", "username"]
    search_fields = ["term"]


admin.site.register(Definition, DefinitionForm)
