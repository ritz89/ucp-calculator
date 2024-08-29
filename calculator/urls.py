from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_project/', views.create_project, name='create_project'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/add_actor/', views.add_actor, name='add_actor'),
    path('project/<int:project_id>/add_use_case/', views.add_use_case, name='add_use_case'),
    path('project/<int:project_id>/add_transaction/', views.add_transaction, name='add_transaction'),
]
