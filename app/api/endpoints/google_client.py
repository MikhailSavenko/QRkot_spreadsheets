from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends

from app.core.db import AsyncSession, get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.schemas.charity_project import ProgectReportGoogleDB
from app.services.google_api import (set_user_permissions, spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()


@router.get(
    '/',
    response_model=list[ProgectReportGoogleDB],
    dependencies=[Depends(current_superuser)],
)
async def get_report_google_tables(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    projects = await project_crud.get_projects_by_completion_rate(
        session=session
    )
    spreadsheetid = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    projects_report = await spreadsheets_update_value(
        spreadsheetid, projects, wrapper_services
    )
    return projects_report
