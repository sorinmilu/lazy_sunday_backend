from app.main import app

#Fisierul principal care lanseaza aplicatia. 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

