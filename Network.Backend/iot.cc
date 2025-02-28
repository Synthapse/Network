/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/csma-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/sixlowpan-helper.h"
#include "ns3/lr-wpan-module.h"
#include "ns3/ssid.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/wifi-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/netanim-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("ThirdScriptExample");

int
main(int argc, char* argv[])
{
    // Enable Logging
    LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO);
    LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_INFO);

    // Create Nodes: 1 AP (Access Point) + 2 Stations (STAs)
    NodeContainer wifiStaNodes, wifiApNode;
    wifiStaNodes.Create(2);
    wifiApNode.Create(1);

    // Setup WiFi Channel
    YansWifiChannelHelper channel;
    channel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel");
    channel.AddPropagationLoss("ns3::LogDistancePropagationLossModel");

    YansWifiPhyHelper phy;
    phy.SetChannel(channel.Create());

    // Configure WiFi
    WifiHelper wifi;
    wifi.SetStandard(WIFI_STANDARD_80211n);
    WifiMacHelper mac;

    // Setup STA (Station) devices
    Ssid ssid = Ssid("ns3-wifi");
    mac.SetType("ns3::StaWifiMac", "Ssid", SsidValue(ssid), "ActiveProbing", BooleanValue(false));
    NetDeviceContainer staDevices = wifi.Install(phy, mac, wifiStaNodes);

    // Setup AP (Access Point) device
    mac.SetType("ns3::ApWifiMac", "Ssid", SsidValue(ssid));
    NetDeviceContainer apDevice = wifi.Install(phy, mac, wifiApNode);

    // Setup Mobility Model
    MobilityHelper mobility;
    mobility.SetPositionAllocator("ns3::GridPositionAllocator",
                                  "MinX", DoubleValue(0.0),
                                  "MinY", DoubleValue(0.0),
                                  "DeltaX", DoubleValue(5.0),
                                  "DeltaY", DoubleValue(5.0),
                                  "GridWidth", UintegerValue(3),
                                  "LayoutType", StringValue("RowFirst"));
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");

    mobility.Install(wifiStaNodes);
    mobility.Install(wifiApNode);

    // Install Internet Stack
    InternetStackHelper stack;
    stack.Install(wifiStaNodes);
    stack.Install(wifiApNode);

    // Assign IP Addresses
    Ipv4AddressHelper address;
    address.SetBase("192.168.1.0", "255.255.255.0");
    Ipv4InterfaceContainer staInterfaces = address.Assign(staDevices);
    Ipv4InterfaceContainer apInterface = address.Assign(apDevice);

    // Setup UDP Echo Server on AP
    UdpEchoServerHelper echoServer(9);
    ApplicationContainer serverApp = echoServer.Install(wifiApNode.Get(0));
    serverApp.Start(Seconds(1.0));
    serverApp.Stop(Seconds(10.0));

    // Setup UDP Echo Client on Station 1
    UdpEchoClientHelper echoClient(apInterface.GetAddress(0), 9);
    echoClient.SetAttribute("MaxPackets", UintegerValue(5));
    echoClient.SetAttribute("Interval", TimeValue(Seconds(1.0)));
    echoClient.SetAttribute("PacketSize", UintegerValue(1024));

    ApplicationContainer clientApp = echoClient.Install(wifiStaNodes.Get(0));
    clientApp.Start(Seconds(2.0));
    clientApp.Stop(Seconds(10.0));

    // Enable NetAnim
    AnimationInterface anim("wifi_netanim.xml");
    anim.SetConstantPosition(wifiStaNodes.Get(0), 10.0, 10.0);
    anim.SetConstantPosition(wifiStaNodes.Get(1), 20.0, 20.0);
    anim.SetConstantPosition(wifiApNode.Get(0), 15.0, 15.0);

    // Run Simulation
    Simulator::Stop(Seconds(10.0));
    Simulator::Run();
    Simulator::Destroy();

    return 0;


