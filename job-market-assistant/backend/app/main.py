from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent import JobMarketAgent
import uuid

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = JobMarketAgent()

class ChatRequest(BaseModel):
    message: str
    user_id: str = None

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Generate or use provided user ID
        user_id = request.user_id or str(uuid.uuid4())
        
        # Get response from agent
        response = await agent.generate_response(user_id, request.message)
        
        return {
            "response": response,
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tools/{tool_name}")
async def use_tool(tool_name: str, params: dict):
    try:
        result = await agent.use_tool(tool_name, **params)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)