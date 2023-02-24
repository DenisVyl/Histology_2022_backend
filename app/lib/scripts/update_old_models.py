import json

FILE = '***/dump.json'


def read_file():
    with open(FILE, 'r') as f:
        data = json.load(f)

    return data


def update_organizations(data):
    organizations = filter(
        lambda org: org['model'] == 'app.organization', data)
    organizations_list = list(organizations)
    for index, org in enumerate(organizations_list):
        org['fields']['name'] = org['pk']
        org['pk'] = index

    with open('organizations.json', 'w', encoding='utf-8') as f:
        json.dump(organizations_list, f, ensure_ascii=False, indent=4)

    return organizations_list


def update_research(data, organizations_list):
    research = filter(lambda org: org['model'] == 'app.research', data)
    research_list = list(research)

    for research in research_list:
        org_name = research['fields']['organization']
        org = list(
            filter(lambda org: org['fields']['name'] == org_name, organizations_list))[0]
        research['fields']['organization'] = org['pk']

    with open('research.json', 'w', encoding='utf-8') as f:
        json.dump(research_list, f, ensure_ascii=False, indent=4)

    return research_list


def update_positions(data):
    positions = filter(lambda org: org['model'] == 'app.position', data)
    positions_list = list(positions)

    for index, position in enumerate(positions_list):
        position['fields']['name'] = position['pk']
        position['pk'] = index

    with open('positions.json', 'w', encoding='utf-8') as f:
        json.dump(positions_list, f, ensure_ascii=False, indent=4)

    return positions_list


def update_roles(data):
    roles = filter(lambda org: org['model'] == 'app.role', data)
    roles_list = list(roles)

    for index, role in enumerate(roles_list):
        role['fields']['name'] = role['pk']
        role['pk'] = index

    with open('roles.json', 'w', encoding='utf-8') as f:
        json.dump(roles_list, f, ensure_ascii=False, indent=4)

    return roles_list


def update_icd(data):
    icds = filter(lambda org: org['model'] == 'app.icd_10', data)
    icds_list = list(icds)

    for index, icd in enumerate(icds_list):
        icd['fields']['code'] = icd['pk']
        icd['pk'] = index

    with open('icds.json', 'w', encoding='utf-8') as f:
        json.dump(icds_list, f, ensure_ascii=False, indent=4)

    return icds_list


def update_employees(data, organizations_list, positions_list, roles_list):
    employees = filter(lambda emp: emp['model'] == 'app.employee', data)
    employees_list = list(employees)

    for employee in employees_list:
        # user
        employee['fields']['user'] = employee['pk']

        # organizations
        org_name = employee['fields']['organization']
        if org_name:
            org = list(
                filter(lambda org: org['fields']['name'] == org_name, organizations_list))[0]
            employee['fields']['organization'] = org['pk']

        # positions
        pos_name = employee['fields']['position']
        if pos_name:
            pos = list(
                filter(lambda pos: pos['fields']['name'] == pos_name, positions_list))[0]
            employee['fields']['position'] = pos['pk']

        # roles
        role_name = employee['fields']['role']
        if role_name:
            role = list(
                filter(lambda role: role['fields']['name'] == role_name, roles_list))[0]
            employee['fields']['role'] = role['pk']

    with open('employees.json', 'w', encoding='utf-8') as f:
        json.dump(employees_list, f, ensure_ascii=False, indent=4)

    return employees_list


def update_slides(data, icds_list):
    slide = filter(lambda org: org['model'] == 'app.slide', data)
    slide_list = list(slide)

    for slide in slide_list:
        icd_code = slide['fields']['Icd_10_code']
        if icd_code:
            icd = list(
                filter(lambda org: icd['fields']['code'] == icd_code, icds_list))[0]
            slide['fields']['Icd_10_code'] = icd['pk']

    with open('slide.json', 'w', encoding='utf-8') as f:
        json.dump(slide_list, f, ensure_ascii=False, indent=4)

    return slide_list


def update_series(data, icds_list):
    series = filter(lambda org: org['model'] == 'app.series', data)
    series_list = list(series)

    for series in series_list:
        icd_code = series['fields']['Icd_10_code']
        if icd_code:
            icd = list(
                filter(lambda icd: icd['fields']['code'] == icd_code, icds_list))[0]
            series['fields']['Icd_10_code'] = icd['pk']

    with open('series.json', 'w', encoding='utf-8') as f:
        json.dump(series_list, f, ensure_ascii=False, indent=4)

    return series_list


def run():
    data = read_file()
    organizations_list = update_organizations(data)
    positions_list = update_positions(data)
    roles_list = update_roles(data)
    icds_list = update_icd(data)

    employees_list = update_employees(
        data, organizations_list, positions_list, roles_list)
    update_research(data, organizations_list)

    update_slides(data, icds_list)
    update_series(data, icds_list)


if __name__ == '__main__':
    run()
