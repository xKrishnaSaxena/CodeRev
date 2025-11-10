import { useState } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

function App() {
  const [code, setCode] = useState(`# Your code here\nprint("Hello, World!")`);
  const [language, setLanguage] = useState("python");
  const [context, setContext] = useState("A simple script for testing.");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const languages = [
    { value: "python", label: "Python" },
    { value: "javascript", label: "JavaScript" },
    { value: "java", label: "Java" },
    { value: "cpp", label: "C++" },
    { value: "go", label: "Go" },
    { value: "rust", label: "Rust" },
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE}/review`, {
        code_snippet: code,
        language,
        context,
      });
      setResult(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || "An error occurred during review."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case "high":
        return "bg-red-100 text-red-800 border-red-200";
      case "med":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "low":
        return "bg-green-100 text-green-800 border-green-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-8">
          Code Review Assistant
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6 mb-8">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Language
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={isLoading}
            >
              {languages.map((lang) => (
                <option key={lang.value} value={lang.value}>
                  {lang.label}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Code Snippet
            </label>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              rows={10}
              className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical font-mono text-sm"
              placeholder="Paste your code here..."
              disabled={isLoading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Context (optional)
            </label>
            <textarea
              value={context}
              onChange={(e) => setContext(e.target.value)}
              rows={3}
              className="w-full p-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-vertical"
              placeholder="Describe the purpose or requirements..."
              disabled={isLoading}
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium py-3 px-4 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200"
          >
            {isLoading ? (
              <span className="flex items-center justify-center">
                <svg
                  className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Reviewing...
              </span>
            ) : (
              "Review Code"
            )}
          </button>
        </form>

        {error && (
          <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-800">{error}</p>
          </div>
        )}

        {result && (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Review Report
              </h2>
              {result.report?.overall_score !== undefined && (
                <div className="mb-4 p-3 bg-blue-50 rounded-md">
                  <p className="text-lg font-medium text-blue-900">
                    Overall Score: {result.report.overall_score}/100
                  </p>
                </div>
              )}
              {result.report?.report_summary && (
                <div className="prose prose-sm max-w-none">
                  <p className="text-gray-700 whitespace-pre-wrap">
                    {result.report.report_summary}
                  </p>
                </div>
              )}
              {result.report?.improved_code && (
                <div className="mt-4">
                  <h3 className="text-md font-medium text-gray-900 mb-2">
                    Improved Code:
                  </h3>
                  <pre className="bg-gray-100 p-3 rounded-md overflow-x-auto font-mono text-sm">
                    {result.report.improved_code}
                  </pre>
                </div>
              )}
            </div>

            {result.issues?.length > 0 && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  Detected Issues
                </h2>
                <div className="space-y-3">
                  {result.issues.slice(0, 5).map(
                    (
                      issue,
                      index // Top 5 as per synthesis
                    ) => (
                      <div
                        key={index}
                        className="flex space-x-3 p-3 border border-gray-200 rounded-md hover:shadow-sm transition-shadow duration-200"
                      >
                        <div
                          className={`flex-shrink-0 w-2 h-2 mt-2 rounded-full ${getSeverityColor(
                            issue.severity
                          )}`}
                        ></div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {issue.type} (Line {issue.line})
                          </p>
                          <p className="text-sm text-gray-600 mt-1">
                            {issue.description}
                          </p>
                          {issue.suggestion && (
                            <p className="text-sm text-gray-500 mt-1 italic">
                              Suggestion: {issue.suggestion}
                            </p>
                          )}
                        </div>
                      </div>
                    )
                  )}
                  {result.issues.length > 5 && (
                    <p className="text-sm text-gray-500 text-center py-2">
                      ... and {result.issues.length - 5} more issues
                    </p>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
