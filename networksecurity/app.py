import sys
import os
import pandas as pd

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from networksecurity.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

# -------------------- FASTAPI INIT --------------------
app = FastAPI()

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- TEMPLATE SETUP --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# -------------------- HOME ROUTE --------------------
@app.get("/")
async def index():
    return RedirectResponse(url="/docs")

# -------------------- TRAIN ROUTE --------------------
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return {"message": "Training successful"}
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# -------------------- PREDICT ROUTE --------------------
@app.post("/predict", response_class=HTMLResponse)
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # 📌 Read CSV
        df = pd.read_csv(file.file)

        if df.shape[0] == 0:
            return HTMLResponse("<h3>No data in uploaded file</h3>")

        # 📌 Load model + preprocessor
        preprocessor = load_object("final_model/preprocessor.pkl")
        model = load_object("final_model/model.pkl")

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=model
        )

        # 📌 Prediction
        y_pred = network_model.predict(df)
        df["predicted_column"] = y_pred

        # 📌 Save output
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)

        # 📌 Convert to HTML table
        table_html = df.to_html(classes="table table-striped", index=False, escape=False)

        # ✅ IMPORTANT: Template name must be STRING
        return templates.TemplateResponse(
            "table.html",
            {
                "request": request,
                "table": table_html
            }
        )

    except Exception as e:
        print("❌ ERROR:", e)   # debug log
        raise NetworkSecurityException(e, sys)


# -------------------- MAIN --------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)