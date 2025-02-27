import Contact from "@/pages/Contact";
import Home from "@/pages/Home";
import PageNotFound from "@/pages/PageNotFound";
import { Routes, Route } from "react-router-dom";

const Routing: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="contact" element={<Contact />} />
      <Route path="*" element={<PageNotFound />} />
    </Routes>
  );
};

export default Routing;
