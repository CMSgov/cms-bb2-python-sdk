import avatar from "../images/patient.png";

export default function Patient() {
  /* DEVELOPER NOTES:
   * Here we are hard coding the users information for the sake of saving time
   * you would display user information that you have stored in whatever persistence layer/mechanism
   * your application is using
   */
  return (
    <div>
      <h3>Clinic records</h3>
      <div className="ds-u-display--flex ds-u-flex-direction--row ds-u-align-items--center">
        <img src={avatar} alt="Profile avatar" />
        <ul>
          <li>John Doe</li>
          <li>Springfield General Hospital</li>
          <li>Dr. Hibbert</li>
        </ul>
      </div>
    </div>
  );
}
