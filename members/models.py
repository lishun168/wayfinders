from django.db import models
from django.conf import settings
from search.models import SearchObject
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now

class Member(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to="profile_gallery", blank=True)
    public = models.BooleanField(default=True)
    logo = models.ImageField(upload_to="group_logo", blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    business_phone = PhoneNumberField(region="CA")
    address = models.CharField(max_length=255, null=True, blank=True)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    membership_expiry = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    membership_since = models.DateField(auto_now_add=False, blank=True, null=True) 
    business_email = models.EmailField(max_length=255)
    number_of_flags = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name='Member'
        verbose_name_plural='Members'

class MemberUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    primary_member = models.ForeignKey(Member, on_delete=models.CASCADE)
    search_tag = models.ForeignKey(SearchObject, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    is_forum_mod = models.BooleanField(default=False)
    is_wf_admin = models.BooleanField(default=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    address_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    province = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    business_phone = PhoneNumberField(region="CA")
    home_phone = PhoneNumberField(region="CA")
    cell_phone = PhoneNumberField(region="CA")
    publicly_viewable = models.BooleanField(u'Public', default=True)
    membership_since = models.DateField(auto_now_add=False, blank=True, null=True)
    main_image = models.ImageField(upload_to="profile_gallery", blank=True)
    number_of_flags = models.IntegerField(default=0)


    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name='Member User'
        verbose_name_plural='Member Users'

class UserToMember(models.Model):
    member_user = models.ForeignKey(MemberUser, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    is_owner = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s' % (self.member_user, self.member)

    class Meta:
        unique_together=("member_user", "member")
        verbose_name="Member To User Relationship"
        verbose_name_plural="Member to User Relationships"

class Permissions(models.Model):
    role_title = models.CharField(max_length=255)
    is_member_admin = models.BooleanField(default=False)
    can_add_calendar_events = models.BooleanField(default=False)
    can_edit_company_profile = models.BooleanField(default=False)
    can_add_employees = models.BooleanField(default=False)
    can_delete_posts = models.BooleanField(default=False)
    can_edit_own_profile = models.BooleanField(default=True)
    can_add_skills = models.BooleanField(default=False)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.role_title)

    class Meta:
        verbose_name='Permission'
        verbose_name_plural='Permissions'

class UserRole(models.Model):
    user = models.ForeignKey(MemberUser, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    permissions = models.ForeignKey(Permissions, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.user, self.permissions)

    class Meta:
        unique_together=("user", "member")
        verbose_name="User Role"
        verbose_name_plural="User Roles"

class Gallery(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='members/static/members/gallery/')

    def __str__(self):
        return '%s: %s' % (self.member, self.image)

    class Meta:
        verbose_name="Gallery"
        verbose_name_plural="Galleries"

class Application(models.Model):
    surname = models.CharField(u'Last Name(*)', max_length=255)
    first_name = models.CharField(u'First Name(*)', max_length=255)
    email = models.CharField(u'Email(*)', max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_website = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(u'City/Town', max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)
    birthdate = models.CharField(max_length=255, blank=True, null=True)
    phone_number = PhoneNumberField(u'Phone Number(*)', region="CA")
    referred_by = models.CharField(max_length=255, blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    date = models.DateField(default=now)
    processed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return '%s: %s' % (self.business_name, self.surname)

    class Meta:
        verbose_name="Application"
        verbose_name_plural="Applications"

class ApplicationUpload(models.Model):
    file = models.FileField(upload_to="application_file")
    date = models.DateField(default=now)
    processed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.file)

    class Meta:
        verbose_name="Application Upload"
        verbose_name_plural="Application Uploads"

class UserFlagUser(models.Model):
    user = models.ForeignKey(MemberUser, on_delete=models.CASCADE)
    flagged_user = models.ForeignKey(MemberUser, on_delete=models.CASCADE, related_name="flagged_user")
    flagged = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s : %s' % (self.flagged_user, self.user, self.flagged)

class UserFlagMember(models.Model):
    user = models.ForeignKey(MemberUser, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s : %s' % (self.member, self.user, self.flagged)