import json
from app.icd_10.models import Icd_10
from prj.settings import BASE_DIR
ICD_10_UPDATED_FILE = f'{BASE_DIR}/app/icd_10_updated_2022_03_22.json'


def get_new_icd():
    with open(ICD_10_UPDATED_FILE, 'r') as updated:
        data_updated = json.load(updated)
    return data_updated


def run():
    new_icd = get_new_icd()

    for key in list(new_icd.keys()):
        code = key
        diagnosis = new_icd[key][0]
        parent = new_icd[key][1]

        icd_10_obj = Icd_10.objects.filter(code=code).first()

        if not icd_10_obj:
            icd_10_obj = Icd_10.objects.create(
                code=code, diagnosis=diagnosis, parent=parent)
            icd_10_obj.save()

        else:
            icd_10_obj.diagnosis = diagnosis
            icd_10_obj.parent = parent
            icd_10_obj.save()
