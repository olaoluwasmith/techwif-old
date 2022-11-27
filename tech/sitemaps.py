from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import *


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['about']
    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    def items(self):
        return Blog.objects.all()

"""
class ForumSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    def items(self):
        return Forum.objects.all()
"""


SITEMAPS = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
 #   'forum': ForumSitemap,
}

