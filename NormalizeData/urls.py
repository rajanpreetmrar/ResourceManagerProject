from django.urls import path
from NormalizeData.views import RawDataUploadView

urlpatterns = [
    path('1nf/', RawDataUploadView.as_view(), name='1nf')
]

