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


class SerpapiSearch:
    def __init__(self, query):
        self.query = query
        self.result = None

    def get_result(self, text_or_image):
        engine_type = ""
        if text_or_image == "text":
            engine_type = "google"
        elif text_or_image == "image":
            engine_type = "google_images"
        result = client.search(
            q=self.query,
            engine=engine_type,
            hl='en',
            gl='us'
        )
        self.result = result

    def format_result(self, text_or_image):
        formatted_result = {}
        if text_or_image == "text":
            for item in self.result['organic_results']:
                formatted_result[item['title']] = ["Link: " + item['link'], "Snippet: " + item['snippet']]
        elif text_or_image == 'image':
            for item in self.result['images_results']:
                formatted_result[item['title']] = ["Link: " + item['link'], "Image: " + item['original']]
        return formatted_result


@router.get("/")
async def search(query: str):
    search_object = SerpapiSearch(query)
    search_object.get_result("text")
    formatted_result = search_object.format_result("text")
    return {"result": formatted_result}


@router.get("/image")
async def search_image(query: str):
    search_image_object = SerpapiSearch(query)
    search_image_object.get_result("image")
    formatted_result = search_image_object.format_result("image")
    return {"result": formatted_result}


