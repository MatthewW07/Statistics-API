"""HTTP API for the Statistics-API analysis objects."""

import math
from pathlib import Path
from typing import Any
from uuid import uuid4

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from src.cat_table import Categorical_Table
from src.heatmap import Heatmap
from src.num_table import Numerical_Table


app = FastAPI(
    title="Statistical Analysis API",
    description="Compute a correlation heatmap and one-variable statistics from a CSV file.",
    version="1.0.0",
)

UPLOAD_FOLDER = Path(__file__).resolve().parent / "uploads"
STATIC_FOLDER = Path(__file__).resolve().parent / "static"
MAX_UPLOAD_BYTES = 50 * 1024 * 1024

app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")

def to_jsonable(value: Any) -> Any:
    """Convert pandas and NumPy values into valid JSON-compatible values."""
    if isinstance(value, np.generic):
        return to_jsonable(value.item())
    if isinstance(value, np.ndarray):
        return [to_jsonable(item) for item in value.tolist()]
    if isinstance(value, (pd.Timestamp, pd.Timedelta)):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if value is None or isinstance(value, (str, int, bool)):
        return value
    # Covers pandas' missing-value sentinels without applying pd.isna to arrays.
    if pd.isna(value):
        return None
    return str(value)


def csv_path(file: str) -> Path:
    """Validate a CSV path supplied as a query parameter."""
    path = Path(file).expanduser()
    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"CSV file not found: {file}")
    if path.suffix.lower() != ".csv":
        raise HTTPException(status_code=422, detail="file must point to a .csv file")
    return path


def response(content: dict[str, Any]) -> JSONResponse:
    # ``to_jsonable`` turns NaN and infinity into null before Starlette renders
    # the response, which also keeps this compatible with older Starlette APIs.
    return JSONResponse(content=to_jsonable(content))


@app.get("/")
async def root():
    return FileResponse(STATIC_FOLDER / "index.html")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Store and validate an uploaded CSV, returning a reference for analysis."""
    if not file.filename or Path(file.filename).suffix.lower() != ".csv":
        raise HTTPException(status_code=422, detail="Upload a file with a .csv extension")

    content = await file.read(MAX_UPLOAD_BYTES + 1)
    await file.close()
    if not content:
        raise HTTPException(status_code=422, detail="The uploaded CSV is empty")
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"CSV exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB upload limit",
        )

    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
    stored_path = UPLOAD_FOLDER / f"{uuid4().hex}.csv"
    stored_path.write_bytes(content)

    try:
        # Parse a small sample now so invalid files fail at upload time rather
        # than later when a statistics endpoint is called.
        sample = pd.read_csv(stored_path, nrows=5)
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as exc:
        stored_path.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=f"Invalid CSV: {exc}") from exc

    return response({
        "file": str(stored_path),
        "original_filename": file.filename,
        "columns": sample.columns.tolist(),
        "message": "Upload complete. Pass the returned file value to an analysis endpoint.",
    })



@app.get("/heatmap")
async def get_heatmap(file: str = Query(..., description="Path to the CSV file to analyze")):
    heatmap = Heatmap(csv_path(file))
    variables = heatmap.variables.tolist()
    pair_details = {}
    for i, x_name in enumerate(variables):
        for j in range(i, len(variables)):
            y_name = variables[j]
            x_type, y_type = heatmap.types[x_name], heatmap.types[y_name]
            relationship = f"{x_type}_v_{y_type}"
            cell = heatmap.heatmap[i][j]
            pair_details[f"{x_name}|{y_name}"] = {
                "x": x_name,
                "y": y_name,
                "type": relationship,
                "metrics": cell.comps,
            }
    return response({
        "variables": variables,
        "column_types": heatmap.types,
        "default_metrics": heatmap.defaults,
        "correlation_matrix": heatmap.corr_matrix,
        "pair_details": pair_details,
    })


@app.get("/num_table")
async def get_num_table(file: str = Query(..., description="Path to the CSV file to analyze")):
    table = Numerical_Table(csv_path(file))
    return response({
        "columns": table.columns, 
        "variables": table.variables,
        "statistics": table.stats
    })


@app.get("/cat_table")
async def get_cat_table(file: str = Query(..., description="Path to the CSV file to analyze")):
    table = Categorical_Table(csv_path(file))
    return response({
        "columns": table.columns, 
        "variables": table.variables,
        "statistics": table.stats
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
