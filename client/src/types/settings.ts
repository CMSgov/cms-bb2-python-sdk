export type SettingsType = {
  env: "sandbox" | "local" | "production";
  version: "v1" | "v2";
  pkce: boolean;
};
