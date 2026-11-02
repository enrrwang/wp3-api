from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="WP3 Simulation API")


class SimulationInput(BaseModel):
    disruption_days: int = Field(ge=1, le=120)
    daily_volume: float = Field(ge=0)
    daily_capacity: float = Field(ge=0)


@app.get("/")
def home():
    return {"status": "WP3 API is running"}


@app.post("/simulate")
def simulate(data: SimulationInput):
    backlog = 0
    results = []

    for day in range(1, data.disruption_days + 1):
        backlog = max(
            0,
            backlog + data.daily_volume - data.daily_capacity
        )

        results.append({
            "day": day,
            "backlog": backlog
        })

    return {
        "total_days": data.disruption_days,
        "final_backlog": backlog,
        "daily_results": results
    }
