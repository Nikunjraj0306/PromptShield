
const API_BASE = "http://127.0.0.1:8000";

export interface SecuritySummary {
  total_events: number;
  blocked_events: number;
  allowed_events: number;
  average_risk: number;
}

export async function getSecuritySummary(): Promise<SecuritySummary> {
  const response = await fetch(
    `${API_BASE}/api/v1/analytics/summary`
  );

  if (!response.ok) {
    throw new Error("Unable to load security analytics");
  }

  return response.json() as Promise<SecuritySummary>;
}
