
from djangopress.accounts.profiles import register, Profile

class UserProfile(Profile):
    def info(self):
        return {
                "position": -1,
                "template": "accounts/profile.html",
                "title": "Personal",
                "data": {
                       
                }
        }
    
register('user', UserProfile)