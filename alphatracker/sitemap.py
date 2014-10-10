from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from content.models import Post


info_dict = {
    'queryset': Post.objects.filter(deleted=False, flagged=False),
    'date_field': 'updated_on'
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'posts': GenericSitemap(info_dict, priority=0.6)
}