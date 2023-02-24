import json
from dateutil import parser
from django.conf import settings

from app.research.models import Research
from app.series.models import Series
from app.slide.models import Slide
from app.organization.models import Organization
from app.icd_10.models import Icd_10
from app.icd_03.models import Icd_03
from app.employee.models import Employee
from app.scanning.models import Scanning
from app.histological_scanners.models import HistologicalScanners

from .filenames_encrypt import filename_encrypt


BASE_CODE_STR = 'base_code'
SRC_PATH = settings.RSYNC_SRC_PATH


def stringify_code_values(data):
    for item in data:
        if item.get('base_code'):
            item['base_code'] = str(item['base_code'])

        if item.get('main_code'):
            item['main_code'] = str(item['main_code'])


def sort_data(data):
    researchs = []
    series = []
    slides = []
    sorted_data = []

    for obj in data:
        if obj.get('type') == 'research':
            researchs.append(obj)
        if obj.get('type') == 'series':
            series.append(obj)
        if obj.get('type') == 'slide':
            slides.append(obj)

    for research in researchs:
        base_code = research.get(BASE_CODE_STR)
        filtered_series = list(
            filter(lambda series_obj: series_obj.get(BASE_CODE_STR) == base_code, series))
        filtered_slides = list(
            filter(lambda slide: slide.get(BASE_CODE_STR) == base_code, slides))

        sorted_elem = {
            'research': research,
            'series': filtered_series,
            'slides': filtered_slides
        }

        sorted_data.append(sorted_elem)

    return sorted_data


def check_object_exists(obj, filter_fields):
    model = type(obj)
    filter_request = {}

    for filter_field in filter_fields:
        object_value = getattr(obj, filter_field)

        filter_request[filter_field] = object_value

    object_exists = model.objects.filter(**filter_request).exists()

    return object_exists


def save_obj(obj):
    obj.save()


def upload_data(data, user):
    stringify_code_values(data)
    sorted_data = sort_data(data)
    is_upload_data_successful = True
    errors = {
        'research': [],
        'series': [],
        'slides': []
    }

    for item in sorted_data:
        research = item['research']
        series = item['series']
        slides = item['slides']

        research_obj = create_research_obj(research, user)
        research_filter_fields = ('base_code', 'year', 'organization')

        series_objs = create_series_objs(series, research_obj)
        series_filter_fields = ('research', 'main_code')

        slides_objs = create_slides_objs(slides, series_objs)
        slides_filter_fields = ('series', 'index_number',
                                'histological_scanner', 'scanning')

        is_research_object_exists = check_object_exists(
            research_obj, filter_fields=research_filter_fields)
        if is_research_object_exists:
            errors['research'].append(
                f"{research_obj.base_code} research already exists")

        for obj in series_objs:
            is_object_exists = check_object_exists(
                obj, filter_fields=series_filter_fields)
            if is_object_exists:
                series_obj_main_code = getattr(obj, 'main_code')
                errors['series'].append(
                    f"{series_obj_main_code} series already exists")

        for obj in slides_objs:
            is_object_exists = check_object_exists(
                obj, filter_fields=slides_filter_fields)
            if is_object_exists:
                slide_obj_name = getattr(obj, 'source_slide_name')
                errors['slides'].append(
                    f"{slide_obj_name} slide already exists")

        if len(errors['research']) or len(errors['series']) or len(errors['slides']):
            is_upload_data_successful = False
        else:
            list(map(save_obj, (research_obj, *series_objs, *slides_objs)))

    if len(errors['research']) or len(errors['series']) or len(errors['slides']):
        errors = json.dumps(errors)

    return (is_upload_data_successful, errors)


def create_research_obj(research, user):
    year = research.get('year')
    base_code = research.get('base_code')
    organization = research.get('organization')
    macroscopic_description = research.get('macroscopic_description')
    microscopic_description = research.get('microscopic_description')
    receipt_employee_str = research.get("receipt_employee")
    return_employee_str = research.get("return_employee")
    receipt_date = research.get('receipt_date')
    return_date = research.get('return_date')

    receipt_employee = Employee.objects.select_related(
        'user').get(user__username=receipt_employee_str)
    return_employee = Employee.objects.select_related(
        'user').get(user__username=return_employee_str)

    org = Organization.objects.get(code=organization)
    operator = Employee.objects.select_related(
        'user').get(user=user)

    research_obj = Research(
        year=year,
        base_code=base_code,
        macroscopic_description=macroscopic_description,
        microscopic_description=microscopic_description,
        organization=org,
        operator=operator,
        receipt_employee=receipt_employee,
        receipt_date=receipt_date,
        return_employee=return_employee,
        return_date=return_date
    )

    return research_obj


def create_series_objs(series, research):
    series_objs = []

    for ser in series:
        main_code = ser.get('main_code')
        number_of_slides = ser.get('slides_per_series')
        icd_10_code = ser.get('Icd_10_code')
        icd_03_code = ser.get('Icd_03_code')
        histological_diagnosis = ser.get('histological_diagnosis')
        macroscopic_description = ser.get('macroscopic_description')
        microscopic_description = ser.get('microscopic_description')

        icd_10_code_obj = Icd_10.objects.get(code=icd_10_code)
        icd_03_code_obj = Icd_03.objects.filter(code=icd_03_code).first()

        series_obj = Series(
            research=research,
            main_code=main_code,
            number_of_slides=number_of_slides,
            Icd_10_code=icd_10_code_obj,
            Icd_03_code=icd_03_code_obj,
            histological_diagnosis=histological_diagnosis,
            macroscopic_description=macroscopic_description,
            microscopic_description=microscopic_description,
        )

        series_objs.append(series_obj)

    return series_objs


def create_slides_objs(slides, series_objs):
    slides_objs = []

    for slide in slides:
        source_slide_name = slide.get('slide_name')
        slide_name = source_slide_name.split(
            '/')[0] + '/' + filename_encrypt(source_slide_name.split('/')[1])
        main_code = slide.get('main_code')
        additional_code = slide.get('additional_code')
        scanning = slide.get('scanning')
        histological_scanner_code = slide.get('histological_scanner')
        focus = slide.get('focus')
        icd_10_code = slide.get('Icd_10_code')
        icd_03_code = slide.get('Icd_03_code')

        scanning_obj = Scanning.objects.get(value=scanning)
        histological_scanner = HistologicalScanners.objects.get(
            code=histological_scanner_code)

        index_number_str = source_slide_name.split(
            '/')[1].split('#')[1].split('_')[1]
        index_number = int(index_number_str)

        series_obj = list(
            filter(lambda series_obj: series_obj.main_code == main_code, series_objs))[0]

        icd_10_code_obj = Icd_10.objects.get(
            code=icd_10_code) if icd_10_code else series_obj.Icd_10_code
        icd_03_code_obj = Icd_03.objects.filter(
            code=icd_03_code).first() if icd_03_code else series_obj.Icd_03_code

        slide_obj = Slide(
            series=series_obj,
            slide_name=slide_name,
            source_slide_name=source_slide_name,
            Icd_10_code=icd_10_code_obj,
            Icd_03_code=icd_03_code_obj,
            additional_code=additional_code,
            index_number=index_number,
            scanning=scanning_obj,
            histological_scanner=histological_scanner,
            focus=focus
        )

        slides_objs.append(slide_obj)

    return slides_objs
