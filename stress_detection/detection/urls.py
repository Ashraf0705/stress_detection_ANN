from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('parameters/', views.parameter_entry, name='parameters'),
    path('results/<str:stress_level>/', views.results, name='results'),  # Updated to accept stress_level as part of the URL
    path('about/', views.about, name='about'),
    path('how_to_use/', views.how_to_use, name='how_to_use'),
]
