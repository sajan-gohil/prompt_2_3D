from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
import uuid
import os
import time
import threading
from generate_mesh import generate_shapes

app = FastAPI()
startup_time = time.time()
version = "1.0.0"

output_root = "outputs"

@app.get("/generate3d")
def generate_3d(prompt: str = Query(...)):
    job_id = str(uuid.uuid4())[:8]
    output_dir = os.path.join(output_root, job_id)
    os.makedirs(output_dir, exist_ok=True)

    # Run generation in background thread
    generate_shapes([prompt], output_dir=output_dir)

    obj_path = os.path.join(output_dir, "mesh_0.obj")
    if os.path.exists(obj_path):
        return FileResponse(obj_path, media_type="text/plain", filename=f"{job_id}.obj")
    else:
        return JSONResponse(status_code=500, content={"error": "Generation failed."})

@app.get("/status")
def status():
    uptime = time.time() - startup_time
    return {
        "status": "ok",
        "uptime_seconds": int(uptime),
        "version": version,
    }
