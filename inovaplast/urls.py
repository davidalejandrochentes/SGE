from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('SGE.urls')),
    path('area/', include('SGE_area.urls')),
    path('pc/', include('SGE_pc.urls')),
    path('herramienta/', include('SGE_herramienta.urls')),
    path('maquina/', include('SGE_maquina.urls')),
    path('repuesto/', include('SGE_repuesto.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)