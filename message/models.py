from django.db import models
from django.contrib.auth.models import User
from main.models import Bossprofile, Normalprofile
from django.utils import timezone

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="message_sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="message_receiver", on_delete=models.CASCADE)
    sentAt = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=150)
    isRead = models.BooleanField(default=False)

    objects = models.Manager()

    def save(self, **kwargs):
        if not self.id:
            self.sentAt = timezone.now()
        super(Message, self).save(**kwargs)

    class Meta:
        ordering = ['-sentAt']

    def __str__(self):
        return self.content
    
    def summary(self):
        return self.content[:17]

    def senderProfile(self):
        try:
            who = Bossprofile.objects.get(user = self.sender)
        except Bossprofile.DoesNotExist:
            who = Normalprofile.objects.get(user = self.sender)
        return who
    
    def recipientProfile(self):
        try:
            who = Bossprofile.objects.get(user = self.recipient)
        except Bossprofile.DoesNotExist:
            who = Normalprofile.objects.get(user = self.recipient)
        return who