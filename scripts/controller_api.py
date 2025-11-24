from fastapi import FastAPI
import uvicorn
import subprocess
import threading
import os

app = FastAPI()

def run_script_thread(script):
    import subprocess
    subprocess.Popen(["python3", "-u", f"/scripts/{script}"])

@app.post("/run-script")
def run_script(script: str):
    threading.Thread(target=run_script_thread, args=(script,)).start()

    return {
        "script": script,
        "status": "Started"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)