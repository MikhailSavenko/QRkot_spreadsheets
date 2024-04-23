from sqlalchemy import func, select

from app.core.db import AsyncSession
from app.models import CharityProject

from .base import CRUDBase


class CRUDProject(CRUDBase):

    async def get_project_id_by_name(
        self, project_name: str, session: AsyncSession
    ):
        obj_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        obj_id = obj_id.scalars().first()
        return obj_id

    async def get_check_full_amount(
        self, project_id: int, new_full_amount: int, session: AsyncSession
    ):
        obj_invested_amount = await session.execute(
            select(CharityProject.invested_amount).where(
                CharityProject.id == project_id
            )
        )
        obj_invested_amount = obj_invested_amount.scalars().first()
        return new_full_amount >= obj_invested_amount

    async def get_projects_by_completion_rate(
        self, session: AsyncSession
    ) -> list[CharityProject]:
        go = (
            select(CharityProject)
            .where(CharityProject.fully_invested == 1)
            .order_by(
                func.extract('day', CharityProject.close_date)
                - func.extract('day', CharityProject.create_date), # noqa
                func.extract('hour', CharityProject.close_date)
                - func.extract('hour', CharityProject.create_date), # noqa
                func.extract('minute', CharityProject.close_date)
                - func.extract('minute', CharityProject.create_date), # noqa
            )
        )
        projects = await session.execute(go)
        projects = projects.scalars().all()
        return projects


project_crud = CRUDProject(CharityProject)
