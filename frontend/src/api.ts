const API_BASE: string =
  import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";
const TOKEN_KEY = "promptshield_token";

export interface SecuritySummary {
  total_events: number;
  blocked_events: number;
  allowed_events: number;
  average_risk: number;
}

export function getToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY);
}

export function logout(): void {
  sessionStorage.removeItem(TOKEN_KEY);
}

export async function login(email: string, password: string): Promise<void> {
  // The backend login endpoint expects form data, not JSON.
  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", password);

  const response = await fetch(`${API_BASE}/api/v1/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });

  if (response.status === 401) {
    throw new Error("Invalid email or password");
  }

  if (response.status === 429) {
    throw new Error("Too many failed attempts. Please wait and try again.");
  }

  if (!response.ok) {
    throw new Error("Login service unavailable. Please try again.");
  }

  const data = (await response.json()) as { access_token: string };
  sessionStorage.setItem(TOKEN_KEY, data.access_token);
}

export async function authFetch(
  path: string,
  options: RequestInit = {},
): Promise<Response> {
  const token = getToken();
  const headers = new Headers(options.headers);

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  // Token expired or invalid: remove it so the app returns to the login page.
  if (response.status === 401) {
    logout();
  }

  return response;
}

export async function getSecuritySummary(): Promise<SecuritySummary> {
  const response = await authFetch("/api/v1/analytics/summary");

  if (!response.ok) {
    throw new Error("Unable to load security analytics");
  }

  return response.json() as Promise<SecuritySummary>;
}

export interface CurrentUser {
  user_id: number;
  email: string;
  role: "Admin" | "Analyst" | "Viewer";
}

export async function getCurrentUser(): Promise<CurrentUser | null> {
  const response = await authFetch("/api/v1/auth/me");

  if (!response.ok) {
    return null;
  }

  return response.json() as Promise<CurrentUser>;
}