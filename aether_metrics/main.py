import uvicorn
import threading
import time
import asyncio
import httpx
from aether_metrics.agents.orchestrator import app as orchestrator_app
from aether_metrics.collectors.base_collector import AIUsageCollector, CoverageCollector

# Mock orchestrator URL
ORCHESTRATOR_URL = "http://localhost:8000"

def start_orchestrator():
    """Run the orchestrator in a separate thread."""
    uvicorn.run(orchestrator_app, host="0.0.0.0", port=8000, log_level="error")

async def run_mock_collection_cycle():
    """Simulate a periodic data collection cycle."""
    print("\n--- Starting Mock Collection Cycle ---\n")
    
    # Initialize collectors
    ai_collector = AIUsageCollector(ORCHESTRATOR_URL)
    cov_collector = CoverageCollector(ORCHESTRATOR_URL)
    
    # Simulate data gathering
    await ai_collector.collect_usage("dev-123", "GitHub Copilot", 1500, "code_gen")
    await ai_collector.collect_usage("dev-456", "Cursor", 300, "debugging")
    
    await cov_collector.parse_coverage_file("lcov.info", "auth-service", "user-mgmt")
    await cov_collector.parse_coverage_file("lcov.info", "billing-service", "payment-gateway")
    
    print("\n--- Collection Cycle Complete ---\n")
    
    # Fetch summary to show it works
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{ORCHESTRATOR_URL}/dashboard/summary")
        print(f"Current Dashboard Summary: {resp.json()}")

if __name__ == "__main__":
    # Start orchestrator in background
    thread = threading.Thread(target=start_orchestrator, daemon=True)
    thread.start()
    
    # Wait for orchestrator to start
    time.sleep(2)
    
    # Run a collection cycle
    asyncio.run(run_mock_collection_cycle())
    
    print("\nAgent is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
