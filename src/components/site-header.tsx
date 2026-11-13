"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X, AudioLines } from "lucide-react";
import { useState } from "react";

const links = [
  { href: "/", label: "Home" },
  { href: "/services", label: "Explore services" },
  { href: "/assistant", label: "Voice assistant" },
  { href: "/about", label: "About" }
];

export function SiteHeader() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  return <header className="site-header"><div className="wrap nav-wrap">
    <Link href="/" className="brand" onClick={() => setOpen(false)}><span className="brand-mark"><AudioLines size={20} /></span><span>Form<span>Saathi</span></span></Link>
    <button className="mobile-menu" aria-label={open ? "Close menu" : "Open menu"} onClick={() => setOpen(!open)}>{open ? <X /> : <Menu />}</button>
    <nav className={open ? "nav-links nav-open" : "nav-links"}>{links.map(link => <Link key={link.href} href={link.href} onClick={() => setOpen(false)} className={pathname === link.href || (link.href !== "/" && pathname.startsWith(link.href)) ? "nav-active" : ""}>{link.label}</Link>)}</nav>
    <Link href="/assistant" className="nav-cta">Get guidance <span>↗</span></Link>
  </div></header>;
}
