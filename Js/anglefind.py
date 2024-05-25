import numpy as np
import requests
import json
import math
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.requests import Request
from test_requst import pull_sheet_data, gsheet_api_check
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
class TrajectoryCalculator:
    def __init__(self, g=9.81, x_target=2, y_launch=0.05, tolerance=0.001, v0=6.5):
        self.g = g
        self.x_target = x_target
        self.y_launch = y_launch
        self.tolerance = tolerance
        self.v0 = v0

    def update_y_target(self, y_target):
        self.y_target = y_target

    def y_position(self, theta, t):
        return self.y_launch + self.v0 * np.sin(np.radians(theta)) * t - 0.5 * self.g * t**2

    def time_to_reach_x(self, theta):
        return self.x_target / (self.v0 * np.cos(np.radians(theta)))
    
    def x_position(self, theta, t):
        return self.v0 * np.cos(np.radians(theta)) * t


    def find_optimal_angle(self):
        best_theta = None
        min_error = float('inf')
        for theta in np.linspace(10, 60, 1000):  # Varying angle from 20 to 60 degrees
            t = self.time_to_reach_x(theta)
        
            y = self.y_position(theta, t)
            error = abs(y - self.y_target)
            # print(f"Theta: {theta}, Time: {t}, Y: {y}, Error: {error}")
            if error < min_error and (self.y_target - self.tolerance <= y <= self.y_target + self.tolerance):
                min_error = error
                best_theta = theta
                print(f"y_target: {self.y_target}, tolerance: {self.tolerance}")

                print(f"Best theta: {best_theta}, Min error: {min_error}")

        return best_theta, min_error
    
    def generate_trajectory_data(self, theta):
        time_points = np.linspace(0, self.time_to_reach_x(theta), num=500)
        # time_points_rob 
        x_points = [self.x_position(theta, t) for t in time_points]
        y_points_rob = [self.y_position(theta, t) for t in time_points if self.y_position(theta, t) >= 0.5]
        y_points = [self.y_position(theta, t) for t in time_points]
        z_points = [0 for t in time_points]
        return {"x": x_points,"y": y_points, "y_rob": y_points_rob,"z": z_points, "t": time_points.tolist()}


if __name__ == "__main__":
    calculator = TrajectoryCalculator()
    calculator.update_y_target()
    theta, error = calculator.find_optimal_angle()
    if theta is not None:
        time_to_target = calculator.time_to_reach_x(theta)
        y_at_target = calculator.y_position(theta, time_to_target)
        print(f"Optimal angle: {theta}")
        print(f"Fixed velocity: {calculator.v0}")
        print(f"Minimum error: {error}")
        print(f"Time to target: {time_to_target}")
        print(f"Y position at target: {y_at_target}")
    else:
        print("No valid angle found within the specified tolerance.")

# Initialize the FastAPI app
app = FastAPI()

@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

origins = [
    "http://localhost:5000",
    "http://localhost:8080",
    "http://127.0.0.1:5500",  # Front-end URL
    "http://localhost:8000"   # Corrected
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# http://127.0.0.1:5500/
# allowed_origins = ["http://127.0.0.1:5500"]

# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     response = await call_next(request)
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     return response
    
# Initialize the trajectory calculator
calculator = TrajectoryCalculator()

class TargetData(BaseModel):
    targetX: float
    targetZ: float
    posX: float
    posY: float
    posZ: float

class OptimalAngleResponse(BaseModel):
    optimal_angle: float
    fixed_velocity: float
    minimum_error: float
    time_to_target: float
    y_position_at_target: float

class CoordinateRequest(BaseModel):
    targetX: float
    targetZ: float
    posX: float
    posY: float
    posZ: float

optimal_angle1 = 0
fixed_velocity1 = 0
minimum_error1 = 0
time_to_target1 = 0
y_position_at_target1 = 0



trajectory_data_store = {}


@app.post("/data", response_model=OptimalAngleResponse)
async def post_optimal_angle(data: TargetData):
    calculator = TrajectoryCalculator()
    # print(f"Received data: {data}")
    # calculator.x_target = data.targetX
    calculator.update_y_target(data.targetZ/1000)
    print(f"Updated x_target: {calculator.x_target}, y_target: {calculator.y_target}")
    print((data.targetZ/1000))
    
    theta, error = calculator.find_optimal_angle()
    print(f"Optimal angle: {theta}")
    print(f"Optimal angle: {theta}")
    if theta is not None:
        time_to_target = calculator.time_to_reach_x(theta)
        y_at_target = calculator.y_position(theta, time_to_target)
        print(f"Optimal angle: {theta}")
        trajectory_data = calculator.generate_trajectory_data(theta)
        trajectory_data_store['data'] = trajectory_data

        global optimal_angle1
        optimal_angle1 = round(theta)
        print("Optimal angle: ", optimal_angle1)
        global fixed_velocity1
        fixed_velocity1 = calculator.v0
        
        global minimum_error1
        minimum_error1 = error
        global time_to_target1
        time_to_target1 = time_to_target
        global y_position_at_target1
        y_position_at_target1 = y_at_target
        trajectory_data = calculator.generate_trajectory_data(theta)
        # with open('projectile_data_test.json', 'w') as json_file:
        #     json.dump(trajectory_data, json_file)
        
        

        # Your data object that needs to be sent as JSON
        data = {
            'targetX': data.targetX,
            'targetZ': data.targetZ,
            'posX': data.posX,
            'posY': data.posY,
            'posZ': data.posZ,
            'angle': optimal_angle1,
            'velocity': fixed_velocity1
            # 'k': 
        }

        # URL to the Google Apps Script Web App
        url = 'https://script.google.com/macros/s/AKfycbxt3Z7yeXxNudrNn7WYUyG4oIkA1dp1MnYnvDCqP2INezWiGF5z7pNpH4Oi3VLadsZBTg/exec'

        # Making a POST request
        # print(f"data: {data}")
        response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))

        # # Check if the request was successful
        # if response.status_code == 200:
        #     print("Request was successful!")
        #     print(response.text)  # Process the response if needed
        # else:
        #     print(f"Error fetching angle and velocity: {response.status_code} {response.reason}")

        

        return OptimalAngleResponse(
            optimal_angle=round(theta),
            fixed_velocity=calculator.v0,
            minimum_error=error,
            time_to_target=time_to_target,
            y_position_at_target=y_at_target
        )
        
        
    else:
        print("No valid angle found within the specified tolerance.")
        raise HTTPException(status_code=404, detail="No valid angle found within the specified tolerance.")


