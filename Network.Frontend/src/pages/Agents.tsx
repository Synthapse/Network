// @ts-nocheck
//01.03.2025 - quite bad, but it's hackhathon... and prototype needs to be deliver fast
"use client";
//import { NextResponse } from "next/server";
import OpenAI from "openai";
import axios from "axios";
import { useState, useEffect, useRef } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Chart } from "react-chartjs-2";
import img from "../assets/agent1.png";
import { Send } from "lucide-react";

const client = new OpenAI({
  //https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
  apiKey: "xai-cqEQdzQnn1lM04QasIuIxumn4NchsmhT9wYqzDc3qfIpx3IdjTVm0JUciiMEF3N4rwm7Jc5oZT8azev9", dangerouslyAllowBrowser: true,
  baseURL: "https://api.x.ai/v1",
});

export default function Home() {

  const [responses, setResponses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);


  const [agentsData, setAgentsData] = useState<ISystemRequest>([{
    title: "",
    numDevices: "",
    category: "",
    networkAgent: {
      agentId: "",
      recommendation: "",
    },
    energyAgent: {
      agentId: "",
      recommendation: "",
    },
    cyberSecurityAgent: {
      agentId: "",
      recommendation: "",
    },

  }]);
  // const [title, setTitle] = useState("");
  // const [numDevices, setNumDevices] = useState("");
  // const [category, setCategory] = useState("");

  const categories = [
    {
      name: "Smart Farming",
      description: "IoT solutions for agriculture, including precision farming, smart irrigation, and livestock monitoring",
    },
    {
      name: "Healthcare",
      description: "IoT-based healthcare solutions for patient monitoring, smart medical devices, and hospital automation",
    },
    {
      name: "Industrial IoT",
      description: "IoT solutions for manufacturing, logistics, and predictive maintenance",
    },
    {
      name: "Smart City",
      description: "IoT applications for home automation, security, and energy efficiency",
    },
  ];

  const requestLLms = async () => {

    const agents = [
      {
        id: "net1",
        role: "system",
        content: `You are a top-tier expert in Network Design for Smart Cities, responsible for optimizing IoT infrastructure. Your role includes ensuring high-speed, low-latency, and secure communication between smart city devices. You leverage 5G, LPWAN, edge computing, and AI-driven networking to improve efficiency.  

       You also communicate with other experts:  
       - **Cyber Security (cyb1)** to ensure networks are resilient against cyber threats.  
       - **Energy Management (ene1)** to optimize network energy consumption.  
       
       When making recommendations, request relevant security measures from the cybersecurity expert and energy efficiency insights from the energy management expert.`},
      {
        id: "ene1",
        role: "system",
        content: `You are a leading expert in Energy Management for Smart Cities, focusing on IoT-driven energy optimization. Your expertise includes smart grids, renewable energy integration, and AI-based energy efficiency strategies. You develop real-time monitoring systems to optimize urban energy distribution.  

        You also communicate with other experts:  
        - **Network Design (net1)** to ensure energy-efficient network connectivity.  
        - **Cyber Security (cyb1)** to secure smart grid data and prevent cyber threats.  
        
        When making recommendations, request optimized network designs from the network expert and security strategies from the cybersecurity expert.`
      },
      {
        id: "cyb1",
        role: "system",
        content: `You are a highly skilled Cybersecurity Specialist for Smart Cities, dedicated to securing IoT networks. Your expertise includes encryption, anomaly detection, zero-trust security, and AI-driven threat prevention. Your goal is to protect smart city infrastructure from cyber threats.  

        You also communicate with other experts:  
        - **Network Design (net1)** to implement secure networking strategies.  
        - **Energy Management (ene1)** to secure smart grid systems from cyberattacks.  
        
        When making recommendations, request insights from the network expert on secure data transmission and from the energy expert on protecting IoT-powered energy systems.`
      },
    ];

    try {
      const agentResponses = await Promise.all(
        agents.map(async (agent) => {

          console.log("Processing for agent:", agent.id);

          const completion = await client.chat.completions.create({
            model: "grok-2-latest",
            messages: [{
              role: agent.role,
              content: agent.content,
            }],
            stream: false,
            temperature: 0,
          });

          console.log(completion.choices[0]?.message?.content);

          console.log("Raw Completion:", completion);
          const reply = completion.choices[0]?.message?.content;

          // 1 request per 1 agnet

          if (agent.id === "net1") {
            setAgentsData({
              ...agentsData,
              networkAgent: {
                agentId: agent.id,
                recommendation: reply,
              },
            });

            setResponses((prev) =>
              prev.map((ag) =>
                ag.agentId === agent.id ? { ...ag, response: reply } : ag // Fix: Spread `ag` instead of `agent`
              )
            );
          } else if (agent.id === "ene1") {
            setAgentsData({
              ...agentsData,
              energyAgent: {
                agentId: agent.id,
                recommendation: reply,
              },
            });

            setResponses((prev) =>
              prev.map((ag) =>
                ag.agentId === agent.id ? { ...ag, response: reply } : ag
              )
            );
          } else if (agent.id === "cyb1") {
            setAgentsData({
              ...agentsData,
              cyberSecurityAgent: {
                agentId: agent.id,
                recommendation: reply,
              },
            });

            setResponses((prev) =>
              prev.map((ag) =>
                ag.agentId === agent.id ? { ...ag, response: reply } : ag
              )
            );
          }
        })
      );

    } catch (error) {
      console.error("Error Details:", error.message);
      if (error.response) {
        console.error("API Response Error:", error.response.status, error.response.data);
      }
    }
  };

  const requestRaporting = async () => {

    axios.post(`https://raporting-319936913236.europe-central2.run.app/generateDocument`, null, {
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(agentsData),
      responseType: 'blob'
    })
      .then(response => {
        console.log(response)
      })
      .catch(error => {
        console.error('Error:', error);
      });

  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setResponses([]); // Reset responses

    const query = `Provide a detailed response for ${agentsData.category} infrastructure with title "${agentsData.category}" and ${agentsData.numOfDevices} devices. Focus on your area of expertise.`;

    // Initialize responses with progress tracking (set to 100% since we want progress bars visible)
    const initialResponses = [
      { agentId: 'net1', agent: "Network Design", response: "Processing...", progress: 100, icon: img },
      { agentId: 'ene1', agent: "Energy Management", response: "Processing...", progress: 100, icon: img },
      { agentId: 'cyb1', agent: "Cyber Security", response: "Processing...", progress: 100, icon: img },
    ];


    setResponses(initialResponses);

    // Simulate progress for each agent (optional, since progress is always 100%)
    const interval = setInterval(() => {
      setResponses((prev) =>
        prev.map((r) => ({
          ...r,
          progress: 100, // Keep progress at 100% as per screenshot
        }))
      );
    }, 500);


    // Call to GROK
    const grokResponse = await requestLLms();
    // Call to Raporting
    const raportResponse = await requestRaporting();

    console.log("Grok Response:", grokResponse);

    console.log(agentsData);

    // const updatedResponses = data.replies.map((reply, index) => ({
    //   agent: initialResponses[index].agent,
    //   response: reply.reply,
    //   progress: 100, // Keep progress at 100% as per screenshot
    //   icon: initialResponses[index].icon,
    // }));
  };


  // Calculate average response length for the graph
  const calculateAverageResponseLength = () => {
    if (responses.length === 0) return 0;
    const totalLength = responses.reduce((sum, r) => sum + (r.response?.length || 0), 0);
    return totalLength / responses.length;
  };


  // 01.03.2025 grafana for charts
  const chartData = {
    labels: ["Average Response Length"],
    datasets: [
      {
        label: "Characters",
        data: [calculateAverageResponseLength()],
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Average Response Length Across Agents" },
    },
    scales: { y: { beginAtZero: true } },
  };

  let messages;

  const canSubmit = isLoading || !agentsData.title || !agentsData.numDevices || !agentsData.category


  console.log(responses);

  return (
    <div className="container mx-auto p-5 max-w-4xl"> {/* Increased max width to make it larger */}
      <h1 className="text-2xl font-bold mb-5 text-gray-900">Describe Your IoT Infrastructure</h1>
      <form onSubmit={handleSubmit} className="mb-5 p-5 bg-white rounded-lg shadow-md">
        <div className="mb-4">
          <label className="block mb-2 text-sm font-medium text-gray-700">What's the title and your IoT infrastructure structure?</label>
          <Textarea
            value={agentsData.title}
            onChange={(e) => setAgentsData({ ...agentsData, title: e.target.value })}
            placeholder="Enter title and description"
            className="w-full border border-gray-300 rounded-md"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-2 text-sm font-medium text-gray-700">Number of devices</label>
          <Select
            value={agentsData.numDevices}
            onValueChange={(value) => setAgentsData({ ...agentsData, numDevices: value })}
          >
            <SelectTrigger className="w-full border border-gray-300 rounded-md">
              <SelectValue placeholder="How many devices do you have?" />
            </SelectTrigger>
            <SelectContent>
              {Array.from({ length: 100 }, (_, i) => i + 1).map((num) => (
                <SelectItem key={num} value={num.toString()}>
                  {num}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
        <div className="mb-4">
          <label className="block mb-2 text-sm font-medium text-gray-700">Category</label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mt-2"> {/* Responsive grid for categories */}
            {categories.map((cat) => (
              <Card
                key={"test"}
                onClick={() => setAgentsData({ ...agentsData, category: cat.name })}
                className={`cursor-pointer transition-shadow hover:shadow-lg ${agentsData.category === cat.name ? "border-2 border-blue-600 shadow-md" : "shadow-md"}`}
              >
                <CardContent className="p-5 flex items-start gap-4">
                  <img src={img} alt={cat.name} className="w-8 h-8" />
                  <div className="flex flex-col">
                    <strong className="text-gray-900 text-base">{cat.name}</strong>
                    <p className="text-sm text-gray-600 line-clamp-3">{cat.description}</p>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
        <Button
          onClick={handleSubmit}
          type="submit"
          disabled={canSubmit}
          className="mt-4 bg-gray-900 text-white hover:bg-gray-700 disabled:bg-gray-400 disabled:cursor-not-allowed w-full flex items-center justify-center gap-2"
        >
          <Send className="w-4 h-4" />
          {isLoading ? "Generating Report..." : "Generate Report"}
        </Button>
      </form >

      {
        responses.length > 0 && (
          <div className="mt-5">
            <h3 className="text-xl font-semibold mb-4 text-gray-900">Agent Responses</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4"> {/* Responsive grid for responses */}
              {responses.map((agent, index) => (
                <Card key={agent.id} className="shadow-md">
                  <CardHeader className="bg-green-50 p-4 flex items-center gap-4">
                    <img src={agent.icon} alt={`${agent.agent} icon`} className="w-8 h-8" />
                    <CardTitle className="text-lg text-gray-900">{agent.agent} working...</CardTitle>
                  </CardHeader>
                  <CardContent className="p-5">
                    <Progress value={agent.progress} className="mb-4" /> {/* Always visible as in screenshot */}
                    <p className="text-sm text-gray-600">
                      <span className="block">
                        {agent.response}
                      </span>
                    </p>
                  </CardContent>
                </Card>
              ))}
            </div>
            {/* <div className="mt-6">
              <h3 className="text-xl font-semibold mb-4 text-gray-900">Response Analysis</h3>
              <Card className="shadow-md">
                <CardContent className="p-5">
                  <Chart type="bar" data={chartData} options={chartOptions} />
                </CardContent>
              </Card>
            </div> */}
          </div>
        )
      }
    </div >
  );
}
