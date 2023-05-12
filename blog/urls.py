
from django.urls import path
from .views import BlogListView,BlogDetailView,BlogCreateView
from . import views
urlpatterns = [
    path('',BlogListView.as_view(),name = 'home'),
    path('airline/<int:pk>/',BlogListView.as_view(),name = 'post_detail'),
    path('airline/new/',BlogCreateView.as_view(),name = 'post_new'),
    # -------------------------------
    path('findflight/', views.searchflight, name='findflight'),
    path('noSeatAvai/', views.noSeatAvai, name='noSeatAvai'),
    path('findflight/Depart_id=<str:from_city>&Arrival_id=<str:to_city>&Departure_time='
         '<str:datetime>/',views.search_results, name='search_results'),
    path('bookflight/Depart_id=<str:from_city>&Arrival_id=<str:to_city>&Departure_time='
         '<str:datetime>&bookingnumber=<str:booking_number>/', views.book_result, name='book_result'),
    path('getpaymentmethods/bookingnumber=<str:booking_number>/', views.getpaymentmethods, name='getpaymentmethods'),
    path('makepayment/bookingnumber=<str:booking_number>&method=<str:method>/', views.makepayment, name='makepayment'),
    path('confirmPayment/token=<str:token>&bookingnumber=<str:bkn>&email=<str:email>'
         '&method=<str:method>/', views.confirmPayment, name='confirmPayment'),
path('finalConfirm/token=<str:token>&bookingnumber=<str:bkn>&cardpasswordpara=<str:cardpasswordpara>/', views.finalConfirm, name='finalConfirm'),
]
