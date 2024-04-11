from uuid import UUID

from schemas.cameras import SCameraRegist
from utils.absract.service import BaseService

class CameraService(BaseService):
    async def regist(
        self,
        camera_schema: SCameraRegist
    ) -> UUID:
        camera_data = camera_schema.model_dump()
        camera_data.update(camera_data.pop("GPScoords"))
        async with self.uow:
            camera_data.update({
                "cam_type": await self.uow.camerus.find_by_path(
                    camera_data.pop("CameraType")
                )
            })  
            result = await self.uow.cameras.add_one(camera_data)
            await self.uow.commit()
        return result
