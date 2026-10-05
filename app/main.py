from fastapi import FastAPI

app = FastAPI(title="Inventory API")


@app.get("/")
def read_root():
    return {"message": "Inventory API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
