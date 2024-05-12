from typing import Annotated, ClassVar, Optional
from uuid import UUID
from fastapi import HTTPException
from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field, validator

from models.roles import RoleORM
from models.structures import StructureORM

class BaseStructFilter(Filter):
    class Constants(Filter.Constants):
        model = StructureORM
    class Config:
        populate_by_name = True

class OrganizationFilter(BaseStructFilter):
    name__in: Annotated[list[str], Field(alias="org_names")] = None
    org_id__isnull: ClassVar[bool] = True

class StructureFilter(BaseStructFilter):
    name__in: Annotated[list[str], Field(alias="struct_names")] = None
    org: Optional[OrganizationFilter] = FilterDepends(with_prefix("org", OrganizationFilter))


# class VancedStructFilter(StructureFilter):
#     name__not_in: Annotated[list[str], Field(alias="except_names")]
#     head__name__in: Annotated[Optional[list[str]], Field(alias="head_names")] = None
#     custom_order_by: Annotated[list[str], Field(alias="order_by")]
    
#     class Constants(BaseStructFilter.Constants):
#         ordering_field_name = "custom_order_by"
#         search_field_name = "custom_search"
#         search_model_fields = ["name", "country", "city"]
