from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents.AnalysisAgent import AnalysisAgent
from agents.GenerationAgent import GenerationAgent
from agents.DispatcherAgent import DispatcherAgent
from context.manager import session_manager
from util.base_models import TextRequest, ChatRequest, ChatResponse
from util.formatting import to_html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analysis_agent = AnalysisAgent()
generation_agent = GenerationAgent()
dispatcher_agent = DispatcherAgent()


@app.post("/")
async def generate_response(request: TextRequest):
    try:
        task = dispatcher_agent.route_request(request.text)

        if task == "análisis de sentimiento":
            response = analysis_agent.handle_request(request.text)
        elif task == "generación de texto":
            response = generation_agent.handle_request(request.text)
        else:
            raise HTTPException(
                status_code=400,
                detail="No se encontró un agente adecuado para la tarea.",
            )

        return {"response": response}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id, history = session_manager.get_or_create(request.session_id)
        response_text = generation_agent.handle_request(request.text, history)
        session_manager.add_messages(session_id, request.text, response_text)
        return ChatResponse(response=to_html(response_text), session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/chat/{session_id}")
async def clear_chat(session_id: str):
    session_manager.clear(session_id)
    return {"message": "Session cleared"}
