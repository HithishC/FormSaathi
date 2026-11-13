import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import type { GovernmentService } from "@/types/service";

export function ServiceCard({ service }: { service: GovernmentService }) {
  return <article className="service-card">
    <div className="service-card-top"><span className={`service-icon ${service.tone}`}>{service.icon}</span><span className="pill">{service.categoryLabel}</span></div>
    <h3>{service.title}</h3><p>{service.description}</p>
    <Link href={`/services/${service.slug}`} className="card-link">View guide <ArrowUpRight size={16} /></Link>
  </article>;
}
