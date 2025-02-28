import { buttonVariants } from "@/components/ui/button"

const Contact = () => {
  return (
    <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
      <div className="flex max-w-[980px] flex-col items-start gap-2">
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          Contact
        </h1>
        <p className="max-w-[700px] text-lg text-muted-foreground">
          Muhammad Qasim
        </p>
        <p className="max-w-[700px] text-lg text-muted-foreground">
          Piotr Żak
        </p>
        <p className="max-w-[700px] text-lg text-muted-foreground">
          Malik Zubair
        </p>
        <p className="max-w-[700px] text-lg text-muted-foreground">
          Norah Alsuqayhi
        </p>
        <button className={buttonVariants()} onClick={() => window.location.href = "mailto:synthapseai@gmail.com"}>
          Send mail
        </button>
      </div>
    </section>
  )
}

export default Contact