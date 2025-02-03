from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import json
import time

app = FastAPI()

class UserInput(BaseModel):
    text: str

@app.post("/process/")
async def process_input(user_input: UserInput):
    try:
        # Save input to input.json
        with open("./input.json", "w") as f:
            json.dump(user_input.dict(), f)

        # Run the TypeScript script
        result = subprocess.run(
            ["npm", "run", "start", "src/parasolv5.ts"],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        # Wait for output.json to be created
        time.sleep(1)

        # Read and parse the agent's thinking process from output.json
        with open("./output.json", "r") as f:
            output_data = json.load(f)

        # Ensure output_data contains detailed agent responses
        if "thinking_process" in output_data:
            return {"steps": output_data["thinking_process"], "final_answer": output_data["result"]}
        else:
            return {"final_answer": output_data["result"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)