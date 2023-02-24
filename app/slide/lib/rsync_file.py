import os
import re
from glob import glob
from celery import shared_task
from subprocess import Popen, PIPE
from django.conf import settings

from app.slide.models import Slide
from app.slide.models import SlideLoadingState


SRC_PATH = settings.RSYNC_SRC_PATH
DST_PATH = settings.RSYNC_DST_PATH
SMB_URL = settings.SMB_URL

states = {
    'QUEUED': 0,
    'LOADING': 1,
    'READY': 2,
    'ERROR': 3,
}


def execute(svs_loading_state, command):
    state = 'LOADING'
    set_svs_loading_state(svs_loading_state, state=state)

    p = Popen(command, stdout=PIPE, stderr=PIPE,
              shell=True, universal_newlines=True)

    for stdout_line in iter(p.stdout.readline, ""):
        yield stdout_line

    p.stdout.close()
    return_code = p.wait()

    if return_code:
        error = p.stderr.read()
        state = 'ERROR'

        set_svs_loading_state(svs_loading_state, state=state, error=error)


def set_svs_loading_state(svs_loading_state, state=None, error=None, percentage=None):
    if state:
        svs_loading_state.state = states.get(state)
    if error:
        svs_loading_state.error = error
    if percentage:
        svs_loading_state.percentage = percentage

    svs_loading_state.save()


def get_dst_path(slide_name, organization_code):
    #base_path = glob(DST_PATH)[0]
    base_path = DST_PATH
    dst_path = os.path.join(base_path, organization_code, slide_name)

    return dst_path


def get_src_path(source_slide_name):
    globbed_src_path = glob(f'{SRC_PATH}/*/{source_slide_name}')[0]
    src_path = re.escape(globbed_src_path)

    return src_path


def mkdir_if_not_exists(dst_path):
    if not os.path.exists(dst_path):
        try:
            os.mkdir(dst_path)

        except FileExistsError:
            return None

        except Exception as error:
            return error

    return None


@shared_task
def rsync_file(svs_loading_state_id, slide_id):
    svs_loading_state = SlideLoadingState.objects.get(id=svs_loading_state_id)
    slide = Slide.objects.get(slide_id=slide_id)

    source_slide_name = slide.source_slide_name
    slide_name = slide.slide_name
    organization_code = slide.series.research.organization.code

    dst_path = get_dst_path(slide_name, organization_code)
    src_path = get_src_path(source_slide_name)

    command = f'rsync -P {src_path} {dst_path}'
    percentage = 0

    create_dir_error = mkdir_if_not_exists(
        dst_path.rstrip(slide_name.split('/')[1]))

    if create_dir_error:
        state = 'ERROR'
        set_svs_loading_state(
            svs_loading_state, state=state, error=create_dir_error)

        return

    for line in execute(svs_loading_state, command):
        if len(line.split()) > 1:
            estimated_percentage = line.split()[1]

            if '%' in estimated_percentage:
                percentage = int(estimated_percentage.rstrip('%'))
                set_svs_loading_state(
                    svs_loading_state, percentage=percentage)

            if percentage == 100:
                slide.smb_path = os.path.join(
                    SMB_URL, organization_code, slide_name)
                slide.path = os.path.join(
                    DST_PATH, organization_code, slide_name)
                slide.slide_name = slide_name.split('/')[1]

                slide.save()

                state = 'READY'
                set_svs_loading_state(svs_loading_state, state=state)
