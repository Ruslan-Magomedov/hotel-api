from sqlalchemy import select, func

from app.repositories.base import BaseRepo
from app.models.hotels import HotelsOrm
from app.schemas.hotels import Hotels



class HotelsRepo(BaseRepo):
    model = HotelsOrm
    schema = Hotels

    async def get_all(self, title, city, limit, offset):
        obj = select(HotelsOrm)

        if city:
            obj = obj.filter(func.lower(HotelsOrm.city).like(f"%{city.lower()}%"))
            
        if title:
            obj = obj.filter(func.lower(HotelsOrm.title).like(f"%{title.lower()}%"))
        
        obj = obj.limit(limit).offset(offset)
        obj = await self.session.execute(obj)
    
        return [self.schema.model_validate(model, from_attributes=True) for model in obj.scalars().all()]
