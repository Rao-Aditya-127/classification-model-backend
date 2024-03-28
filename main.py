from fastapi import FastAPI, UploadFile, File , HTTPException
from fastapi.responses import JSONResponse
import subprocess
import json
import os

# creating an instance
app = FastAPI()

# Define the directory where uploaded files will be saved
upload_folder = "D:\CODE\Fastapi\image"
stored_string = "full path of file"


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Create the full path to save the file
    file_path = os.path.join(upload_folder, file.filename)
    global stored_string 
    print(file_path)
    stored_string = file_path 
    # Save the file
    with open(file_path, "wb") as image:
        image.write(file.file.read())
    
    # Return a response with the filename
    return {"filename": file.filename}

@app.get("/run-model")
async def run_model():
    try:
        global stored_string
        print(stored_string)
        # Run the model.py script using subprocess
        result = subprocess.run(["python", "model.py" , stored_string], capture_output=True, text=True)
        
        # Check if the subprocess ran successfully
        if result.returncode == 0:
            # Attempt to find and extract the JSON part from the output
            print(result)
            json_start = result.stdout.find("{")
            json_end = result.stdout.rfind("}")
            
            # Check if JSON part is found
            if json_start != -1 and json_end != -1:
                json_str = result.stdout[json_start:json_end+1]
                
                # Parse the JSON string
                output_json = json.loads(json_str)
                
                # Return the JSON as a response
                return JSONResponse(content=output_json, status_code=200)
            else:
                raise HTTPException(status_code=500, detail="JSON not found in model output.")
        else:
            # If the subprocess failed, raise an HTTPException
            raise HTTPException(status_code=500, detail="Model execution failed.")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/run-grading-model")
async def run_model():
    try:
        global stored_string
        print(stored_string)
        # Run the model.py script using subprocess
        result = subprocess.run(["python", "grading_model.py" , stored_string], capture_output=True, text=True)
        
        # Check if the subprocess ran successfully
        if result.returncode == 0:
            # Attempt to find and extract the JSON part from the output
            print(result)
            json_start = result.stdout.find("{")
            json_end = result.stdout.rfind("}")
            
            # Check if JSON part is found
            if json_start != -1 and json_end != -1:
                json_str = result.stdout[json_start:json_end+1]
                
                # Parse the JSON string
                output_json = json.loads(json_str)
                
                # Return the JSON as a response
                return JSONResponse(content=output_json, status_code=200)
            else:
                raise HTTPException(status_code=500, detail="JSON not found in model output.")
        else:
            # If the subprocess failed, raise an HTTPException
            raise HTTPException(status_code=500, detail="Model execution failed.")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=str(e))
    