from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('welcome/', views.welcome, name='welcome'),
    path('parameter_entry/', views.parameter_entry, name='parameter_entry'),
    path('results/<str:stress_level>/', views.results, name='results'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('how_to_use/', views.how_to_use, name='how_to_use'),
    path('maintain_low_stress/', views.maintain_low_stress, name='maintain_low_stress'),
    path('overcome_stress/', views.overcome_stress, name='overcome_stress'),
]