//
//    NodeContainer p2pNodes;
//    p2pNodes.Create(2);
//
//    PointToPointHelper pointToPoint;
//    pointToPoint.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
//    pointToPoint.SetChannelAttribute("Delay", StringValue("2ms"));
//
//    NetDeviceContainer p2pDevices;
//    p2pDevices = pointToPoint.Install(p2pNodes);
//
//    NodeContainer csmaNodes;
//    csmaNodes.Add(p2pNodes.Get(1));
//    csmaNodes.Create(nCsma);
//
//    CsmaHelper csma;
//    csma.SetChannelAttribute("DataRate", StringValue("100Mbps"));
//    csma.SetChannelAttribute("Delay", TimeValue(NanoSeconds(6560)));
//
//    NetDeviceContainer csmaDevices;
//    csmaDevices = csma.Install(csmaNodes);
//
//    NodeContainer wifiStaNodes;
//    wifiStaNodes.Create(nWifi);
//    NodeContainer wifiApNode = p2pNodes.Get(0);
//
//    YansWifiChannelHelper channel = YansWifiChannelHelper::Default();
//    YansWifiPhyHelper phy;
//    phy.SetChannel(channel.Create());
//
//    WifiMacHelper mac;
//    Ssid ssid = Ssid("ns-3-ssid");
//
//    WifiHelper wifi;
//
//    NetDeviceContainer staDevices;
//    mac.SetType("ns3::StaWifiMac", "Ssid", SsidValue(ssid), "ActiveProbing", BooleanValue(false));
//    staDevices = wifi.Install(phy, mac, wifiStaNodes);
//
//    NetDeviceContainer apDevices;
//    mac.SetType("ns3::ApWifiMac", "Ssid", SsidValue(ssid));
//    apDevices = wifi.Install(phy, mac, wifiApNode);
//
//    MobilityHelper mobility;
//
//    mobility.SetPositionAllocator("ns3::GridPositionAllocator",
//                                  "MinX",
//                                  DoubleValue(0.0),
//                                  "MinY",
//                                  DoubleValue(0.0),
//                                  "DeltaX",
//                                  DoubleValue(5.0),
//                                  "DeltaY",
//                                  DoubleValue(10.0),
//                                  "GridWidth",
//                                  UintegerValue(3),
//                                  "LayoutType",
//                                  StringValue("RowFirst"));
//
//    mobility.SetMobilityModel("ns3::RandomWalk2dMobilityModel",
//                              "Bounds",
//                              RectangleValue(Rectangle(-50, 50, -50, 50)));
//    mobility.Install(wifiStaNodes);
//
//    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
//    mobility.Install(wifiApNode);
//
//    InternetStackHelper stack;
//    stack.Install(csmaNodes);
//    stack.Install(wifiApNode);
//    stack.Install(wifiStaNodes);
//
//    Ipv4AddressHelper address;
//
//    address.SetBase("10.1.1.0", "255.255.255.0");
//    Ipv4InterfaceContainer p2pInterfaces;
//    p2pInterfaces = address.Assign(p2pDevices);
//
//    address.SetBase("10.1.2.0", "255.255.255.0");
//    Ipv4InterfaceContainer csmaInterfaces;
//    csmaInterfaces = address.Assign(csmaDevices);
//
//    address.SetBase("10.1.3.0", "255.255.255.0");
//    address.Assign(staDevices);
//    address.Assign(apDevices);
//
//    UdpEchoServerHelper echoServer(9);
//
//    ApplicationContainer serverApps = echoServer.Install(csmaNodes.Get(nCsma));
//    serverApps.Start(Seconds(1.0));
//    serverApps.Stop(Seconds(10.0));
//
//    UdpEchoClientHelper echoClient(csmaInterfaces.GetAddress(nCsma), 9);
//    echoClient.SetAttribute("MaxPackets", UintegerValue(1));
//    echoClient.SetAttribute("Interval", TimeValue(Seconds(1.0)));
//    echoClient.SetAttribute("PacketSize", UintegerValue(1024));
//
//    ApplicationContainer clientApps = echoClient.Install(wifiStaNodes.Get(nWifi - 1));
//    clientApps.Start(Seconds(2.0));
//    clientApps.Stop(Seconds(10.0));
//
//    Ipv4GlobalRoutingHelper::PopulateRoutingTables();
//
//    Simulator::Stop(Seconds(10.0));
//
//    if (tracing)
//    {
//        phy.SetPcapDataLinkType(WifiPhyHelper::DLT_IEEE802_11_RADIO);
//        pointToPoint.EnablePcapAll("third");
//        phy.EnablePcap("third", apDevices.Get(0));
//        csma.EnablePcap("third", csmaDevices.Get(0), true);
//    }
//
//    Simulator::Run();
//    Simulator::Destroy();
//    return 0;
}
