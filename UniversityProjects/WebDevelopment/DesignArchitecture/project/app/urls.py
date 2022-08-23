from django.urls import path
from . import views


"""
Possible URL extensions
"""
urlpatterns = [
    path('', views.default, name='default'),    # Redirect to login when default URL used
    path('login', views.login, name='login'),
    path('index', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    path('searchTestSites', views.searchTestSites, name='searchTestSites'),
    path('homeBook', views.homeBook, name='homeBook'),
    path('checkBooking', views.checkBooking, name='checkBooking'),
    path('editBooking', views.editBooking, name='editBooking'),
    path('revertBooking', views.revertBooking, name='revertBooking'),
    path('onsiteBook', views.onsiteBook, name='onsiteBook'),
    path('adminInterface', views.adminInterface, name='adminInterface'),
    path('onsiteTest', views.onsiteTest, name='onsiteTest'),
]
