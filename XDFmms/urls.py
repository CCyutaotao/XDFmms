
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^mms/', include('mms.mmsURLS')),
    url(r'^docs/', include('rest_framework_docs.urls')),
]
