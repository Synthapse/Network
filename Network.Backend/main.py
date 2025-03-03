from fastapi import FastAPI
import asyncio
import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import openai  # Make sure you have the OpenAI package installed
import asyncio
import redis
import json
from typing import List, Dict


from multiagent import AICoordinator, Message
from multiagent import agents

app = FastAPI()

# how it should be structured?
@app.get("/")
async def read_root():
    coord_id = "random_id"
    agent_coordinator = AICoordinator(coord_id)

    # res = []
    #
    # for agent in agents:
    #     response = await agent_coordinator.get_agent_response(agent)
    #     print(res)
    #     res.append(response)
    #
    # return res

    # asyncio.gather - make 3 operations asynchronously - but there is some error with coroutine.

    async def collect_responses(agent):
        response = agent_coordinator.get_agent_response(agent)  # Don't await yet
        print(f"Response type for {agent['id']}: {response} {type(response)}")  # Debugging
        print(response)
        return response

    results = await asyncio.gather(*(collect_responses(agent) for agent in agents))
    return results


@app.post("/chat")
async def chat_with_agent():

    coord_id = "random_id"
    agent_coordinator = AICoordinator(coord_id)

    r = await agent_coordinator.pair_agents_and_exchange()

    return r