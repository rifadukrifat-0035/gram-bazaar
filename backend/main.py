from fastapi import FastAPI
app = FastAPI(title="Gram-Bazaar API")

@app.get("/")
def read_root():
    return {"message": "Backend is alive!"}
