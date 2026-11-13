import Link from "next/link";
import { AudioLines } from "lucide-react";

export function SiteFooter() {
  return <footer className="site-footer"><div className="wrap footer-inner">
    <div><Link href="/" className="brand footer-brand"><span className="brand-mark"><AudioLines size={19} /></span><span>Form<span>Saathi</span></span></Link><p>Government services, made easier to understand.</p></div>
    <div className="footer-links"><Link href="/services">Services</Link><Link href="/assistant">Assistant</Link><Link href="/about">About</Link></div>
    <p className="footer-note">Independent prototype · Verify details with official sources.</p>
  </div></footer>;
}
