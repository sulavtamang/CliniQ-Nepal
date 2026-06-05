from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # accounts endpoints
    path('api/accounts/', include('accounts.urls')),

    # clinics and doctors endpoints
    path('api/', include('clinics.urls')),  

    # tokens endpoints
    path('api/', include('queues.urls')),  
]
