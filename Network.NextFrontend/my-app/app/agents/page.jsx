"use client";

import { useState, useEffect, useRef } from "react";
import Image from "next/image";
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
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import img from "../assets/agent1.png";
import { Send } from "lucide-react";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function Home() {
  const [title, setTitle] = useState("");
  const [numDevices, setNumDevices] = useState("");
  const [category, setCategory] = useState("");
  const [responses, setResponses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title || !numDevices || !category) return;

    setIsLoading(true);
    setResponses([]); // Reset responses

    const query = `Provide a detailed response for ${category} infrastructure with title "${title}" and ${numDevices} devices. Focus on your area of expertise.`;

    try {
      // Initialize responses with progress tracking (set to 100% since we want progress bars visible)
      const initialResponses = [
        { agent: "Network Design", response: "Processing...", progress: 100, icon: img },
        { agent: "Energy Management", response: "Processing...", progress: 100, icon: img },
        { agent: "Cyber Security", response: "Processing...", progress: 100, icon: img },
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

      const res = await fetch("/api/grok", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [{ role: "user", content: query }],
        }),
      });

      const data = await res.json();
      clearInterval(interval);

      if (data.error) {
        setResponses(initialResponses.map((r) => ({ ...r, response: "Error fetching response", progress: 100 })));
      } else {
        const updatedResponses = data.replies.map((reply, index) => ({
          agent: initialResponses[index].agent,
          response: reply.reply,
          progress: 100, // Keep progress at 100% as per screenshot
          icon: initialResponses[index].icon,
        }));
        setResponses(updatedResponses);
      }
    } catch (error) {
      setResponses(initialResponses.map((r) => ({ ...r, response: "Error fetching response", progress: 100 })));
    } finally {
      setIsLoading(false);
    }
  };

  // Calculate average response length for the graph
  const calculateAverageResponseLength = () => {
    if (responses.length === 0) return 0;
    const totalLength = responses.reduce((sum, r) => sum + (r.response?.length || 0), 0);
    return totalLength / responses.length;
  };

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

  return (
    <div className="container mx-auto p-5 max-w-4xl"> {/* Increased max width to make it larger */}
      <h1 className="text-2xl font-bold mb-5 text-gray-900">Describe Your IoT Infrastructure</h1>
      <form onSubmit={handleSubmit} className="mb-5 p-5 bg-white rounded-lg shadow-md">
        <div className="mb-4">
          <label className="block mb-2 text-sm font-medium text-gray-700">What's the title and your IoT infrastructure structure?</label>
          <Textarea
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Enter title and description"
            className="w-full border border-gray-300 rounded-md"
          />
        </div>
        <div className="mb-4">
          <label className="block mb-2 text-sm font-medium text-gray-700">Number of devices</label>
          <Select
            value={numDevices}
            onValueChange={(value) => setNumDevices(value)}
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
                key={cat.name}
                onClick={() => setCategory(cat.name)}
                className={`cursor-pointer transition-shadow hover:shadow-lg ${category === cat.name ? "border-2 border-blue-600 shadow-md" : "shadow-md"}`}
              >
                <CardContent className="p-5 flex items-start gap-4">
                  <Image src={img} alt={cat.name} className="w-8 h-8" />
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
          type="submit"
          disabled={isLoading || !title || !numDevices || !category}
          className="mt-4 bg-gray-900 text-white hover:bg-gray-700 disabled:bg-gray-400 disabled:cursor-not-allowed w-full flex items-center justify-center gap-2"
        >
          <Send className="w-4 h-4" />
          {isLoading ? "Generating Report..." : "Generate Report"}
        </Button>
      </form>

      {responses.length > 0 && (
        <div className="mt-5">
          <h3 className="text-xl font-semibold mb-4 text-gray-900">Agent Responses</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4"> {/* Responsive grid for responses */}
            {responses.map((agent, index) => (
              <Card key={agent.agent} className="shadow-md">
                <CardHeader className="bg-green-50 p-4 flex items-center gap-4">
                  <Image src={agent.icon} alt={`${agent.agent} icon`} className="w-8 h-8" />
                  <CardTitle className="text-lg text-gray-900">{agent.agent} working...</CardTitle>
                </CardHeader>
                <CardContent className="p-5">
                  <Progress value={agent.progress} className="mb-4" /> {/* Always visible as in screenshot */}
                  <p className="text-sm text-gray-600">
                    {agent.response.split("\n").map((line, i) => (
                      <span key={i} className="block">
                        {line}
                      </span>
                    ))}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
          <div className="mt-6">
            <h3 className="text-xl font-semibold mb-4 text-gray-900">Response Analysis</h3>
            <Card className="shadow-md">
              <CardContent className="p-5">
                <Chart type="bar" data={chartData} options={chartOptions} />
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
}