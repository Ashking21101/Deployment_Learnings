import { Link } from "react-router-dom";

function Header() {
  return (
    <nav style={{ padding: "1rem", background: "#222" }}>
      <Link to="/" style={{ color: "#fff", marginRight: "1rem" }}>
        Home
      </Link>
      <Link to="/about" style={{ color: "#fff" }}>
        About
      </Link>
    </nav>
  );
}

export default Header;
