## 1. Network Protocols

Sending Packets:

- not need TLS


**RINA** (Recursive InterNetwork Architecture)


-> more than 1000 times faster than TCP/IP 
-> not need TLS

Data-Link Layer (DLC): Responsible for node-to-node communication, error correction, and addressing within a single network segment.
Network Layer (NL): Handles addressing and routing between different network segments.
Transport Layer (TL): Manages end-to-end communication, flow control, and reliability.
Application Layer: Implements higher-level protocols.


While you can't run Linux-specific modules on macOS, you can still develop and experiment with networking protocols
and simulations in macOS if they don’t require kernel-level interaction. 

https://irati.github.io/stack/
https://github.com/IRATI/stack/wiki/Software-architecture-overview
https://github.com/IRATI/stack/wiki/Tutorials
https://pouzinsociety.org/iot-or-coping-with-the-tribble-syndrome/

TCP/IP and RINA:
Protocols: Internet – 15; RINA – 3
Non-security mechanisms: Internet – 89; RINA – 15
Security mechanisms: Internet – 28; RINA – 7

https://www.martingeddes.com/think-tank/network-architecture-research-tcp-ip-vs-rina/

# NS-3

https://www.nsnam.com/2024/08/ns3-installation-in-mac-m1.html

`
brew install cmake ninja gnuplot ccache 

brew install wget
wget https://www.nsnam.org/releases/ns-allinone-3.42.tar.bz2

tar jxvf ns-allinone-3.42.tar.bz2
cd ns-allinone-3.42/
./build.py --enable-examples --enable-tests
`


RINASim

Application Layer (top-most layer for handling user data)
Transport Layer (for data transfer)
Link Layer (handling actual physical transmission)

Recursion instead fixed layers. 

- IRATI (for real-world testing)
- RINASim in OMNeT++ (for simulations)


OMNeT++ uses Bison to parse its NED (Network Description) files
Bison then generates a C parser to process this rule.
require Bison >3.0


`arch -arm64 brew install bison`

`echo 'export PATH="/usr/local/opt/bison/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc`



`cd omnetpp-6.0.1`


`
source setenv
./configure
make -j$(nproc)
`

OMNeT++ supports numpy (>=1.18.0, <2.0.0)
downgrade numpy: pip install "numpy<2.0.0,>=1.18.0"

depends on arch

arm64 installation
arch -arm64 pip install "numpy>=1.18.0,<2.0.0"

x86_64 installation
arch -x86_64 pip install numpy

brew install cmake


on Mac: 
`make -j$(sysctl -n hw.ncpu)`

NetworkX with OMNeT++





**NDN** (Named Data Networking)

IoT, content heavy

Not Ip Addresses. 

1. Simulation Approach 
   a. NetworkX
   b. Mininet 
   c. NS-3
   d OMNeT++




### TCP Alternatives:

- **HOMA/QUIC** ([Quicly](https://github.com/h2o/quicly/))
-   Future internet architectures (RINA)
-   Future decentralized networking (NDN)
- **DCCP** (Datagram Congestion Control Protocol) - Video Streaming, Gaming
- **SCTP** (Stream Control Transmission Protocol) - 5G

---