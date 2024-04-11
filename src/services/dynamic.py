import json
from typing import Annotated
from uuid import UUID
from datetime import datetime
from pydantic import create_model, BaseModel, ValidationError, Field
from typing import Type
from models import DependenciesOrm
from utils.absract.service import BaseService
from logging import getLogger

logger = getLogger(__name__)

class Camerus:
    @classmethod
    def parse_camerus1(cls, data: dict) -> tuple:
        numbers = data.get("transport_numbers")
        return (
            f"{numbers[0]}{data.get('transport_chars')}{numbers[1:]}{data.get('transport_region')}",
            data.get("camera_id"),
            data.get("violation_id"),
            data.get("violation_value"),
            data.get('skill_value'),
            data.get('datetime')
        )  

    @classmethod
    def parse_camerus2(cls, data: dict) -> tuple:
        transport:dict = data.get("transport")
        numbers = transport.get("numbers")
        camera:dict = data.get('camera')
        violation: dict = data.get('violation')
        skill: dict = data.get('skill')
        return (
            f"{numbers[0]}{transport.get('chars')}{numbers[1:]}{data.get('region')}",
            camera.get("id"),
            violation.get('id'),
            violation.get('value'),
            skill.get('value'),
            datetime(**data.get('datetime'))
        )
    
    @classmethod
    def parse_camerus3(cls, data: dict) -> tuple:
        camera:dict = data.get('camera')
        violation: dict = data.get('violation')
        return (
            data.get('transport'),
            camera.get("id"),
            violation.get('id'),
            violation.get('value'),
            data.get('skill'),
            datetime.fromtimestamp(float(data.get('datetime')), tz=None)
        )

class CamerusService(BaseService):
    extraTypes = {
        "UUID": UUID,
        "datetime": datetime,
    }
    extraTypes.update(__builtins__)

    camerus_list: list[Type[BaseModel]] = []
    camerus_pattern_list: list[str] = []


    def get_builtin(self, name: str):
        return self.extraTypes.get(name)
    

    async def create(self, name: str, data: list[DependenciesOrm]):
        kwargs = {}
        for dependency in data:
            val_type = self.get_builtin(dependency.value_type)
            field_attrs = {
                "validate_default": True
            }
            if val_type is dict:
                async with self.uow:
                    val_type = await self.create(dependency.key, await self.uow.camerus.construct(dependency.id))
            field_attrs.update(dependency.field_attrs)
            kwargs.update({dependency.key: (Annotated[val_type, Field(**field_attrs)], None)})
        setattr(self, name, new_model:=create_model(name, __base__=BaseModel, **kwargs))
        return new_model


    async def generate(self):
        async with self.uow:
            root_list: tuple[UUID] = await self.uow.camerus.collect()
        for root in root_list:
            async with self.uow:
                key = (await self.uow.camerus.find_by_id(root)).key
                data = await self.uow.camerus.construct(root)
                await self.uow.commit()
            self.__class__.camerus_list.append(
                await self.create(
                    key,
                    data
                )
            )
        await self.set_pattern()
            
    @classmethod
    async def set_pattern(cls) -> None:
        cls.camerus_pattern_list = [cam_type.__name__ for cam_type in cls.camerus_list]


    async def validate(self, data:dict) -> Type[BaseModel] | dict[str, ValidationError]:
        exceptions: dict[str, ValidationError] = {}
        for camerus in self.camerus_list:
            try:
                model = camerus.model_validate_json(json.dumps(data))
                return model, camerus.__name__
            except ValidationError as e:
                exceptions.update({camerus.__name__: e.errors()})
        else:
            return exceptions, "error"


    async def parse(self, model: Type[BaseModel], model_name: str) -> dict:
        values = getattr(Camerus, f"parse_{model_name}")(model.model_dump())
        keys = (
            "transport",
            "camera_id",
            "violation_id",
            "violation_value",
            'skill_value',
            'case_timestamp'
        )
        return {
            key:value 
            for 
                key, value
            in 
                zip(keys, values)
        }
