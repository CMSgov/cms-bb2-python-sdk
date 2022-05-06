import { Button } from "@cmsgov/design-system";
import axios from "axios";
import chart from "../images/who-charted.png";
import { SettingsType } from "../types/settings";
import { useState } from "react";

export default function PatientData() {
  const [header] = useState("Add your Medicare Prescription Drug data");
  const [settingsState] = useState<SettingsType>({
    pkce: true,
    version: "v2",
    env: "sandbox",
  });
  async function goAuthorize() {
    const authUrlResponse = await axios.get(`/api/authorize/authurl`, {
      params: settingsState,
    });
    window.location.href = authUrlResponse.data || "/";
  }

  /* DEVELOPER NOTES:
   * Here we are hard coding the users information for the sake of saving time
   * you would display user information that you have stored in whatever persistence layer/mechanism
   * your application is using
   */
  return (
    <div>
      <h3>Medicare Prescription Drug Records</h3>
      <div className="ds-u-display--flex ds-u-flex-direction--row ds-u-align-items--start">
        <img src={chart} alt="Chart icon" className="" />
        <p className="ds-u-padding-x--2 ds-u-margin-top--0">
          John, you can now allow Springfield General Hospital access to your
          Medicare prescription drug records!
        </p>
      </div>
      <div className="ds-u-margin-top--2 ds-u-border-top--2">
        <div>
          <h4>{header}</h4>
        </div>
        <Button variation="primary" onClick={goAuthorize}>
          Authorize
        </Button>
      </div>
    </div>
  );
}
