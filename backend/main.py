from fastapi import FastAPI

app = FastAPI(title="Terraria Server Manager")

@app.get("/")
def read_root():
    print("Hello World")
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
