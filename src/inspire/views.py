# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic


class HomePage(generic.TemplateView):
    template_name = "index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomePage, self).dispatch(*args, **kwargs)


class Header(generic.TemplateView):
    template_name = "tpl/header.html"


class Footer(generic.TemplateView):
    template_name = "tpl/footer.html"


class Sidebar(generic.TemplateView):
    template_name = "tpl/sidebar.html"


class ThemePanel(generic.TemplateView):
    template_name = "tpl/theme-panel"


class DashboardView(generic.TemplateView):
    template_name = "views/dashboard.html"


class QuickSideBarView(generic.TemplateView):
    template_name = "tpl/quick-sidebar.html"


class AddReportView(generic.TemplateView):
    template_name = "views/addreport.html"


class AudienceView(generic.TemplateView):
    template_name = "views/audience.html"


class ReportDataTableView(generic.TemplateView):
    template_name = "views/report_datatable.html"
