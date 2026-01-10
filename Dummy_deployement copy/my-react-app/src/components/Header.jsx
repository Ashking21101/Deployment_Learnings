import { Link } from "react-router-dom";
import {
  SignedIn,
  SignedOut,
  SignInButton,
  UserButton,
} from "@clerk/clerk-react";

function Header() {
  return (
    <nav style={{ padding: "1rem", background: "#222", color: "#fff" }}>
      <Link to="/" style={{ color: "#fff", marginRight: "1rem" }}>
        Home
      </Link>

      <Link to="/about" style={{ color: "#fff", marginRight: "1rem" }}>
        About
      </Link>

      {/* When user is signed OUT */}
      <SignedOut>
        <SignInButton />
      </SignedOut>

      {/* When user is signed IN */}
      <SignedIn>
        <UserButton />
      </SignedIn>
    </nav>
  );
}

export default Header;




