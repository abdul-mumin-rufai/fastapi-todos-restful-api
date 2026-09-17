from fastapi import APIRouter

router = APIRouter()


#  this includes the auth file as a router to connect the auth to the main port

@router.get('/auth/')
async def get_auth():
    return {'auth': 'authenticated user'}
