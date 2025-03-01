import { NextResponse } from "next/server";
import OpenAI from "openai";

// Initialize the OpenAI client
const client = new OpenAI({
  apiKey: process.env.GROK_API_KEY,
  baseURL: "https://api.x.ai/v1",
});

export async function POST(req) {
  let messages;
  try {
    const body = await req.json();
    messages = body.messages;
    console.log("Received Messages:", messages);
  } catch (error) {
    console.error("Failed to parse request body:", error.message);
    return NextResponse.json({ error: "Invalid request body" }, { status: 400 });
  }

  const apiKey = process.env.GROK_API_KEY;
  console.log("Using API Key:", apiKey || "Missing");

  if (!apiKey) {
    return NextResponse.json({ error: "API key not configured" }, { status: 500 });
  }

  const agents = [
    { role: "system", content: "You are an expert in Network Design for Smart Cities, focusing on IoT infrastructure optimization." },
    { role: "system", content: "You are an expert in Energy Management for Smart Cities, focusing on IoT-based energy efficiency." },
    { role: "system", content: "You are an expert in Cyber Security for Smart Cities, focusing on securing IoT networks." },
  ];

  try {
    const agentResponses = await Promise.all(
      agents.map(async (agent) => {
        const requestMessages = [agent, ...messages.slice(1)];
        console.log("Processing for agent:", agent.content);
        console.log("Request Messages:", requestMessages);

        const completion = await client.chat.completions.create({
          model: "grok-2-latest",
          messages: requestMessages,
          stream: false,
          temperature: 0,
        });

        console.log("Raw Completion:", completion);
        const reply = completion.choices[0]?.message?.content;
        if (!reply) {
          throw new Error("No content in response");
        }

        return {
          agent: agent.content.split(" ")[4], // "Network", "Energy", "Cyber"
          reply,
        };
      })
    );

    return NextResponse.json({ replies: agentResponses });
  } catch (error) {
    console.error("Error Details:", error.message);
    if (error.response) {
      console.error("API Response Error:", error.response.status, error.response.data);
    }
    return NextResponse.json({ error: `Failed to fetch Grok API: ${error.message}` }, { status: 500 });
  }
}