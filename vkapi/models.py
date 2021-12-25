from django.contrib.auth.models import User
from django.db import models

class Main(models.Model):
    auth = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)
    category = models.CharField(max_length=20, default=False)
    main_info = models.TextField(default=False)


    def get_info(self):
        return self.main_info