@app.get("/table")
async def get_table():
    # Fetch data from Google Sheets API
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '15RY2X_TGgvw37gEl6GPtc7Eg-O-DoHT06UTzMWQjdDo'
    DATA_TO_PULL = 'Data'
    data = pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL)
    df = pd.DataFrame(data[1:], columns=data[0])
    latest_row = df.iloc[-1]
    print(latest_row)
    return latest_row

@app.get("/data")
async def get_trajectory():
    # Fetch data from Google Sheets API
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '15RY2X_TGgvw37gEl6GPtc7Eg-O-DoHT06UTzMWQjdDo'
    DATA_TO_PULL = 'Data'
    data = pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL)
    df = pd.DataFrame(data[1:], columns=data[0])
    latest_row = df.iloc[-1]
    # print(latest_row)

    data = CoordinateRequest(
        targetX=float(latest_row['targetX']),
        targetZ=float(latest_row['targetZ']),
        posX=float(latest_row['posX']),
        posY=float(latest_row['posY']),
        posZ=float(latest_row['posZ'])
    )
    calculator = TrajectoryCalculator()
    # print(f"Received data: {data}")
    # calculator.x_target = data.targetX
    calculator.update_y_target(data.targetZ/1000)
    print((data.targetZ/1000))
    # Simplified physics for projectile motion
    g = 9.81  # gravity

    # angle = math.atan2(data.targetZ - data.posZ, data.targetX - data.posX)
    # velocity = 20  # Assume a fixed velocity for simplicity

    # time_of_flight = (2 * velocity * math.sin(angle)) / g
    num_points = 100
    # time_intervals = [i * time_of_flight / num_points for i in range(num_points + 1)]
    theta, error = calculator.find_optimal_angle()
    print(f"Optimal angle: {theta}")
    print(f"Optimal angle: {theta}")
    if theta is not None:
        time_to_target = calculator.time_to_reach_x(theta)
        y_at_target = calculator.y_position(theta, time_to_target)
        print(f"Optimal angle: {theta}")
        trajectory_data = calculator.generate_trajectory_data(theta)
        trajectory_data_store['data'] = trajectory_data
    # x_coords = [data.posX + velocity * math.cos(angle) * t for t in time_intervals]
    # z_coords = [data.posZ + velocity * math.sin(angle) * t - 0.5 * g * t**2 for t in time_intervals]
    # y_coords = [data.posZ + velocity * math.sin(angle) * t - 0.5 * g * t**2 for t in time_intervals]  # Assuming flat ground for simplicity
    # print(f"X: {x_coords}, Y: {y_coords}, Z: {z_coords}")
        print(f"trajectory_data: {trajectory_data}")

        return trajectory_data_store

    # Calculate projectile motion trajectory...
    # return {"message": "Success", "data": data}  # Example response

@app.get("/get")
async def get_optimal_angle():
    print("Optimal angle: ", optimal_angle1)

    return {
        "optimal_angle": optimal_angle1,
        "fixed_velocity": fixed_velocity1,
        "minimum_error": minimum_error1,
        "time_to_target": time_to_target1,
        "y_position_at_target": y_position_at_target1
    }
    