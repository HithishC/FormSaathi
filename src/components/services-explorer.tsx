"use client";

import { useMemo, useState } from "react";
import { Search, SlidersHorizontal } from "lucide-react";
import { ServiceCard } from "@/components/service-card";
import type { GovernmentService } from "@/types/service";

export function ServicesExplorer({ items }: { items: GovernmentService[] }) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("all");
  const categories = ["all", ...Array.from(new Set(items.map(item => item.category)))];
  const filtered = useMemo(() => items.filter(item => {
    const matchesQuery = `${item.title} ${item.description} ${item.categoryLabel}`.toLowerCase().includes(query.toLowerCase());
    return matchesQuery && (category === "all" || item.category === category);
  }), [items, query, category]);

  return <div>
    <div className="filter-bar"><label className="search-box"><Search size={19} /><input value={query} onChange={event => setQuery(event.target.value)} placeholder="Search a service, document or scheme..." /></label><label className="select-box"><SlidersHorizontal size={17} /><select value={category} onChange={event => setCategory(event.target.value)} aria-label="Filter by category">{categories.map(value => <option key={value} value={value}>{value === "all" ? "All categories" : value[0].toUpperCase() + value.slice(1)}</option>)}</select></label></div>
    <p className="result-count">{filtered.length} {filtered.length === 1 ? "guide" : "guides"} found</p>
    {filtered.length ? <div className="service-grid">{filtered.map(service => <ServiceCard key={service.slug} service={service} />)}</div> : <div className="empty-state"><Search size={26} /><h3>No matching services</h3><p>Try another search term or choose a different category.</p></div>}
  </div>;
}
