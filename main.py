from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import tensorflow.lite as tflite
import json
import os

app = FastAPI()

# --- Model and Label Loading ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.tflite')
LABELS_PATH = os.path.join(os.path.dirname(__file__), 'labels.json')
AVOCADO_INFO_PATH = os.path.join(os.path.dirname(__file__), 'avocado_info.json')

interpreter = None
labels = []
avocado_info = {}

def load_model_and_labels():
    global interpreter, labels, avocado_info
    try:
        interpreter = tflite.Interpreter(model_path=MODEL_PATH)
        interpreter.allocate_tensors()

        with open(LABELS_PATH, 'r') as f:
            labels = json.load(f)

        if os.path.exists(AVOCADO_INFO_PATH):
            with open(AVOCADO_INFO_PATH, 'r') as f:
                avocado_info = json.load(f)

    except FileNotFoundError as e:
        print(f"Error loading model or labels file: {e}")
    except Exception as e:
        print(f"An error occurred during model/label loading: {e}")

load_model_and_labels()

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if interpreter is None or not labels:
        raise HTTPException(status_code=503, detail="Model or labels not loaded.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        input_details = interpreter.get_input_details()
        input_shape = input_details[0]['shape']
        input_dtype = input_details[0]['dtype']
        expected_height, expected_width = input_shape[1], input_shape[2]

        image = image.resize((expected_width, expected_height))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image_np = np.array(image)

        if input_dtype == np.float32:
            image_np = image_np / 255.0

        image_np = np.expand_dims(image_np, axis=0)
        image_np = image_np.astype(input_dtype)

        input_tensor_index = interpreter.get_input_details()[0]['index']
        interpreter.set_tensor(input_tensor_index, image_np)
        interpreter.invoke()
        output_tensor_index = interpreter.get_output_details()[0]['index']
        output_data = interpreter.get_tensor(output_tensor_index)

        predictions = output_data[0]
        predicted_class_index = np.argmax(predictions)
        predicted_label = labels[predicted_class_index]
        confidence = predictions[predicted_class_index]

        results = {
            "predicted_label": predicted_label,
            "confidence": float(confidence)
        }

        if predicted_label in avocado_info:
            results["info"] = avocado_info[predicted_label]

        return JSONResponse(content=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")
