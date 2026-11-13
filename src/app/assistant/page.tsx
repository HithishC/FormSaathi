import { AssistantPanel } from "@/components/assistant-panel";

export default function AssistantPage() {
  return <section className="page-shell wrap">
    <div className="page-intro centered"><p className="kicker">Your FormSaathi guide</p><h1>What would you like help with?</h1><p>Speak or type a question. The demo assistant will show a sample guidance response.</p></div>
    <AssistantPanel />
    <p className="disclaimer">FormSaathi provides general guidance, not official approval or legal advice. Always verify current details on the relevant government portal.</p>
  </section>;
}
