from django.contrib.auth.models import User
from django.db import models

class Subscription(models.Model):

    tg_user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    category = models.CharField(max_length=20)
    main_info = models.TextField()


    def get_info(self):
        return self.main_info

