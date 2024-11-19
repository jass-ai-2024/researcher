from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from src.runner import chat

app = FastAPI()


class FromArch(BaseModel):
    text: str


@app.post("/research")
async def submit_text(request: FromArch):
    text = request.text
    result = chat(a, session_id)
    pass
    # TODO return research result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
