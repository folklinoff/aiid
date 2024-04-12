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
from applications.views import FlightsViewSet, TicketsViewSet, PassengerViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/flights/', FlightsViewSet.as_view({'get': 'list', 'post': 'create'}), name='flights-list-create'),
    path('api/flights/<str:id>/', FlightsViewSet.as_view({'get': 'retrieve', 'patch': 'update'}), name='flights-retrieve-update'),
    path('api/flights/<str:id>/tickets', FlightsViewSet.as_view({'get': 'list_tickets', 'post': 'create_ticket'}), name='flights-get-tickets'),
    path('api/flights/<str:id>/passengers', FlightsViewSet.as_view({'get': 'list_passengers'}), name='flights-get-passengers'),
    path('api/tickets/<str:id>/book', TicketsViewSet.as_view({'post': 'book'}), name='book-ticket'),
    path('api/passengers', PassengerViewSet.as_view({'post': 'create', 'get': 'list'}), name='create-list-passengers'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]
