
from djangopress.accounts.profiles import register, Profile
from djangopress.forum.models import ForumUser

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
        
register('forum', ForumUserProfile)