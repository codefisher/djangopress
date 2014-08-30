
from django import forms
from djangopress.accounts.profiles import register, Profile, ProfileText
from djangopress.forum.models import ForumUser, Thread
from django.template.loader import render_to_string

class ForumProfileForm(forms.ModelForm):
    
    class Meta:
        model = ForumUser
        fields = ('notify', 'show_simlies', 'show_img', 'show_avatars', 'show_sig')

    fieldsets = (
        ("Forum Email Settings", ('notify', )),
        ("Forum Display Settings", ('show_simlies', 'show_img', 'show_avatars', 'show_sig')),
    )

class ForumUserProfile(Profile):
    label = "Forum Settings"
    
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
        subscriptions = render_to_string("forum/profile_subscriptions.html", {"user": self._user})
        return {
                "forms": [form, ProfileText(subscriptions)],
        }
    
    def admin(self, request):
        pass
        
register('forum', ForumUserProfile)

class ForumSubscriptionProfile(Profile):
    label = "Thread Subscriptions"
    show_tab = False
    
    def info(self):
        return {}
        
    def edit(self, request):
        if request.method == 'POST':
            for thread_id in request.POST.getlist('thread'):
                thread = Thread.objects.get(pk=thread_id)
                if thread:
                    self._user.forum_subscriptions.remove(thread)
        data = {
                "user": self._user,
                "subscriptions": self._user.forum_subscriptions.all()
        }
        return {
                "forms": [ProfileText(render_to_string("forum/subscriptions.html", data))],
        }
    
    def admin(self, request):
        pass
        
register('forum_subscription', ForumSubscriptionProfile)