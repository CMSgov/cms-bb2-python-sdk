import { Badge } from "@cmsgov/design-system";
import { Link as RouterLink } from "react-router-dom";

export default function Header() {
  return (
    <header className="ds-u-padding--3 ds-u-sm-padding--6 ds-u-display--block ds-u-fill--primary-darkest">
      <h1 className="ds-u-margin--0 ds-u-color--white ds-u-font-size--display ds-u-text-align--center">
        <RouterLink to="/" style={{ textDecoration: "none", color: "inherit" }}>
          Blue Button 2.0 Sample App
        </RouterLink>
      </h1>
      <div className="ds-u-text-align--center">
        <Badge variation="info" size="big">
          Medicare Prescription Drug Claims Data
        </Badge>
      </div>
    </header>
  );
}
