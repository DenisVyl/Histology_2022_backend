import json
from django.contrib.auth.models import User
from app.icd_10.models import Icd_10
from app.icd_03.models import Icd_03
from app.research.models import Research
from app.series.models import Series
from app.slide.models import Slide
from app.organization.models import Organization
from app.employee.models import Employee
from app.scanning.models import Scanning
from app.histological_scanners.models import HistologicalScanners

YEAR_MIN, YEAR_MAX = 1990, 2022


def check_data(data, user):
    res = {'exist': [], 'duplicates': [], 'incorrect_data': [],
           'wrong_icd_10': [], 'wrong_icd_03': [], 'wrong_year': [], 'wrong_org': [], 'user_unemployed': [],
           'wrong_scanning': [], 'wrong_histological_scanner': []}

    user_employed = Employee.objects.select_related(
        'user').filter(user=user).exists()
    if not user_employed:
        res['user_unemployed'].append(user.username)

    unique_research_values, unique_series_values, unique_slide_values = set(), set(), set()

    for line in data:
        line_type = line.get('type')

        try:
            wrong_icd_10, wrong_icd_03 = False, False
            if line_type == 'research':
                organization = line.get('organization')
                base_code = line.get('base_code')
                year = line.get('year')

                unique_research_value = f'{base_code}-{organization}-{year}'

                org_correct = Organization.objects.filter(
                    code=organization).exists()
                if not org_correct:
                    res['wrong_org'].append(line)

                if unique_research_value in unique_research_values:
                    res['duplicates'].append(line)
                else:
                    unique_research_values.add(unique_research_value)
                exists = Research.objects.select_related('organization').filter(
                    base_code=base_code, year=year, organization__code=organization).exists()

                if line.get('year') is None or (
                    not isinstance(year, int) or (
                        isinstance(year, int) and (
                            year < YEAR_MIN or year > YEAR_MAX
                        )
                    )
                ):
                    res['wrong_year'].append(line)

            elif line_type == 'series':
                main_code = line.get('main_code')
                base_code = line.get('base_code')
                icd_10_code = line.get('Icd_10_code')
                icd_03_code = line.get('Icd_03_code')
                exists = False

                #research = Research.objects.filter(base_code=base_code).first()

                #unique_series_value = f'{research}-{base_code}-{main_code}'

                # if unique_series_value in unique_series_values:
                #    res['duplicates'].append(line)
                # else:
                #    unique_series_values.add(unique_series_value)

                if icd_10_code is None or not Icd_10.objects.filter(code=icd_10_code).exists():
                    wrong_icd_10 = True
                if icd_03_code is not None and not Icd_03.objects.filter(code=icd_03_code).exists():
                    wrong_icd_03 = True

            elif line_type == 'slide':
                main_code = line.get('main_code')
                base_code = line.get('base_code')
                slide_name = line.get('slide_name')
                icd_10_code = line.get('Icd_10_code')
                icd_03_code = line.get('Icd_03_code')
                scanning = line.get('scanning')
                histological_scanner = line.get('histological_scanner')

                unique_slide_value = f'{slide_name}-{base_code}-{main_code}-{histological_scanner}-{scanning}'

                if unique_slide_value in unique_slide_values:
                    res['duplicates'].append(line)
                else:
                    unique_slide_values.add(unique_slide_value)
                exists = Slide.objects.select_related('histological_scanner', 'scanning').filter(
                    source_slide_name=slide_name, histological_scanner__code=histological_scanner, scanning__value=scanning).exists()

                if icd_10_code is not None and not Icd_10.objects.filter(code=icd_10_code).exists():
                    wrong_icd_10 = True
                if icd_03_code is not None and not Icd_03.objects.filter(code=icd_03_code).exists():
                    wrong_icd_03 = True

                scanning_exists = Scanning.objects.filter(
                    value=scanning).exists()
                histological_scanner_exists = HistologicalScanners.objects.filter(
                    code=histological_scanner).exists()
                if not scanning_exists:
                    res['wrong_scanning'].append(line)
                if not histological_scanner_exists:
                    res['wrong_histological_scanner'].append(line)
            else:
                res['incorrect_data'].append((line, 'incorrect type'))

            if exists:
                res['exist'].append(line)
            if wrong_icd_10:
                res['wrong_icd_10'].append(line)
            if wrong_icd_03:
                res['wrong_icd_03'].append(line)
        except Exception as e:
            res['incorrect_data'].append((line, f'Exception: {str(e)}'))

    json_response = json.dumps(res)
    return json_response
