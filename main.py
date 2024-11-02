from fastapi import FastAPI, HTTPException

from agents.AnalysisAgent import AnalysisAgent
from agents.GenerationAgent import GenerationAgent
from agents.DispatcherAgent import DispatcherAgent
from util.base_models import TextRequest

app = FastAPI()

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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
