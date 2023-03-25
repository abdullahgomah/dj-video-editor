from django import template
from ..models import User, Profile

register = template.Library() 

@register.filter(name='user_info')
def user_info (user):
    profile = Profile.objects.get(user=user)
    return profile 


@register.filter(name='user_image')
def user_img(user):
    img_url = Profile.objects.get(user=user).image.url
    return img_url