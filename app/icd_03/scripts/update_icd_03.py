import json
from app.icd_03.models import Icd_03
from prj.settings import BASE_DIR
ICD_03_UPDATED_FILE = f'{BASE_DIR}/app/icd_03.json'


def get_new_icd():
    with open(ICD_03_UPDATED_FILE, 'r') as updated:
        data_updated = json.load(updated)
    return data_updated


def run():
    new_icd = get_new_icd()

    for key in list(new_icd.keys()):
        code = key
        diagnosis = new_icd[key][0]
        parent = new_icd[key][1]

        icd_03_obj = Icd_03.objects.filter(code=code).first()

        if not icd_03_obj:
            icd_03_obj = Icd_03.objects.create(
                code=code, diagnosis=diagnosis, parent=parent)
            icd_03_obj.save()

        else:
            icd_03_obj.diagnosis = diagnosis
            icd_03_obj.parent = parent
            icd_03_obj.save()
