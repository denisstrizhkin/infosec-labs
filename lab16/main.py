from fastapi import FastAPI
from fastapi.responses import JSONResponse
import subprocess

app = FastAPI()


@app.get("/dns_lookup/{hostname}")
def dns_lookup(hostname: str):
    result = subprocess.run(
        f"dig +short {hostname}", shell=True, check=True, capture_output=True
    )
    ip_address = result.stdout.decode("utf8").strip()
    result = {"result": None}
    if ip_address:
        result["result"] = ip_address.split("\n")
    return JSONResponse(content=result)
