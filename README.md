# prompt_2_3D
prompt_2_3d is a small project that generates 3D object meshes (.obj or similar) files using text to 3d models. Currently, OpenAI shape-E model is used.

# Dependencies

`pip install -r requirements.txt`


# Usage

Run api server:
`uvicorn api:app --host 0.0.0.0 --port 8000`

Endpoints:

1. `/generate3d`

Example (cURL): `curl "http://127.0.0.1:8000/generate3d?prompt=a%20robotic%20spider" --output spider.obj`

