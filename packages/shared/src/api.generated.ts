// Generated from docs/api/openapi.json. Do not edit by hand.
export type DisplayDefaults = {
  "currency": string;
  "locale": string;
  "timezone": string;
};

export type HealthChecks = {
  "database": boolean;
  "migrations": boolean;
};

export type PublicMetadata = {
  "defaults": DisplayDefaults;
  "name": string;
  "phase": number;
  "version": string;
};

export type Readiness = {
  "checks": HealthChecks;
  "status": "ok" | "unavailable";
};
