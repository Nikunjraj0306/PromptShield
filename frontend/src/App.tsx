
import { useCallback, useEffect, useState } from "react";
import "./App.css";
import Login from "./Login";
import { authFetch, getCurrentUser, getToken, logout } from "./api";
import type { CurrentUser } from "./api";

type Finding = {
  rule_name: string;
  category: string;
  severity: string;
  weight: number;
  is_critical: boolean;
  evidence_summary: string;
};

type InspectResult = {
  correlation_id: string;
  risk_score: number;
  decision: string;
  reason_code: string;
  findings: Finding[];
};

type SecuritySummary = {
  total_events: number;
  blocked_events: number;
  allowed_events: number;
  average_risk: number;
};


function Dashboard({
  onLogout,
  user,
}: {
  onLogout: () => void;
  user: CurrentUser;
}) {
  const canInspect = user.role === "Admin" || user.role === "Analyst";
  const [applicationId, setApplicationId] = useState("1");
  const [endpointId, setEndpointId] = useState("1");
  const [text, setText] = useState("Hello, this is a normal request.");
  const [result, setResult] = useState<InspectResult | null>(null);
  const [summary, setSummary] = useState<SecuritySummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const [error, setError] = useState("");
  const [summaryError, setSummaryError] = useState("");

  const loadAnalytics = useCallback(async () => {
    setAnalyticsLoading(true);
    setSummaryError("");

    try {
            const response = await authFetch("/api/v1/analytics/summary");

      if (response.status === 401) {
        onLogout();
        return;
      }

      if (!response.ok) {
        throw new Error(`Analytics request failed: ${response.status}`);
      }

      const data = (await response.json()) as SecuritySummary;
      setSummary(data);
    } catch {
      setSummaryError(
        "Could not load analytics. Check that FastAPI is running and the analytics endpoint is available.",
      );
    } finally {
      setAnalyticsLoading(false);
    }
  }, [onLogout]);

  useEffect(() => {
    void loadAnalytics();
  }, [loadAnalytics]);

  async function inspectRequest(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
        const response = await authFetch("/api/v1/inspect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          application_id: Number(applicationId),
          endpoint_id: Number(endpointId),
          text,
        }),
      });
      if (response.status === 401) {
        onLogout();
        return;
      }
      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : `Request failed with status ${response.status}`,
        );
      }

      setResult(data as InspectResult);

      // Refresh persisted analytics after a successful inspection.
      await loadAnalytics();
    } catch (err) {
      setError(
        err instanceof Error
          ? `${err.message}. Check that FastAPI is running and CORS allows this frontend origin.`
          : "Could not reach the PromptShield API.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand-mark">P</div>
        <div className="brand-name">PromptShield</div>
        <div className="brand-caption">APPLICATION SECURITY</div>

        <nav>
          <div className="nav-item active">◈ &nbsp; Overview</div>
          <div className="nav-item">⌁ &nbsp; Request Inspector</div>
          <div className="nav-item">▤ &nbsp; Security Events</div>
          <div className="nav-item">⚙ &nbsp; Settings</div>
        </nav>

        <div className="sidebar-bottom">
          <span className="status-dot" />
          {user.email}
          <br />
          Role: {user.role}
          <br />
          <small>FastAPI · Azure SQL</small>
        </div>
      </aside>

      <section className="main-content">
        <header className="topbar">
          <div>
            <div className="eyebrow">SECURITY OPERATIONS / OVERVIEW</div>
            <h1>Security dashboard</h1>
            <p>
              Inspect requests, evaluate risk, and review security decisions.
            </p>
          </div>

          <div className="environment-badge">
            <span className="status-dot" /> API environment
          </div>
                    <button type="button" className="logout-button" onClick={onLogout}>
            Sign out
          </button>
        </header>

        <section className="notice">
          <span className="notice-icon">i</span>
          <div>
            <strong>Development mode</strong>
            <p>
              Rule-based detection is enabled. Findings are heuristic signals,
              not a guarantee that every attack will be detected.
            </p>
          </div>
        </section>

        <section className="metrics-grid">
          <article className="metric-card">
            <div className="metric-label">TOTAL EVENTS</div>
            <div className="metric-value">
              {summary ? summary.total_events : "—"}
            </div>
            <div className="metric-note">Persisted inspection events</div>
          </article>

          <article className="metric-card">
            <div className="metric-label">BLOCKED EVENTS</div>
            <div className="metric-value danger-text">
              {summary ? summary.blocked_events : "—"}
            </div>
            <div className="metric-note">Requests blocked by policy</div>
          </article>

          <article className="metric-card">
            <div className="metric-label">ALLOWED EVENTS</div>
            <div className="metric-value">
              {summary ? summary.allowed_events : "—"}
            </div>
            <div className="metric-note">Requests allowed by policy</div>
          </article>

          <article className="metric-card">
            <div className="metric-label">AVERAGE RISK</div>
            <div className="metric-value">
              {summary ? summary.average_risk : "—"}
              <span className="metric-unit"> / 100</span>
            </div>
            <div className="metric-note">Average across recorded events</div>
          </article>
        </section>

        <div className="analytics-status">
          <span>
            {analyticsLoading
              ? "Refreshing analytics..."
              : "Analytics reflect persisted inspection events."}
          </span>
          <button
            type="button"
            className="secondary-button"
            onClick={() => void loadAnalytics()}
            disabled={analyticsLoading}
          >
            {analyticsLoading ? "Refreshing..." : "Refresh analytics"}
          </button>
        </div>

        {summaryError && (
          <div className="error-message" role="alert">
            <strong>Analytics unavailable</strong>
            <p>{summaryError}</p>
          </div>
        )}

                {!canInspect && (
          <section className="notice">
            <span className="notice-icon">i</span>
            <div>
              <strong>Read-only access</strong>
              <p>
                Your role ({user.role}) can view analytics but cannot run
                request inspections.
              </p>
            </div>
          </section>
        )}

        {canInspect && (
        <section className="workspace-grid">
          <article className="panel inspector-panel">
            <div className="panel-heading">
              <div>
                <div className="eyebrow">LIVE TEST</div>
                <h2>Request inspector</h2>
              </div>
              <span className="tag">POST</span>
            </div>

            <p className="panel-description">
              Submit sample text to your local PromptShield inspection API.
            </p>

            <form onSubmit={inspectRequest}>
              <div className="form-row">
                <label>
                  Application ID
                  <input
                    type="number"
                    min="1"
                    value={applicationId}
                    onChange={(event) =>
                      setApplicationId(event.target.value)
                    }
                    required
                  />
                </label>

                <label>
                  Endpoint ID
                  <input
                    type="number"
                    min="1"
                    value={endpointId}
                    onChange={(event) => setEndpointId(event.target.value)}
                    required
                  />
                </label>
              </div>

              <label>
                Request text
                <textarea
                  value={text}
                  onChange={(event) => setText(event.target.value)}
                  maxLength={10000}
                  minLength={1}
                  rows={6}
                  required
                  placeholder="Enter sample text to inspect..."
                />
              </label>

              <div className="form-footer">
                <span>{text.length.toLocaleString()} / 10,000 characters</span>
                <button type="submit" disabled={loading}>
                  {loading ? "Inspecting..." : "Inspect request →"}
                </button>
              </div>
            </form>

            {error && (
              <div className="error-message" role="alert">
                <strong>Inspection failed</strong>
                <p>{error}</p>
              </div>
            )}
          </article>

          <article className="panel result-panel">
            <div className="panel-heading">
              <div>
                <div className="eyebrow">LATEST RESPONSE</div>
                <h2>Inspection result</h2>
              </div>

              {result && (
                <span
                  className={`decision-tag ${
                    result.decision === "Block" ? "blocked" : "allowed"
                  }`}
                >
                  {result.decision.toUpperCase()}
                </span>
              )}
            </div>

            {!result && !error && (
              <div className="empty-state">
                <div className="empty-icon">⌕</div>
                <strong>Waiting for inspection</strong>
                <p>
                  Submit a sample request to view the risk score and findings.
                </p>
              </div>
            )}

            {result && (
              <div className="result-content">
                <div className="score-block">
                  <div className="score-number">{result.risk_score}</div>
                  <div>
                    <strong>Risk score</strong>
                    <p>out of 100</p>
                  </div>
                </div>

                <div className="score-track">
                  <div
                    className={`score-fill ${
                      result.decision === "Block" ? "blocked-fill" : ""
                    }`}
                    style={{
                      width: `${Math.min(
                        100,
                        Math.max(0, result.risk_score),
                      )}%`,
                    }}
                  />
                </div>

                <div className="result-detail">
                  <span>Reason code</span>
                  <code>{result.reason_code}</code>
                </div>

                <div className="result-detail">
                  <span>Findings</span>
                  <strong>{result.findings.length}</strong>
                </div>

                <div className="correlation">
                  <span>Correlation ID</span>
                  <code>{result.correlation_id}</code>
                </div>

                <div className="findings-heading">Detected findings</div>

                {result.findings.length === 0 ? (
                  <p className="no-findings">
                    No enabled rules matched this request.
                  </p>
                ) : (
                  result.findings.map((finding, index) => (
                    <div
                      className="finding-item"
                      key={`${finding.category}-${index}`}
                    >
                      <div className="finding-symbol">!</div>
                      <div className="finding-copy">
                        <strong>{finding.rule_name}</strong>
                        <p>
                          {finding.category} · {finding.severity} · Weight{" "}
                          {finding.weight}
                        </p>
                        <small>{finding.evidence_summary}</small>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </article>
        </section>
        )}

        <footer>
          <span>PromptShield · Capstone prototype</span>
          <span>Requests are inspected and logged; this UI does not forward traffic.</span>
        </footer>
      </section>
    </main>
  );
}

function App() {
  const [loggedIn, setLoggedIn] = useState(() => getToken() !== null);
  const [user, setUser] = useState<CurrentUser | null>(null);

  const handleLogout = useCallback(() => {
    logout();
    setUser(null);
    setLoggedIn(false);
  }, []);

  useEffect(() => {
    if (!loggedIn) {
      return;
    }

    let cancelled = false;

    getCurrentUser()
      .then((profile) => {
        if (cancelled) return;
        if (profile === null) {
          handleLogout();
        } else {
          setUser(profile);
        }
      })
      .catch(() => {
        if (!cancelled) handleLogout();
      });

    return () => {
      cancelled = true;
    };
  }, [loggedIn, handleLogout]);

  if (!loggedIn) {
    return <Login onLoginSuccess={() => setLoggedIn(true)} />;
  }

  if (user === null) {
    return <p style={{ padding: "2rem" }}>Loading...</p>;
  }

  return <Dashboard onLogout={handleLogout} user={user} />;
}

export default App;