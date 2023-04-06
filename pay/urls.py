from django.urls import path
from .views import plan_details , plans
from django.conf import settings
from django.conf.urls.static import static

app_name = "pay"




urlpatterns = [
    path("plans/", plans, name="plans"),
    path("plan_detalis/<int:id>", plan_details, name="plan_detalis"),

]
