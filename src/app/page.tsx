import { ServicesExplorer } from "@/components/services-explorer";
import { services } from "@/data/services";

export default function ServicesPage() {
  return <section className="page-shell wrap">
    <div className="page-intro"><p className="kicker">Service directory</p><h1>Explore government services</h1><p>Search common services and open a guide to see example eligibility notes, document lists and next steps.</p></div>
    <ServicesExplorer items={services} />
  </section>;
}
