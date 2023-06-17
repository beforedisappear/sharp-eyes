from django.db.models.signals import post_save, pre_delete, pre_save
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from .models import MyUser
from uuslug import slugify

content = [1,3,6,7,8,9,10,16]

@receiver(pre_save, sender=MyUser)
def create_group(sender, instance, **kwargs):
   group = Group.objects.get_or_create(name="Moderators")
   if not group[1]: return

   permissions_list = Permission.objects.filter(content_type_id__in=content)
   group[0].permissions.set(permissions_list)


@receiver(post_save, sender=MyUser)
def add_group(sender, instance, **kwargs):
   group = Group.objects.get(name="Moderators")
   group_user = group.user_set.all()
   if instance in group_user: 
      return

   if instance.is_staff and not instance.is_superuser:
      try:
         instance.groups.add(group)
      except Group.DoesNotExist:
        pass
      
@receiver(post_save, sender=MyUser)
def update_user_slug(sender, instance, **kwargs):
   # You now have both access to self.id
   if not instance.is_superuser: 
      #now have both access to self.id
      instance.userslug = str(instance.id) + '-' + slugify(instance.username.lower().replace(' ', '-'))
      MyUser.objects.filter(id=instance.id).update(userslug=instance.userslug)