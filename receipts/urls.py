# from django.urls import path
# from . import views

# urlpatterns = [
#     path('upload', views.upload_receipt),
#     path('validate', views.validate_receipt),
#     path('process', views.process_receipt),
#     path('receipts', views.list_receipts),
#     path('receipts/<int:id>', views.get_receipt),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload', views.upload_receipt, name='upload'),
    path('validate', views.validate_receipt, name='validate'),
    path('process', views.process_receipt, name='process'),
    path('receipts', views.list_receipts, name='list_receipts'),
    path('receipts/<int:id>', views.get_receipt, name='get_receipt'),
]
