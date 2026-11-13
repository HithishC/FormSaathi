import { HeartHandshake, Languages, ShieldCheck, Users } from "lucide-react";

export default function AboutPage() {
  return <section className="page-shell wrap">
    <div className="page-intro"><p className="kicker">About FormSaathi</p><h1>Technology should make public services easier to understand.</h1><p>FormSaathi is a hackathon prototype exploring how voice-first, plain-language guidance can help people navigate government services with more confidence.</p></div>
    <div className="values-grid">
      <article className="value-card"><Languages /><h2>Language access</h2><p>Make information easier to approach through familiar languages and voice interaction.</p></article>
      <article className="value-card"><Users /><h2>Inclusive by design</h2><p>Consider citizens who may be new to digital forms, portals or online processes.</p></article>
      <article className="value-card"><ShieldCheck /><h2>Trust and clarity</h2><p>Separate general guidance from official rules and encourage verification at source.</p></article>
      <article className="value-card"><HeartHandshake /><h2>Human-centred support</h2><p>Break complicated processes into manageable, understandable steps.</p></article>
    </div>
    <div className="notice"><b>Prototype notice</b><p>This project is a demonstration. It is not affiliated with or endorsed by any government department. Scheme data and assistant answers must be verified before real-world use.</p></div>
  </section>;
}
