from django.urls import path
from .views import sub_plan_payment_page, get_plan_prices, payment_confirmation_page, payment_result_page

urlpatterns = [
    path('', sub_plan_payment_page),
    path('<int:plan_id>/', sub_plan_payment_page),
    path('payment-confirmation/', payment_confirmation_page),
    path('get-plan-prices/', get_plan_prices),
    path('payment-result/', payment_result_page)
]