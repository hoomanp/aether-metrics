from fastapi import FastAPI, HTTPException
from aether_metrics.agents.models import A2AMessage, CoverageMetrics, AIUsageMetrics, VelocityMetrics
import json
import httpx
import os

app = FastAPI(title="Aether-Metrics Orchestrator Agent")

# In-memory storage for demonstration
METRIC_DB = {
    "coverage": [],
    "ai_usage": [],
    "velocity": []
}

@app.post("/a2a/receive")
async def receive_message(message: A2AMessage):
    """
    Standard A2A (Agent-to-Agent) endpoint for receiving tasks or data.
    """
    print(f"Received message from {message.sender_id}: {message.request_type}")
    
    if message.request_type == "REPORT_METRICS":
        return await handle_metrics_report(message)
    elif message.request_type == "QUERY_STATUS":
        return {"status": "operational", "active_collectors": 3}
    else:
        raise HTTPException(status_code=400, detail="Unknown request type")

async def handle_metrics_report(message: A2AMessage):
    # Logic to process incoming metrics from collector agents
    payload = message.payload
    if "coverage" in payload:
        METRIC_DB["coverage"].append(CoverageMetrics(**payload["coverage"]))
    if "ai_usage" in payload:
        METRIC_DB["ai_usage"].append(AIUsageMetrics(**payload["ai_usage"]))
    if "velocity" in payload:
        METRIC_DB["velocity"].append(VelocityMetrics(**payload["velocity"]))
    return {"status": "success", "message": "Metrics recorded"}

@app.get("/dashboard/summary")
async def get_summary():
    """
    Returns a high-level summary of all KPIs.
    """
    avg_coverage = sum(m.line_coverage_pct for m in METRIC_DB["coverage"]) / len(METRIC_DB["coverage"]) if METRIC_DB["coverage"] else 0
    total_tokens = sum(m.token_count for m in METRIC_DB["ai_usage"])
    
    return {
        "average_test_coverage": f"{avg_coverage:.2f}%",
        "total_tokens_consumed": total_tokens,
        "active_microservices": len(set(m.microservice for m in METRIC_DB["coverage"] if m.microservice)),
        "alert_status": "NORMAL" if avg_coverage > 80 else "LOW_COVERAGE_DETECTED"
    }

async def hire_agent(agent_url: str, request_type: str, payload: dict):
    """
    A2A Capability: Hire another agent to perform a specialized task.
    """
    async with httpx.AsyncClient() as client:
        message = A2AMessage(
            sender_id="Aether-Orchestrator",
            recipient_id="Specialized-Agent",
            request_type=request_type,
            payload=payload
        )
        response = await client.post(f"{agent_url}/a2a/receive", json=message.dict())
        return response.json()

# Example usage for A2A logic:
# if avg_coverage < 80:
#     await hire_agent("http://test-gen-agent:8001", "GENERATE_TESTS", {"repo": "my-service"})
