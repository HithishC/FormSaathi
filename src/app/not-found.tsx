import Link from "next/link";
export default function NotFound() {
  return <section className="page-shell wrap centered"><p className="kicker">404</p><h1>We couldn't find that page.</h1><p>Try returning to the service directory.</p><Link className="button button-primary" href="/services">Explore services</Link></section>;
}
