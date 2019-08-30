"""store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


import django
from django.apps import apps
from django.urls import include, path, re_path  # > Django-2.0
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

# add small site map
# from django.contrib.sitemaps.views import sitemap
# from django.contrib.sitemaps import sitemaps
# from apps.sitemaps import base_sitemaps

# Allow dashboard access
# from apps.gateway import urls as gateway_urls
from oscar.views import handler403, handler404, handler500
# from paypal.payflow.dashboard.app import application as payflow
# from paypal.express.dashboard.app import application as express_dashboard

admin.autodiscover()

urlpatterns = [
    # url(r'^i18n/', include('django.conf.urls.i18n')),
    path('i18n/', include(django.conf.urls.i18n)),  # > Django-2.0

    # The Django admin is not officially supported; expect breakage.
    # Nonetheless, it's often useful for debugging.

    # url(r'^admin/', admin.site.urls),
    path('admin/', admin.site.urls),  # > Django-2.0

    # include a basic sitemap
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    # path('sitemap-<str:section>\.xml',
    #      views.sitemap, {'sitemaps': base_sitemaps},
    #      name='django.contrib.sitemaps.views.sitemap')
    re_path(r'payment', TemplateView.as_view(template_name='checkout/payment_details.html')),
]

# Prefix Oscar URLs with language codes
urlpatterns += i18n_patterns(
    # Custom functionality to allow dashboard users to be created
    # path('gateway/', include(gateway_urls)),

    # PayPal Express integration...
    # re_path(r'checkout/paypal/', include('paypal.express.urls')),

    # Dashboard views for Payflow Pro
    # re_path(r'^basket/', TemplateView.as_view(template_name='base1.html')),

    # Dashboard views for Express
    # re_path(r'^dashboard/paypal/express/', express_dashboard.urls),

    # Oscar's normal URLs
    # url(r'^', include(apps.get_app_config('oscar').urls[0])),
    re_path(r'^', include(apps.get_app_config('oscar').urls[0])),
)

# In debug mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += staticfiles_urlpatterns()
    # Server statics and uploaded media
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # Allow error pages to be tested
    urlpatterns += [
        path('403', handler403, {'exception': Exception()}),
        path('404', handler404, {'exception': Exception()}),
        path('500', handler500),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
