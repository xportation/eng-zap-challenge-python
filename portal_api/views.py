from fastapi import APIRouter

router = APIRouter()


@router.get('/api/properties')
async def load_properties():
    return {}
