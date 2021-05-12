from django.contrib import admin

class ModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return self.model.objects.get_queryset()

