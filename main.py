from fastapi import FastAPI

from TankSensor import TankSensor


sensor = TankSensor()
app = FastAPI()


@app.get("/")
async def root():
    return {
        "level": sensor.get_level_over_100(),
        "volume": sensor.get_level_in_volume(),
        "distance_from_sensor": sensor.sensor.distance,
        "distance_from_ground": sensor.distance_from_ground(),
    }
