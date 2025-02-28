import Contact from "@/pages/Contact";
import Home from "@/pages/Home";
import London from "@/pages/London";
import PageNotFound from "@/pages/PageNotFound";
import { Routes, Route } from "react-router-dom";

const Routing: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="contact" element={<Contact />} />
      <Route path="london" element={<London />} />
      <Route path="*" element={<PageNotFound />} />
    </Routes>
  );
};

export default Routing;
