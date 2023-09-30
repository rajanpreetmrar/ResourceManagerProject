from django.urls import path
from NormalizeData.views import FirstNormalForm

urlpatterns = [
    path('1nf/', FirstNormalForm.as_view(), name='1nf')
]

