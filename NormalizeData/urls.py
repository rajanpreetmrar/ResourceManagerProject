from django.urls import path
from NormalizeData.views import RawDataUploadView, FeedHospitalDataView

urlpatterns = [
    path('RawDataUpload/', RawDataUploadView.as_view(), name='RawDataUpload'),
    path('FeedHospitalData/', FeedHospitalDataView.as_view(), name='FeedHospitalData')
]

