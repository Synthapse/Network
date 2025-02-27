import { siteConfig } from "@/config/site";
import { buttonVariants } from "@/components/ui/button";
import iot from "./iot.png";
import { Icons } from "./icons";
import { signInWithPopup } from "firebase/auth";
import { auth, googleProvider } from "@/firebase";

export default function HomePage() {


  const signInWithGoogle = async (event: React.MouseEvent<HTMLButtonElement>) => {
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

        <a href="" onClick={(e) => signInWithGoogle(e)} className={buttonVariants()}>
          <Icons.google style={{ marginRight: 10 }} className="h-5 w-5 fill-current" /> Sign up with Google
        </a>
        <a
          href={siteConfig.links.github}
          className={buttonVariants({ variant: "outline" })}
        >
          Contact
        </a>
      </div>
      <img src={iot} />
    </section>
  );
}
