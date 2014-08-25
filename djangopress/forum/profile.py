
from django import forms
from djangopress.accounts.profiles import register, Profile
from djangopress.forum.models import ForumUser

class ForumProfileForm(forms.ModelForm):
    
    class Meta:
        model = ForumUser
        fields = ('notify', 'show_simlies', 'show_img', 'show_avatars', 'show_sig')

    fieldsets = (
        ("Forum Email Settings", ('notify', )),
        ("Forum Display Settings", ('show_simlies', 'show_img', 'show_avatars', 'show_sig')),
    )

class ForumUserProfile(Profile):
    def info(self):
        forum_profile = ForumUser.objects.get_or_create(user=self._user)[0]
        return {
                "template": "forum/profile.html",
                "title": "Forum",
                "data": {
                       "forum_profile": forum_profile,
                }
        }
        
    def edit(self, request):
        forum_profile = ForumUser.objects.get_or_create(user=self._user)[0]
        if request.method == 'POST':
            form = ForumProfileForm(request.POST, instance=forum_profile)
            if form.is_valid():
                form.save(True)
        else:
            form = ForumProfileForm(instance=forum_profile)
        return {
                "forms": [form],
        }
    
    def admin(self, request):
        pass
        
register('forum', ForumUserProfile)