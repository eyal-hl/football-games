from typing import List

from sqlalchemy import select

from models.specials import SpecialsModel
from schemas.specials import SpecialSchema
from services.base import BaseDataManager, BaseService


class SpecialService(BaseService):
    async def get_special(self, special_id: str) -> SpecialSchema:
        """Get special by ID."""
        return await SpecialDataManager(self.session).get_special(special_id)

    async def get_specials(self) -> List[SpecialSchema]:
        """Select all special."""
        return await SpecialDataManager(self.session).get_specials()


class SpecialDataManager(BaseDataManager):
    async def get_special(self, special_id: str) -> SpecialSchema:
        stmt = select(SpecialsModel).where(SpecialsModel.special_id == special_id)
        model = await self.get_one(stmt)

        return SpecialSchema(**model.to_dict())

    async def get_specials(self) -> List[SpecialSchema]:
        schemas: List[SpecialSchema] = list()

        stmt = select(SpecialsModel)

        for model in await self.get_all(stmt):
            schemas += [SpecialSchema(**model.to_dict())]

        return schemas
