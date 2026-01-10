import { BrowserRouter, Routes, Route } from "react-router-dom";
import { SignedIn, SignedOut, SignIn } from "@clerk/clerk-react";

import Home from "./pages/Home";
import About from "./pages/About";
import Header from "./components/Header";

function App() {
  return (
    <BrowserRouter>
      <Header />

      {/* If user is NOT logged in → show login */}
      {/* so u our code will work fine wo below routing and path, here we ar just giving an Endpoint of clerk*/}
      <SignedOut>
        <SignIn routing="path" path="/sign-in" />
      </SignedOut>

      {/* If user IS logged in → allow app access */}
      <SignedIn>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </SignedIn>
    </BrowserRouter>
  );
}

export default App;








