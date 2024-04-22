"""
URL configuration for flightManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from applications.views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/flights/', FlightsViewSet.as_view({'get': 'list', 'post': 'create'}), name='flights-list-create'),
    path('api/flights/<uuid:id>/', FlightsViewSet.as_view({'get': 'retrieve'}), name='flights-retrieve'),
    path('api/flights/<uuid:id>:change_status', FlightsViewSet.as_view({'post': 'change_status'}), name='flights-change-status'),
    path('api/flights/<uuid:id>/tickets', FlightsViewSet.as_view({'get': 'list_tickets', 'post': 'create_ticket'}), name='flights-get-tickets'),
    path('api/flights/<uuid:id>/passengers', FlightsViewSet.as_view({'get': 'list_passengers'}), name='flights-get-passengers'),
    path('api/tickets/<uuid:id>:book', TicketsViewSet.as_view({'post': 'book'}), name='book-ticket'),
    path('api/tickets/<uuid:id>', TicketsViewSet.as_view({'get': 'retrieve'}), name='book-ticket'),
    path('api/passengers', PassengerViewSet.as_view({'post': 'create', 'get': 'list'}), name='create-list-passengers'),
    path('api/operations/<uuid:id>', OperationsViewSet.as_view({ 'get': 'get' }), name='ops'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
