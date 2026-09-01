import React, { useState } from "react";

const API_URL = "https://verbose-eureka-5g4gp5x55pqx3v75x-8000.app.github.dev";

export default function App() {
  const [file, setFile] = useState(null);
  const [uploaded, setUploaded] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function uploadReport() {
    if (!file) return;

    setUploading(true);
    setError("");
    setAnswer("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Upload failed.");
      }

      setUploaded(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  }

  async function askQuestion() {
    if (!question.trim()) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          question: question
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to get answer.");
      }

      setAnswer(data.answer);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.page}>
      <div style={styles.container}>

        <header style={styles.header}>
          <div style={styles.logo}>✚</div>

          <div>
            <h1 style={styles.title}>MedReport AI</h1>
            <p style={styles.subtitle}>
              Understand your medical report in simple language.
            </p>
          </div>
        </header>

        <div style={styles.warning}>
          <strong>Educational use only</strong>
          <br />
          This AI explains medical information but does not diagnose
          conditions or replace professional medical advice.
        </div>

        <section style={styles.card}>
          <h2>📄 Upload your report</h2>

          <p style={styles.muted}>
            Upload a PDF blood test or laboratory report.
          </p>

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => {
              setFile(e.target.files[0]);
              setUploaded(false);
            }}
          />

          {file && (
            <p style={styles.fileName}>
              Selected: {file.name}
            </p>
          )}

          <button
            onClick={uploadReport}
            disabled={!file || uploading}
            style={styles.button}
          >
            {uploading ? "Processing..." : "Upload & Analyze"}
          </button>

          {uploaded && (
            <p style={styles.success}>
              ✓ Report processed successfully
            </p>
          )}
        </section>

        <section style={styles.card}>
          <h2>💬 Ask about your report</h2>

          <p style={styles.muted}>
            Ask about values, medical terms, or sections in your report.
          </p>

          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Example: What does my hemoglobin result mean?"
            style={styles.textarea}
          />

          <button
            onClick={askQuestion}
            disabled={!uploaded || !question.trim() || loading}
            style={styles.button}
          >
            {loading ? "Thinking..." : "Ask MedReport AI"}
          </button>
        </section>

        {answer && (
          <section style={styles.answerCard}>
            <h2>🤖 AI Explanation</h2>

            <div style={styles.answer}>
              {answer}
            </div>
          </section>
        )}

        {error && (
          <div style={styles.error}>
            {error}
          </div>
        )}

        <footer style={styles.footer}>
          🔒 No persistent medical data storage
          <br />
          LangChain • Groq • ChromaDB
        </footer>

      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#f4f7fb",
    fontFamily: "Arial, sans-serif",
    padding: "40px 20px"
  },

  container: {
    maxWidth: "800px",
    margin: "auto"
  },

  header: {
    display: "flex",
    alignItems: "center",
    gap: "15px",
    marginBottom: "25px"
  },

  logo: {
    width: "55px",
    height: "55px",
    borderRadius: "15px",
    background: "#2563eb",
    color: "white",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "28px"
  },

  title: {
    margin: 0,
    fontSize: "32px"
  },

  subtitle: {
    marginTop: "5px",
    color: "#64748b"
  },

  warning: {
    background: "#fff7ed",
    padding: "15px",
    borderRadius: "12px",
    marginBottom: "20px",
    color: "#9a3412"
  },

  card: {
    background: "white",
    padding: "25px",
    borderRadius: "18px",
    marginBottom: "20px",
    boxShadow: "0 5px 20px rgba(0,0,0,0.06)"
  },

  answerCard: {
    background: "white",
    padding: "25px",
    borderRadius: "18px",
    marginBottom: "20px",
    boxShadow: "0 5px 20px rgba(0,0,0,0.06)"
  },

  muted: {
    color: "#64748b"
  },

  fileName: {
    color: "#2563eb",
    fontWeight: "bold"
  },

  textarea: {
    width: "100%",
    minHeight: "120px",
    boxSizing: "border-box",
    padding: "15px",
    margin: "15px 0",
    borderRadius: "10px",
    border: "1px solid #cbd5e1",
    fontSize: "15px"
  },

  button: {
    width: "100%",
    padding: "14px",
    marginTop: "15px",
    border: "none",
    borderRadius: "10px",
    background: "#2563eb",
    color: "white",
    fontSize: "16px",
    fontWeight: "bold",
    cursor: "pointer"
  },

  success: {
    color: "#15803d",
    fontWeight: "bold"
  },

  answer: {
    whiteSpace: "pre-wrap",
    lineHeight: "1.7",
    color: "#334155"
  },

  error: {
    background: "#fee2e2",
    color: "#b91c1c",
    padding: "15px",
    borderRadius: "10px"
  },

  footer: {
    textAlign: "center",
    color: "#64748b",
    marginTop: "30px",
    lineHeight: "1.8"
  }
};