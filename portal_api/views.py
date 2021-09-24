from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query

import portal_api.schemas
from portal_api import filters, schemas
from portal_api.di import Container

router = APIRouter()


@router.get('/api/properties/zap', response_model=schemas.Pagination)
@inject
async def load_properties_zap(
        portal=Depends(Provide[Container.zap_portal]),
        filters_query: portal_api.schemas.Filter = Depends(),
        page_number: int = Query(1, alias='pageNumber'),
        page_size: int = Query(10, alias='pageSize')
):
    items, total = portal.load_filters(filters.filters_factory(filters_query), page_number, page_size)
    return dict(page_number=page_number, page_size=page_size, total_count=total, listings=items)


@router.get('/api/properties/viva-real', response_model=schemas.Pagination)
@inject
async def load_properties_viva_real(
        portal=Depends(Provide[Container.viva_real_portal]),
        filters_query: portal_api.schemas.Filter = Depends(),
        page_number: int = Query(1, alias='pageNumber'),
        page_size: int = Query(10, alias='pageSize')
):
    items, total = portal.load_filters(filters.filters_factory(filters_query), page_number, page_size)
    return dict(page_number=page_number, page_size=page_size, total_count=total, listings=items)
