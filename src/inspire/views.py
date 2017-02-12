from django.views import generic


class HomePage(generic.TemplateView):
    template_name = "index.html"

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
