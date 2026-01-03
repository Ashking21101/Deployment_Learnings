import { BrowserRouter, Routes, Route } from "react-router-dom";
// BrowserRouter: enables client-side routing
// Routes: container for all route definitions
// Route: maps a URL path to a component

import Home from "./pages/Home";     // Page that talks to backend
import About from "./pages/About";   // Static page (no backend call)
import Header from "./components/Header"; // Common navigation bar

function App() {
  return (
    <BrowserRouter>
      {/* Header is OUTSIDE Routes, so it appears on every page */}
      <Header />

      <Routes>
        {/* When URL is "/", render Home component */}
        <Route path="/" element={<Home />} />

        {/* When URL is "/about", render About component */}
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
