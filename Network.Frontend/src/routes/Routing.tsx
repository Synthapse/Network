import Contact from "@/pages/Contact";
import Home from "@/pages/Home";
import London from "@/pages/London";
import Agents from "@/pages/Agents";
import { HashRouter, Routes, Route } from "react-router-dom";

const Routing: React.FC = () => {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="contact" element={<Contact />} />
        <Route path="london" element={<London />} />
        <Route path="agents" element={<Agents />} />
        {/* <Route path="*" element={<PageNotFound />} /> */}
      </Routes>
    </HashRouter>
  );
};

export default Routing; x
