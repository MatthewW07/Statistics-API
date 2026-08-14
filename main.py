"""HTTP API for the Statistics-API analysis objects."""

import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from src.cat_table import Categorical_Table
from src.heatmap import Heatmap
from src.num_table import Numerical_Table


app = FastAPI(
    title="Statistical Analysis API",
    description="Compute a correlation heatmap and one-variable statistics from a CSV file.",
    version="1.0.0",
)


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
    return {
        "status": "API is running",
        "docs": "/docs",
        "endpoints": ["/heatmap", "/num_table", "/cat_table"],
    }


@app.get("/heatmap")
async def get_heatmap(file: str = Query(..., description="Path to the CSV file to analyze")):
    heatmap = Heatmap(csv_path(file))
    # Cells contain pandas Series and are intentionally kept internal.  
    # The correlation matrix is the portable API representation of the heatmap.
    return response({
        "columns": heatmap.columns.tolist(),
        "column_types": heatmap.types,
        "metric": {
            "num_v_num": "pearson",
            "num_v_cat": "eta",
            "cat_v_cat": "cramer",
        },
        "heatmap": heatmap.corr_matrix,
    })


@app.get("/num_table")
async def get_num_table(file: str = Query(..., description="Path to the CSV file to analyze")):
    table = Numerical_Table(csv_path(file))
    return response({"columns": table.columns, "statistics": table.stats})


@app.get("/cat_table")
async def get_cat_table(file: str = Query(..., description="Path to the CSV file to analyze")):
    table = Categorical_Table(csv_path(file))
    return response({"columns": table.columns, "statistics": table.stats})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
