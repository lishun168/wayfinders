from django.db import models
from members.models import MemberUser, Member

# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    official = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.name)

class MemberToSkills(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.member, self.skill)

    class Meta:
        verbose_name="Member Skill Relationship"
        verbose_name_plural="Member Skill Relationships"

class UserToSkills(models.Model):
    user = models.ForeignKey(MemberUser, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.user, self.skill)

    class Meta:
        verbose_name="User Skill Relationship"
        verbose_name_plural="User Skill Relationships"
        
