import PropTypes from "prop-types";
import { Link } from "react-router-dom";

function Header(props) {
  const headerStyles = {
    backgroundColor: props.bgColor,
    color: props.textColor,
  };
  return (
    <header style={headerStyles}>
      <div className={"container"}>
        <Link to={"/"} style={{ textDecoration: "none", color: "#ff6a95" }}>
          <h1>{props.text}</h1>
        </Link>
      </div>
    </header>
  );
}

Header.defaultProps = {
  text: "FeedbackItem UI",
  bgColor: "rgba(0,0,0,0.4)",
  textColor: "#ff6a95",
};

Header.propTypes = {
  text: PropTypes.string,
  bgColor: PropTypes.string,
  textColor: PropTypes.string,
};

export default Header;
