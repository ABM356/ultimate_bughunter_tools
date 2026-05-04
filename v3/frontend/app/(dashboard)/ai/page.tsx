"use client";

import { useState } from "react";
import { Bot, FileText, Loader2, Send, Sparkles } from "lucide-react";
import { toast } from "sonner";
import { PageHeader } from "@/components/PageHeader";
import { SeverityBadge } from "@/components/SeverityBadge";
import { cn } from "@/lib/utils";
import type { Severity } from "@/lib/types";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  ts: string;
}

const STARTER_MESSAGES: ChatMessage[] = [
  {
    role: "assistant",
    content:
      "Hi! I'm your HopeUp AI assistant. Ask me about scans, vulnerabilities, or to generate executive reports. Try: \"summarize the top critical findings this week\".",
    ts: new Date().toISOString(),
  },
];

export default function AIPage() {
  const [messages, setMessages] = useState<ChatMessage[]>(STARTER_MESSAGES);
  const [input, setInput] = useState("");
  const [thinking, setThinking] = useState(false);
  const [classifying, setClassifying] = useState(false);
  const [classification, setClassification] = useState<{
    severity: Severity;
    cwe: string;
    confidence: number;
  } | null>(null);
  const [classifyText, setClassifyText] = useState("");

  const handleSend = async () => {
    if (!input.trim() || thinking) return;
    const userMsg: ChatMessage = { role: "user", content: input, ts: new Date().toISOString() };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setThinking(true);
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Analyzed scan SC-4421: 12 findings (1 critical, 3 high, 4 medium, 4 low). Critical SQLi on /search?q= should be patched immediately. Want me to draft an exec report?",
          ts: new Date().toISOString(),
        },
      ]);
      setThinking(false);
    }, 900);
  };

  const handleClassify = () => {
    if (!classifyText.trim()) return;
    setClassifying(true);
    setTimeout(() => {
      setClassification({ severity: "high", cwe: "CWE-89", confidence: 0.92 });
      setClassifying(false);
    }, 700);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="AI Assistant"
        description="Ask questions, classify vulnerabilities, generate reports"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 panel flex flex-col h-[600px]">
          <div className="px-4 py-3 border-b border-border flex items-center gap-2">
            <Bot className="h-4 w-4 text-accent" />
            <h3 className="text-sm font-semibold">Chat</h3>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={cn("flex", m.role === "user" ? "justify-end" : "justify-start")}
              >
                <div
                  className={cn(
                    "max-w-[80%] rounded-lg px-4 py-2.5 text-sm",
                    m.role === "user"
                      ? "bg-accent text-bg"
                      : "bg-bg-secondary border border-border text-fg",
                  )}
                >
                  {m.content}
                </div>
              </div>
            ))}
            {thinking && (
              <div className="flex justify-start">
                <div className="bg-bg-secondary border border-border rounded-lg px-4 py-2.5 text-sm flex items-center gap-2 text-fg-muted">
                  <Loader2 className="h-3 w-3 animate-spin" /> Thinking...
                </div>
              </div>
            )}
          </div>
          <div className="border-t border-border p-3 flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Ask about scans, vulnerabilities, reports..."
              className="input flex-1"
              disabled={thinking}
            />
            <button
              type="button"
              onClick={handleSend}
              disabled={thinking || !input.trim()}
              className="btn-primary"
              aria-label="Send"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
        </div>

        <div className="space-y-4">
          <div className="panel">
            <div className="px-4 py-3 border-b border-border flex items-center gap-2">
              <Sparkles className="h-4 w-4 text-accent" />
              <h3 className="text-sm font-semibold">Vulnerability Classifier</h3>
            </div>
            <div className="p-4 space-y-3">
              <textarea
                value={classifyText}
                onChange={(e) => setClassifyText(e.target.value)}
                placeholder="Paste a vulnerability description..."
                className="input min-h-[100px] text-xs"
              />
              <button
                type="button"
                onClick={handleClassify}
                className="btn-primary w-full"
                disabled={classifying || !classifyText}
              >
                {classifying ? <Loader2 className="h-4 w-4 animate-spin" /> : "Classify"}
              </button>
              {classification && (
                <div className="border border-border rounded-md p-3 space-y-2 animate-fade-in bg-bg-secondary">
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-fg-muted">Severity</span>
                    <SeverityBadge severity={classification.severity} />
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-fg-muted">CWE</span>
                    <span className="text-xs font-mono">{classification.cwe}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-fg-muted">Confidence</span>
                    <span className="text-xs font-mono text-accent">
                      {(classification.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="panel">
            <div className="px-4 py-3 border-b border-border flex items-center gap-2">
              <FileText className="h-4 w-4 text-accent" />
              <h3 className="text-sm font-semibold">Report Generator</h3>
            </div>
            <div className="p-4 space-y-3">
              <select className="input">
                <option>Executive Summary (CISO)</option>
                <option>Technical Report (Engineer)</option>
                <option>Compliance Report</option>
                <option>Board Update</option>
              </select>
              <select className="input">
                <option>Last 7 days</option>
                <option>Last 30 days</option>
                <option>Last quarter</option>
              </select>
              <button
                type="button"
                onClick={() => toast.success("Report queued")}
                className="btn-primary w-full"
              >
                Generate Report
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
