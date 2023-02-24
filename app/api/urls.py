from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app.employee.api.urls import urlpatterns as employee_views
from app.icd_10.api.urls import urlpatterns as icd_10_views
from app.role.api.urls import urlpatterns as role_views
from app.position.api.urls import urlpatterns as positions_views
from app.organization.api.urls import urlpatterns as organizations_views
from app.external_upload_file.api.urls import urlpatterns as external_upload_file_views
from app.scanning.api.urls import urlpatterns as scanning_views
from app.histological_scanners.api.urls import urlpatterns as histological_scannners_views
from app.research.api.urls import urlpatterns as research_views
from app.series.api.urls import urlpatterns as series_views
from app.slide.api.urls import urlpatterns as slide_views
from app.models_log.api.urls import urlpatterns as models_log_views


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + external_upload_file_views + organizations_views + positions_views\
    + role_views + icd_10_views + employee_views + \
    scanning_views + histological_scannners_views + research_views + \
    series_views + slide_views + models_log_views
