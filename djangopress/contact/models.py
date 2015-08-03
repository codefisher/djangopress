from django.db import models

class MailAddress(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MailLog(models.Model):
    subject = models.CharField(max_length=200, verbose_name="Subject")
    email = models.CharField(max_length=100, verbose_name="E-mail")
    name = models.CharField(max_length=50, verbose_name="Name")
    to = models.ForeignKey(MailAddress, verbose_name="To")
    message = models.TextField(verbose_name="Message")

    def __str__(self):
        return self.subject