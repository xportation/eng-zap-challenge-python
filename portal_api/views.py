from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from portal_api.di import Container

router = APIRouter()


@router.get('/api/properties/zap')
@inject
async def load_properties_zap(portal=Depends(Provide[Container.zap_portal])):
    return portal.load_filters([])


@router.get('/api/properties/viva-real')
@inject
async def load_properties_viva_real(portal=Depends(Provide[Container.viva_real_portal])):
    return portal.load_filters([])
