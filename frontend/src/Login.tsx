
import { useState } from "react";
import { login } from "./api";

type LoginProps = {
  onLoginSuccess: () => void;
};

const DEMO_EMAIL = "teacher.demo@promptshield.local";
const DEMO_PASSWORD = "Promptshield@123";

function Login({ onLoginSuccess }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      await login(email, password);
      setPassword("");
      onLoginSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleSubmit}>
        <h1>PromptShield</h1>
        <p>Cloud-Native Application Security Gateway</p>

        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="username"
          placeholder="Enter your email"
          required
        />

        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
          placeholder="Enter your password"
          required
        />

        {error && (
          <p className="login-error" role="alert">
            {error}
          </p>
        )}

        <button type="submit" disabled={loading}>
          {loading ? "Signing in..." : "Sign in"}
        </button>

        <div className="demo-account-info">
          <h3>Explore PromptShield</h3>
          <p>
            Welcome, Teacher/Evaluator! Use the public demo
            account below to explore the dashboard and test
            PromptShield security features.
          </p>

          <div>
            <strong>Demo Email</strong>
            <p>{DEMO_EMAIL}</p>
          </div>

          <div>
            <strong>Demo Password</strong>
            <p>{DEMO_PASSWORD}</p>
          </div>

          <span>Analyst Access · No Administrator Privileges</span>
        </div>
      </form>
    </div>
  );
}

export default Login;
