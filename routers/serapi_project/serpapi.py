import os
from dotenv import load_dotenv
import serpapi
from fastapi import APIRouter

load_dotenv()
api_key = os.getenv('SERPAPI_KEY')
router = APIRouter(
    prefix="/serp",
    tags=['serp']
)

client = serpapi.Client(api_key=api_key)


@router.get("/")
async def search(query: str):
    result = client.search(
        q=query,
        engine='google',
        hl='en',
        gl='us'
    )
    formatted_result = {}
    for item in result['organic_results']:
        '''formatted_result += item['title']
        formatted_result += item['link']
        formatted_result += item['snippet']
        formatted_result += "-------------" '''
        formatted_result[item['title']] = ["Link: " + item['link'], "Snippet: " + item['snippet']]

    return {"result": formatted_result}


@router.get("/image")
async def search_image(query: str):
    result = client.search(
        q=query,
        engine='google_images',
        hl='en',
        gl='us'
    )
    formatted_result = {}
    for item in result['images_results']:
        formatted_result[item['title']] = ["Link: " + item['link'], "Image: " + item['original']]

    return {"result": formatted_result}


