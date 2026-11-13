"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { AudioLines, Bot, Mic, MicOff, Send, Volume2, VolumeX, Sparkles, UserRound } from "lucide-react";

type Message = { role: "user" | "assistant"; text: string };
type RecognitionResult = { 0: { transcript: string }; isFinal: boolean };
type RecognitionEvent = { resultIndex: number; results: ArrayLike<RecognitionResult> };
type RecognitionErrorEvent = { error: string };
type RecognitionInstance = {
  lang: string; continuous: boolean; interimResults: boolean;
  onstart: (() => void) | null; onresult: ((event: RecognitionEvent) => void) | null;
  onerror: ((event: RecognitionErrorEvent) => void) | null; onend: (() => void) | null;
  start: () => void; stop: () => void; abort: () => void;
};
type SpeechWindow = Window & { SpeechRecognition?: new () => RecognitionInstance; webkitSpeechRecognition?: new () => RecognitionInstance };

const suggestions = ["How can I apply for an old-age pension?", "What documents are needed for an income certificate?", "How do I apply for a scholarship?", "How can I get a ration card?"];

function sampleAnswer(question: string) {
  const q = question.toLowerCase();
  if (q.includes("pension") || q.includes("old-age")) return "For an old-age pension, start by checking the age, residence and income rules for your state. These vary by scheme. In general, you may be asked for proof of age, identity, residence, bank details and an income-related document. 1) Check your state social-welfare department's official scheme page. 2) Confirm eligibility and the current document list. 3) Apply through the official portal or a notified service centre. 4) Keep the acknowledgement number. Would you like to open the pension guide?";
  if (q.includes("ration")) return "Ration-card requirements differ by state. Commonly requested items can include identity and address proof, family-member details and photographs. Check your state's food and civil supplies department for the current list and application process. You can use the Services directory to find a related guide.";
  if (q.includes("scholarship")) return "Scholarship applications usually depend on the student's course, institution, category and family income. Keep your student ID, previous marksheet, bank details and any required income or category certificate ready. Check the official National Scholarship Portal or your state scholarship portal for current eligibility and dates.";
  if (q.includes("income") || q.includes("certificate")) return "An income certificate is generally issued by a state revenue department. The process commonly involves filling an application, providing identity and residence proof plus income evidence, and submitting it online or at a service centre. The exact documents and fees depend on your state. Check your state e-District portal for current instructions.";
  return "I can help you understand common government-service steps. Please tell me the service name and your state. I can outline what to check, which documents may be needed and where to verify the official process. This demo answer is general guidance, so confirm current details with the relevant government department.";
}

export function AssistantPanel() {
  const [language, setLanguage] = useState("en-IN");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([{ role: "assistant", text: "Namaste! I'm Saathi. Ask me about a government service, scheme or document. You can type or use the microphone." }]);
  const [listening, setListening] = useState(false);
  const [status, setStatus] = useState("");
  const [speaking, setSpeaking] = useState(false);
  const recognitionRef = useRef<RecognitionInstance | null>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  function startListening() {
    if (typeof window === "undefined") return;
    const speechWindow = window as SpeechWindow;
    const Recognition = speechWindow.SpeechRecognition || speechWindow.webkitSpeechRecognition;
    if (!Recognition) {
      setStatus("Voice input is not supported in this browser. Please type your question instead.");
      return;
    }
    try {
      recognitionRef.current?.abort();
      const recognition = new Recognition();
      recognitionRef.current = recognition;
      recognition.lang = language;
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.onstart = () => { setListening(true); setStatus("Listening… speak now."); };
      recognition.onresult = (event) => {
        const transcript = Array.from(event.results).map(result => result[0].transcript).join(" ").trim();
        if (transcript) { setInput(transcript); setStatus("Speech captured. Press Send to get guidance."); }
      };
      recognition.onerror = (event) => {
        const messagesByError: Record<string, string> = {
          "not-allowed": "Microphone permission is blocked. Allow microphone access in your browser settings.",
          "service-not-allowed": "The browser speech service is unavailable. Try typing your question.",
          "no-speech": "No speech was detected. Try again and speak clearly.",
          "network": "Speech recognition needs a network connection. Check your internet and retry.",
          "audio-capture": "No microphone was found. Check your laptop's microphone settings."
        };
        setStatus(messagesByError[event.error] || `Voice input error: ${event.error}. You can type your question instead.`);
      };
      recognition.onend = () => setListening(false);
      recognition.start();
    } catch {
      setListening(false);
      setStatus("Could not start the microphone. Check browser permission and try again.");
    }
  }

  function stopListening() {
    recognitionRef.current?.stop();
    setListening(false);
  }

  function speak(text: string) {
    if (!("speechSynthesis" in window)) { setStatus("Read-aloud is not supported in this browser."); return; }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language;
    utterance.onstart = () => setSpeaking(true);
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    window.speechSynthesis.speak(utterance);
  }

  function sendQuestion(question: string) {
    const trimmed = question.trim();
    if (!trimmed) return;
    const answer = sampleAnswer(trimmed);
    setMessages(current => [...current, { role: "user", text: trimmed }, { role: "assistant", text: answer }]);
    setInput("");
    setStatus("Demo guidance generated. Connect an AI backend for live answers.");
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    sendQuestion(input);
  }

  return <div className="assistant-card">
    <div className="assistant-toolbar"><div><span className="online-dot" /> Saathi assistant <small>General guidance demo</small></div><label className="language-select"><span>Language</span><select value={language} onChange={event => setLanguage(event.target.value)}><option value="en-IN">English</option><option value="hi-IN">हिन्दी</option><option value="kn-IN">ಕನ್ನಡ</option><option value="ta-IN">தமிழ்</option><option value="te-IN">తెలుగు</option><option value="ml-IN">മലയാളം</option></select></label></div>
    <div className="chat-area">
      {messages.map((message, index) => <div key={`${index}-${message.role}`} className={`message-row ${message.role}`}><span className="avatar">{message.role === "assistant" ? <Bot size={18} /> : <UserRound size={18} />}</span><div className="message-bubble"><p>{message.text}</p>{message.role === "assistant" && <button className="speak-button" onClick={() => speaking ? (window.speechSynthesis.cancel(), setSpeaking(false)) : speak(message.text)}>{speaking ? <VolumeX size={15} /> : <Volume2 size={15} />}{speaking ? "Stop reading" : "Read aloud"}</button>}</div></div>)}
      <div ref={bottomRef} />
    </div>
    <div className="suggestion-area"><span className="suggestion-label"><Sparkles size={14} /> Try asking</span><div className="suggestion-list">{suggestions.map(question => <button key={question} onClick={() => sendQuestion(question)}>{question}</button>)}</div></div>
    {status && <div className="assistant-status" role="status">{status}</div>}
    <form className="chat-composer" onSubmit={handleSubmit}><button type="button" className={listening ? "mic-button is-listening" : "mic-button"} aria-label={listening ? "Stop listening" : "Start voice input"} onClick={listening ? stopListening : startListening}>{listening ? <MicOff size={20} /> : <Mic size={20} />}</button><input value={input} onChange={event => setInput(event.target.value)} placeholder={listening ? "Listening… speak now" : "Type your question here…"} aria-label="Your question" /><button className="send-button" type="submit" disabled={!input.trim()} aria-label="Send question"><Send size={18} /></button></form>
    <div className="assistant-footnote"><AudioLines size={14} /> Speech recognition availability depends on your browser and device. Sample answers are not official advice.</div>
  </div>;
}
