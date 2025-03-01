
import { cn } from "@/lib/utils";
import logo from "./logo.png"
import Image from "next/image";

export function MainNav() {
  return (
    <div className="flex gap-6 md:gap-10">
      <a href="/" className="flex items-center space-x-2">

        <Image style = {{width: '42px'}} src={logo} alt="Image " />

      </a>
        <nav className="flex gap-6">
       
                <a
                  key={index}
                  href={item.href}
                  className={cn(
                    "flex items-center text-sm font-medium text-muted-foreground",
                    item.disabled && "cursor-not-allowed opacity-80"
                  )}
                >
                </a>
              
        </nav>
    </div>
  );
}
