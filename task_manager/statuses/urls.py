from django.urls import path
from . import views

app_name = 'statuses'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create', views.CreateStatusView.as_view(), name='create'),
    path('<int:pk>/update', views.UpdateStatusView.as_view(), name='update'),
    path('<int:pk>/delete', views.DeleteStatusView.as_view(), name='delete')
]
