from userprofile.models import UserProfile


def userprofile_processor(request):
    if request.user.is_authenticated():
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            return {'gravatar_url': user_profile.gravatar_url}
        except UserProfile.DoesNotExist:
            pass

    return {}