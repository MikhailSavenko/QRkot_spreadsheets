from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = {
        'properties': {
            'title': f'Отчёт на {now_date_time}',
            'locale': 'ru_RU',
        },
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': 0,
                    'title': 'Лист1',
                    'gridProperties': {'rowCount': 100, 'columnCount': 11},
                }
            }
        ],
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheetid = response['spreadsheetId']
    return spreadsheetid


async def set_user_permissions(
    spreadsheetid: str, wrapper_services: Aiogoogle
) -> None:
    prmissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid, json=prmissions_body, fields='id'
        )
    )


async def spreadsheets_update_value(
    spreadsheetid: str, projects: list, wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание'],
    ]
    for prjct in projects:
        gathering_time = prjct.close_date - prjct.create_date
        new_row = [
            str(prjct.name),
            str(gathering_time),
            str(prjct.description),
        ]
        table_values.append(new_row)

    update_body = {'majorDimension': 'ROWS', 'values': table_values}
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range='A:E',
            valueInputOption='USER_ENTERED',
            json=update_body,
        )
    )
    projects_report_list = []
    projects_all = table_values[3:]
    for pro in projects_all:
        projects_report = {}
        projects_report['name'] = pro[0]
        projects_report['gathering_time'] = pro[1]
        projects_report['description'] = pro[2]
        projects_report_list.append(projects_report)

    return projects_report_list
