from django.urls import path
from NormalizeData.views import RawDataUploadView, FeedHospitalDataView, FeedHospitalExpensesView

urlpatterns = [
    path('RawDataUpload/', RawDataUploadView.as_view(), name='RawDataUpload'),
    path('FeedHospitalData/', FeedHospitalDataView.as_view(), name='FeedHospitalData'),
    path('FeedHospitalExpenses/', FeedHospitalExpensesView.as_view(), name='FeedHospitalExpensesView')
]

