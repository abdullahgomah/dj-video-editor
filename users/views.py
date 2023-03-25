from django.shortcuts import render 
from forms import UserUpdateForm, UpdateProfileForm
from models import Profile  
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def profile(request):
    user = request.user 
    profile = Profile.objects.get(user=user) 
    user_update = UserUpdateForm(instance=user)
    profile_update = UpdateProfileForm(instance=profile)
    if request.POST: # Save
        user_update = UserUpdateForm(request.POST, instance=request.user)
        profile_update = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if user_update.is_valid() and profile_update.is_valid():
            # user_update.save(commit=False)
            user_update.save()

            profile_update.save(commit=False) 
            profile_update.user = request.user 
            profile_update.save()
            print('Saved !!!')
            print('save successfully !') # test code 
    else: # Show
        user_update = UserUpdateForm(instance=user)
        profile_update = UpdateProfileForm(instance=profile)

    context = {
        'user_update': user_update,
        'profile_update': profile_update, 
    }
    return render(request, 'users/profile.html', context)
