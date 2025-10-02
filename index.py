from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# Allow all origins, all headers, POST method
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow requests from any domain
    allow_methods=["POST"], 
    allow_headers=["*"]
)

@app.post("/")
async def latency_metrics(req: Request):
    body = await req.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 180)

    # Dummy telemetry data for testing
    dummy_data = {
        "amer": [100, 150, 200, 180],
        "emea": [120, 140, 190, 170]
    }

    result = {}
    for r in regions:
        latencies = dummy_data.get(r, [])
        if not latencies:
            continue
        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        avg_uptime = 1.0
        breaches = sum(l > threshold for l in latencies)
        result[r] = {
            "avg_latency": round(avg_latency,2),
            "p95_latency": round(p95_latency,2),
            "avg_uptime": avg_uptime,
            "breaches": breaches
        }

    return result
