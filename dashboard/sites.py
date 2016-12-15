#-*- coding: UTF-8 -*-
from __future__ import unicode_literals
from django.contrib.admin.sites import AdminSite
from django.conf.urls import url
from dashboard.views import DashboardMainView


class AdminMixin(object):
    """Mixin for AdminSite to allow custom dashboard views."""

    def get_urls(self):
        """Add dashboard view to admin urlconf."""
        urls = super(AdminMixin, self).get_urls()
        del urls[0]
        custom_url = [
            url(r'^$', self.admin_view(DashboardMainView.as_view()), name="index")
        ]

        return custom_url + urls


class DashboardSite(AdminMixin, AdminSite):
    """
    A Django AdminSite with the AdminMixin to allow registering custom dashboard view.
    """
    pass