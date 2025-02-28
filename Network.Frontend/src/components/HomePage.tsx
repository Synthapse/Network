import { siteConfig } from "@/config/site";
import { buttonVariants } from "@/components/ui/button";
import iot from "./iot.png";
import AgentsImg from "../assets/agent1.png";
import NetworkAgents from "../assets/agent2.png";
import ImgNetwork from "../assets/image 61.png";
import ImgOptimizing from "../assets/image 62.png";
import img from "../assets/image 590.png";
import img2 from "../assets/image 591.png";
import img3 from "../assets/image 592.png";
import { Icons } from "./icons";
import { signInWithPopup } from "firebase/auth";
import { auth, googleProvider } from "@/firebase";

export default function HomePage() {

  const signInWithGoogle = async (event: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => {
    try {
      event.preventDefault();
      const credentials = await signInWithPopup(auth, googleProvider);
      console.log(credentials)
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
      <div className="flex max-w-[980px] flex-col items-start gap-2">
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          Transforming IoT infrastructures <br className="hidden sm:inline" />
          with Swarm AI
        </h1>
        <p className="max-w-[700px] text-lg text-muted-foreground">
          Unlocking technology potential with network AI for optimize metrics.
        </p>
      </div>
      <div className="flex gap-4">
        <a
          href=""
          onClick={(e) => signInWithGoogle(e)}
          className={buttonVariants()}
        >
          <Icons.google
            style={{ marginRight: 10 }}
            className="h-5 w-5 fill-current"
          />{" "}
          Sign up with Google
        </a>
        <a
          href={siteConfig.links.github}
          className={buttonVariants({ variant: "outline" })}
        >
          Contact
        </a>
      </div>
      <img src={iot} />
      <div className="flex flex-wrap md:flex-nowrap justify-between items-center mt-9 gap-4">
        <div className="w-full md:w-1/2">
          <div className="flex flex-col md:flex-row items-center">
            <img
              src={ImgNetwork}
              alt="Optimizing Network"
              className="w-20 md:w-28"
            />
            <p className="mx-5 text-xl text-center md:text-left">
              Optimizing <span className="text-green-400">network</span> and
              data flow with Swarm AI and Network AI for improved performance.
            </p>
          </div>
        </div>

        <div className="w-full md:w-1/2">
          <div className="flex flex-col md:flex-row items-center">
            <img
              src={ImgOptimizing}
              alt="Optimizing Energy"
              className="w-20 md:w-28"
            />
            <p className="mx-5 text-xl text-center md:text-left">
              Reducing <span className="text-green-400">energy</span> usage and
              costs through AI-driven optimization in IoT systems.
            </p>
          </div>
        </div>
      </div>

      <div className="mt-10 p-5">
        <div className="flex flex-wrap justify-center md:justify-between items-center gap-4 mt-10">
          <img src={AgentsImg} alt="Agent" />
          <img src={NetworkAgents} alt="Network" />
        </div>
      </div>

      <div className="mt-10 text-center md:text-left">
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          How it works?
        </h1>

        <div className="mt-7">
          <p className="mb-2 text-xl">
            This process takes 1-3 business days before signing an agreement.
          </p>
          <p className="mb-2 text-xl">
            Instead of 3-6 weeks of specification and gathering requirements.
          </p>
          <p className="mb-2 text-xl">
            You get a full specification for free & decide whether to continue
            with implementation and pilot deployment.
          </p>
        </div>

        <hr className="border-2 bg-zinc-950 mt-5" />
        <div className="mt-16">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 text-center md:text-left items-center">
            <div>
              <h2 className="text-xl font-bold">01 Research</h2>
              <ul className="text-blue-500">
                <li>Infrastructure assessment</li>
                <li>AI feasibility study</li>
                <li>Efficiency & security analysis</li>
              </ul>
            </div>

            <div>
              <h2 className="text-xl font-bold">02 Multi-agent system</h2>
              <ul className="text-blue-500">
                <li>Smart automation</li>
                <li>Four network of AI Agents</li>
                <li>Consultation & Planning</li>
              </ul>
            </div>

            <div>
              <h2 className="text-xl font-bold">03 Supervisor agent</h2>
              <ul className="text-blue-500">
                <li>Agent input critique</li>
                <li>Generate weak-points</li>
                <li>Verify potential</li>
              </ul>
            </div>

            <div>
              <h2 className="text-xl font-bold">04 Contract proposal</h2>
              <ul className="text-blue-500">
                <li>Prototype implementation</li>
                <li>Pilot deployment</li>
                <li>Ongoing optimization</li>
              </ul>
            </div>
          </div>
        </div>
        {/* SDG Icons Section */}

        <div className="flex justify-center gap-6 items-center mt-20">
          <img src={img} alt="Sustainable Cities" />
          <img src={img2} alt="Clean Energy" />
          <img src={img3} alt="Innovation & Infrastructure" />
        </div>
      </div>

    </section>
  );
}
