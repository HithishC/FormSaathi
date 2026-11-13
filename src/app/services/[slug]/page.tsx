import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, ArrowUpRight, CheckCircle2, FileText, ListChecks } from "lucide-react";
import { services } from "@/data/services";
import { Checklist } from "@/components/checklist";

export function generateStaticParams() {
  return services.map((service) => ({ slug: service.slug }));
}

export default async function ServiceDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const service = services.find((item) => item.slug === slug);
  if (!service) notFound();

  return <section className="page-shell wrap detail-page">
    <Link href="/services" className="back-link"><ArrowLeft size={16} /> Back to services</Link>
    <div className="detail-hero">
      <div className="detail-icon">{service.icon}</div>
      <div><span className="pill">{service.categoryLabel}</span><h1>{service.title}</h1><p>{service.description}</p></div>
    </div>
    <div className="detail-layout">
      <div className="detail-main">
        <section className="content-card"><h2>Who may need this?</h2><p>{service.overview}</p><h3>Eligibility notes</h3><ul className="check-list">{service.eligibility.map(item => <li key={item}><CheckCircle2 size={17} />{item}</li>)}</ul></section>
        <section className="content-card"><h2>Application steps</h2><ol className="steps-list">{service.steps.map((step, index) => <li key={step}><span>{index + 1}</span><p>{step}</p></li>)}</ol></section>
        <section className="content-card official-card"><div><h2>Check the official source</h2><p>Rules, forms and links can change. Confirm the latest information with the relevant official department before applying.</p></div><a className="button button-primary" href={service.officialUrl} target="_blank" rel="noreferrer">Official information <ArrowUpRight size={16} /></a></section>
      </div>
      <aside className="detail-side"><div className="content-card"><h2><FileText size={19} /> Documents to prepare</h2><p className="muted">This is a general preparation list. The exact requirements may vary.</p><Checklist items={service.documents} storageKey={`formsaathi-${service.slug}-docs`} /></div><div className="help-card"><ListChecks size={22} /><b>Need help understanding this?</b><p>Ask the assistant to explain the process in simpler words.</p><Link href="/assistant" className="text-link">Ask FormSaathi <ArrowUpRight size={15} /></Link></div></aside>
    </div>
  </section>;
}
