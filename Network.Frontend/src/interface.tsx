// Sample Data
const systemRequest: ISystemRequest = {
  infrastructureDescription: "My infrastracture have garden and need provide water there and soil for growing",
  infrastractureCategory: "Smart farming",
  networkAgent: {
    agentId: "network1",
    numberOfNodes: 5, // In Interface client give how many device he have
    recommendation: "AI response",
  },
  energyAgent: {
    agentId: "energy1",
    recommendation: "AI response",
  },
  cyberSecurityAgent: {
    agentId: "cyber1",
    recommendation: "AI response",
  },
};

interface ISystemRequest {
  infrastructureDescription: string;
  infrastractureCategory: 'Smart farming' | 'Healtcare' | 'Smart city' | 'Industrial IoT';
  networkAgent: INetworkAgentRequest;
  energyAgent: IEnergyAgentRequest;
  cyberSecurityAgent: ICyberSecurityAgentRequest;
}


interface IAgentRequest {
  agentId: string;
  // 28.02.2025 -> we can extend by action by right now it's too much
  // action: "configureNetwork" | "loadBalance" | "scaleNetwork";

  action?: string;
  recommendation: string;
}


interface INetworkAgentRequest extends IAgentRequest {
  numberOfNodes: number;
}

interface IEnergyAgentRequest extends IAgentRequest {
}

interface ICyberSecurityAgentRequest extends IAgentRequest {
}