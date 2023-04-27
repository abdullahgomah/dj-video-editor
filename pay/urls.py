from django.urls import path
from .views import plan_details , plans, create_subscription, videos_limit_end
from django.conf import settings
from django.conf.urls.static import static

app_name = "pay"




urlpatterns = [
    path("plans/", plans, name="plans"),
    path("plan_detalis/<int:id>", plan_details, name="plan_detalis"),
    path("create_subscription/", create_subscription, name='create-subscription'),
    path('limit_ended/', videos_limit_end, name='video_limit_end'), 
]
