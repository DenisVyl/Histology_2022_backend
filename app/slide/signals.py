import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Slide, SlideLoadingState
from .lib.rsync_file import rsync_file


@receiver(post_save, sender=Slide)
def rsync_svs_files(
        sender, instance, created, *args, **kwargs
):
    if created:
        svs_loading_state = SlideLoadingState(slide=instance)
        svs_loading_state.save()

        svs_loading_state_id = svs_loading_state.id
        slide_id = instance.slide_id

        rsync_file.delay(svs_loading_state_id, slide_id)


@receiver(post_delete, sender=Slide)
def remove_svs_file(sender, instance, *args, **kwargs):
    file_path = instance.path

    if not file_path:
        return 

    dir_path = os.path.dirname(file_path)

    if os.path.exists(file_path):
        os.remove(file_path)

    if os.path.exists(dir_path) and not os.listdir(dir_path):
        os.rmdir(dir_path)
