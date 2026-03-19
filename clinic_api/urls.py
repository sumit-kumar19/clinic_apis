from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from patients.views import PatientViewSet, AppointmentViewSet, StatsView, LoginView

# connect urls to views
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/stats/', StatsView.as_view(), name='stats'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
]

# handle errors
handler404 = 'clinic_api.utils.handle_404'
handler500 = 'clinic_api.utils.handle_500'
