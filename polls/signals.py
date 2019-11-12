@receiver(post_save, sender=User, dispatch_uid='save_new_user_usuario')
def save_usuario(sender, instance, created, **kwargs):
    user = instance
    if created:
        usuario = Usuario(user=user)
        usuario.save()