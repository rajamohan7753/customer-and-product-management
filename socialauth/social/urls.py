from django.urls import  path
from social import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

     path('products/', views.products, name='products'),
     path('customer/<str:pk>/', views.customers, name="customer"),
     path('create_order/<str:pk>/', views.create_Order, name="create_order"),
     path('update_order/<str:pk>/', views.Update_Order, name="update_order"),
     path('delete/<str:pk>/', views.delete_Order, name="delete_order"),
     path('logout/', views.logout_view, name='logout')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
