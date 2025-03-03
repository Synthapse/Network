from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import json

from pydantic import BaseModel
import openai

# Make sure you have the OpenAI package installed

import redis

from typing import List, Dict

# Set your OpenAI API key
# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


class Message(BaseModel):
    role: str
    content: str

class Conversation(BaseModel):
    agentId: str
    messages: List[Message]



agents = [
    {
        "id": "net1",
        "role": "You are a top-tier expert in Network Design for Smart Cities, responsible for optimizing IoT infrastructure.",
        "content": (
            "Your role includes ensuring high-speed, low-latency, and secure communication between smart city devices. "
            "You leverage 5G, LPWAN, edge computing, and AI-driven networking to improve efficiency.\n\n"
            "You also communicate with other experts:\n"
            "- **Cyber Security (cyb1)** to ensure networks are resilient against cyber threats.\n"
            "- **Energy Management (ene1)** to optimize network energy consumption.\n\n"
            "When making recommendations, request relevant security measures from the cybersecurity expert "
            "and energy efficiency insights from the energy management expert."
        ),
    },
    {
        "id": "ene1",
        "role": "You are a leading expert in Energy Management for Smart Cities, focusing on IoT-driven energy optimization. ",
        "content": (
            "Your expertise includes smart grids, renewable energy integration, and AI-based energy efficiency strategies. "
            "You develop real-time monitoring systems to optimize urban energy distribution.\n\n"
            "You also communicate with other experts:\n"
            "- **Network Design (net1)** to ensure energy-efficient network connectivity.\n"
            "- **Cyber Security (cyb1)** to secure smart grid data and prevent cyber threats.\n\n"
            "When making recommendations, request optimized network designs from the network expert "
            "and security strategies from the cybersecurity expert."
        ),
    },
    {
        "id": "cyb1",
        "role": "You are a highly skilled Cybersecurity Specialist for Smart Cities, dedicated to securing IoT networks. ",
        "content": (
            "Your expertise includes encryption, anomaly detection, zero-trust security, and AI-driven threat prevention. "
            "Your goal is to protect smart city infrastructure from cyber threats.\n\n"
            "You also communicate with other experts:\n"
            "- **Network Design (net1)** to implement secure networking strategies.\n"
            "- **Energy Management (ene1)** to secure smart grid systems from cyberattacks.\n\n"
            "When making recommendations, request insights from the network expert on secure data transmission "
            "and from the energy expert on protecting IoT-powered energy systems."
        ),
    },
]


# Also mediates the communication between the agents?
# Or just the AI responses?

class AICoordinator:

    def __init__(self, id):

        self.id = id
        self.agents = agents
        self.grok_api_key = "xai-cqEQdzQnn1lM04QasIuIxumn4NchsmhT9wYqzDc3qfIpx3IdjTVm0JUciiMEF3N4rwm7Jc5oZT8azev9"


    def get_agent(self, agent_id):
        return next((agent for agent in self.agents if agent["id"] == agent_id), None)

    def get_conversation(self, agent_id):
        history = redis_client.get(agent_id)

        return json.loads(history) if history else []

    def update_conversation(self, agent_id, other_agent_id, messages):
        redis_key = f"conv:{agent_id}:{other_agent_id}"  # ✅ Unique key
        redis_client.set(redis_key, json.dumps(messages))  # ✅ Store in Redis

    async def pair_agents_and_exchange(self):
        conversations = []  # Store (agent_id, other_agent_id, response)
        processed_pairs = set()  # Track unique agent pairs

        for agent in agents:
            history = self.get_conversation(agent["id"])
            if not history:
                history = [{"role": agent["role"], "content": agent["content"]}]
                self.update_conversation(agent["id"], agent["id"], history)  # Store self-convo

            for other_agent in agents:
                if agent["id"] == other_agent["id"]:  # Skip self-conversation
                    continue

                # Ensure unique pairs (A talks to B, but B doesn't reinitiate with A)
                pair = tuple(sorted([agent["id"], other_agent["id"]]))  # Ensures (A, B) == (B, A)
                if pair in processed_pairs:
                    continue  # Skip duplicate conversation

                processed_pairs.add(pair)  # Mark pair as processed

                print(f"Agent: {agent['id']} → Other Agent: {other_agent['id']}")

                history.append(
                    {"role": "user", "content": f"What advice do you have for {other_agent['id']}?"}
                )

                response_text = self.get_agent_conversation(agent, history)
                self.update_conversation(agent["id"], other_agent["id"], history)

                # Store (who talked to whom, conversation result)
                conversations.append((agent["id"], other_agent["id"], response_text))

        return conversations  # List of tuples

    def get_agent_conversation(self, agent, history):
        try:

            print(agent)
            print(history)

            client = openai.OpenAI (
                api_key=self.grok_api_key,
                base_url="https://api.x.ai/v1",
            )

            completion = client.chat.completions.create(
                model="grok-2-latest",
                messages=[
                    {
                        "role": "system",
                        "content": agent["role"]
                    },
                    {
                        "role": "user",
                        "content": str(history)
                    },
                ],
            )

            ai_answer = completion.choices[0].message.content
            print(ai_answer)

            redis_client.set(f"{agent['id']}_response", json.dumps(ai_answer))
            print(ai_answer)
            return ai_answer

        except Exception as e:
            return f"Error processing {agent['id']}: {str(e)}\n"

    def get_agent_response(self, agent):
        try:
            client = openai.OpenAI (
                api_key=self.grok_api_key,
                base_url="https://api.x.ai/v1",
            )

            completion = client.chat.completions.create(
                model="grok-2-latest",
                messages=[
                    {
                        "role": "system",
                        "content": agent["role"]
                    },
                    {
                        "role": "user",
                        "content": agent["content"]
                    },],
            )

            ai_answer = completion.choices[0].message.content
            print(ai_answer)

            redis_client.set(f"{agent['id']}_response", json.dumps(ai_answer))
            print(ai_answer)
            return ai_answer

        except Exception as e:
            return f"Error processing {agent['id']}: {str(e)}\n"