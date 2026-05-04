import { useEffect, useRef, useState } from "react";
import { Mic, Send } from "lucide-react";
import api from "../services/api";

const starter = {
  role: "assistant",
  content: "**FinMate AI is ready.** Ask about spending, budgets, savings, financial health, or investment basics."
};

export default function Chat() {
  const [messages, setMessages] = useState([starter]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    api.get("/chat/history").then((res) => {
      if (res.data.length) setMessages([starter, ...res.data]);
    }).catch(() => {});
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const send = async (event) => {
    event.preventDefault();
    if (!input.trim() || loading) return;
    const userMessage = { role: "user", content: input.trim() };
    setMessages((current) => [...current, userMessage, { role: "assistant", content: "" }]);
    setInput("");
    setLoading(true);
    try {
      const response = await fetch(`${api.defaults.baseURL}/chat/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage.content })
      });
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      if (!reader) throw new Error("Streaming unavailable");
      let answer = "";
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        answer += decoder.decode(value);
        setMessages((current) => current.map((item, index) => index === current.length - 1 ? { ...item, content: answer } : item));
      }
    } catch {
      const { data } = await api.post("/chat", { message: userMessage.content });
      setMessages((current) => current.map((item, index) => index === current.length - 1 ? { ...item, content: data.answer } : item));
    } finally {
      setLoading(false);
    }
  };

  const startVoice = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;
    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.onresult = (event) => setInput(event.results[0][0].transcript);
    recognition.start();
  };

  return (
    <div className="mx-auto grid max-w-4xl gap-4">
      <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm dark:border-white/10 dark:bg-slate-900">
        <div className="mb-4 flex items-center justify-between border-b border-slate-100 pb-4 dark:border-white/10">
          <div>
            <h2 className="text-xl font-black">AI Finance Assistant</h2>
            <p className="text-sm text-slate-500 dark:text-slate-400">Context-aware answers using transactions, budgets, predictions, and health score.</p>
          </div>
          <span className="rounded-lg bg-mint/15 px-3 py-2 text-sm font-bold text-emerald-700 dark:text-mint">Streaming</span>
        </div>
        <div className="grid max-h-[560px] min-h-[520px] gap-3 overflow-y-auto pr-1">
          {messages.map((message, index) => (
            <div key={index} className={`max-w-[86%] rounded-lg px-4 py-3 text-sm leading-6 ${message.role === "user" ? "ml-auto bg-ink text-white dark:bg-mint dark:text-ink" : "bg-slate-100 dark:bg-slate-950"}`}>
              <MarkdownText text={message.content || (loading && index === messages.length - 1 ? "Typing..." : "")} />
            </div>
          ))}
          <div ref={scrollRef} />
        </div>
      </div>
      <form onSubmit={send} className="flex gap-2">
        <button type="button" onClick={startVoice} aria-label="Voice command" title="Voice command" className="grid h-12 w-12 place-items-center rounded-lg border border-slate-200 bg-white dark:border-white/10 dark:bg-slate-900">
          <Mic size={18} />
        </button>
        <input className="min-w-0 flex-1 rounded-lg border px-4 py-3 dark:border-white/10 dark:bg-slate-950" value={input} onChange={(event) => setInput(event.target.value)} placeholder="Ask: How is my budget looking this month?" />
        <button aria-label="Send message" className="grid h-12 w-12 place-items-center rounded-lg bg-ink text-white dark:bg-mint dark:text-ink"><Send size={18} /></button>
      </form>
    </div>
  );
}

function MarkdownText({ text }) {
  const escaped = text.replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[char]));
  const html = escaped
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/`(.*?)`/g, "<code>$1</code>")
    .replace(/\n/g, "<br />");
  return <span dangerouslySetInnerHTML={{ __html: html }} />;
}
