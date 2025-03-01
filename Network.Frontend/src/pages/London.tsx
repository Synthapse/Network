import graph from '../assets/graph.png'
//import htmlContent from "./london_broadband_map.html"; // Webpack or Vite loads it as a string


const London = () => {
  return (

    <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
      <div className="flex max-w-[980px] flex-col items-start gap-2">
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          Proof of Concept with London <span className="text-green-400">(Smart city)</span>
        </h1>


        <p className="text-lg text-muted-foreground">
          We focused on London for PoC - cause it’s the most developed smart city with the network infrastracture.
          And from that point for development is great for <a className="text-blue-500" href="https://sharingcities.eu/wp-content/uploads/sites/6/2022/07/D5-01-One-replication-strategy.pdf">One Replication Strategy</a> The London Smart City Optimization project enhances urban infrastructure using AI, IoT, and cybersecurity.
          The focus areas include This initiative ensures London remains a sustainable, secure, and efficient smart city.
        </p>


        <img src={graph} />

        <hr />

        <h2 className="text-2xl font-extrabold leading-tight tracking-tighter md:text-3l">
          Data (Google Colabs):
        </h2>

        <a target="_blank" className="text-blue-500" href="https://colab.research.google.com/drive/1DmcUJBjGgn1Cev4aoCKOWrz7uLFO8et5?usp=sharing">
          - [NETWORK] Smart city network performance by predicting network usage trends (2021)
        </a>

        <a target="_blank" className="text-blue-500" href="https://colab.research.google.com/drive/1qV8barEi_0nftJDi9T6YXjHBYYDbPV6F?usp=sharing">
          - [NETWORK] OFCOM Fixed Broadband (2014)
        </a>

        <a target="_blank" className="text-blue-500" href="https://colab.research.google.com/drive/1xI-6ifDUpONUS5BmUInk7Lq_UCLbvCdF?usp=sharing">
          - [ENERGY] Smart Meters 30min intervals / Granite prediction
        </a>

        <hr />

        <h2 className="text-2xl font-extrabold leading-tight tracking-tighter md:text-3l">
          Results
        </h2>

        <hr />

        <p className="text-lg text-muted-foreground">
          Map of London network usage - based on 2021 data - separated via districts
        </p>

        <iframe src="/london_broadband_map.html" width="100%" height="600px" title="Embedded HTML"></iframe>
      </div>
    </section >
  )
}

export default London