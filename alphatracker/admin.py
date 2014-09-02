from django.contrib.contenttypes.models import ContentType

class ContentTypeAdmin(admin.ModelAdmin):
  list_display = ['name', 'app_label']
  fieldsets = (
    ('', {
      'classes': ('',),
      'fields': ('name', 'app_label')
    }),
  )

  admin.site.register(ContentType, ContentTypeAdmin)