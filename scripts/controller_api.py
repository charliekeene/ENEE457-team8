from fastapi import FastAPI
import uvicorn
import subprocess
import os

app = FastAPI()

@app.post("/run-script")
def run_script(script: str):
    script_path = os.path.join("/scripts", script)

    if not os.path.isfile(script_path):
        return {"error": f"Script '{script}' not found."}

    # Execute the script
    result = subprocess.run(
        ["python3", script_path], capture_output=True, text=True
    )

    return {
        "script": script,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)