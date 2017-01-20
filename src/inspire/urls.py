from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^$', views.HomePage.as_view(), name='home'),
	url(r'^tpl/header$', views.Header.as_view(), name='header'),
	url(r'^tpl/footer$', views.Footer.as_view(), name='footer'),
	url(r'^tpl/sidebar$', views.Sidebar.as_view(), name='sidebar'),
	url(r'^tpl/theme-panel$', views.Sidebar.as_view(), name='theme_panel'),
	url(r'^view/dashboard$', views.DashboardView.as_view(), name='dashboard'),
	url(r'^view/quick-sidebar$', views.QuickSideBarView.as_view(), name='quick_sidebar'),
	url(r'^admin/', include(admin.site.urls)),
]

# User-uploaded files like profile pics need to be served in development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Include django debug toolbar if DEBUG is on
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
