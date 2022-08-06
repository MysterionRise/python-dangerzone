import io

import pandas as pd
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/toloka", StaticFiles(directory="."), name="toloka")


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), limit: int = Form(...)):
    results = []
    df = pd.read_csv(io.StringIO(file.file.read().decode("utf-8")), sep="\t")
    df = (
        df[["ASSIGNMENT:worker_id", "OUTPUT:pic_name", "OUTPUT:pic_act_list"]]
        .groupby(["ASSIGNMENT:worker_id"])
        .agg(["count"])
    )
    for index, row in df.iterrows():
        print(index)
        print(row)
        if (
            64 - (row["OUTPUT:pic_name"]["count"] + row["OUTPUT:pic_act_list"]["count"])
            > limit
        ):
            results.append(index)

    return {
        "filename": file.filename,
        "results": results,
        "limit": limit,
        "size": len(results),
    }
