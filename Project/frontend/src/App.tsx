import { useState } from "react";
import Hero from "@/components/Hero";
import ChatWorkspace from "@/components/ChatWorkspace";

const CHAT_ACTIVE_KEY = "wandor-rental-chat-active";

export default function App() {
  const [startingPrompt, setStartingPrompt] = useState<string | null>(() =>
    sessionStorage.getItem(CHAT_ACTIVE_KEY) ? "" : null,
  );
  const startChat = (prompt: string) => { sessionStorage.setItem(CHAT_ACTIVE_KEY, "true"); setStartingPrompt(prompt); };
  const returnHome = () => { sessionStorage.removeItem(CHAT_ACTIVE_KEY); setStartingPrompt(null); };
  return startingPrompt !== null
    ? <ChatWorkspace initialPrompt={startingPrompt} onBack={returnHome} />
    : <Hero onStart={startChat} />;
}
