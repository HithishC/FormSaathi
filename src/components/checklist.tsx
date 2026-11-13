"use client";

import { useEffect, useState } from "react";
import { Check, Printer } from "lucide-react";

export function Checklist({ items, storageKey }: { items: string[]; storageKey: string }) {
  const [checked, setChecked] = useState<string[]>([]);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    try {
      const saved = localStorage.getItem(storageKey);
      if (saved) setChecked(JSON.parse(saved) as string[]);
    } catch { /* Ignore invalid local storage data. */ }
    setReady(true);
  }, [storageKey]);

  function toggle(item: string) {
    setChecked(current => {
      const next = current.includes(item) ? current.filter(value => value !== item) : [...current, item];
      try { localStorage.setItem(storageKey, JSON.stringify(next)); } catch { /* Storage may be unavailable. */ }
      return next;
    });
  }

  const progress = items.length ? Math.round((checked.length / items.length) * 100) : 0;
  return <div className="checklist">
    <div className="progress-copy"><span>{ready ? checked.length : 0} of {items.length} ready</span><b>{ready ? progress : 0}%</b></div>
    <div className="progress-track"><span style={{ width: `${ready ? progress : 0}%` }} /></div>
    <div className="check-items">{items.map(item => <label key={item} className={checked.includes(item) ? "check-item is-checked" : "check-item"}><input type="checkbox" checked={checked.includes(item)} onChange={() => toggle(item)} /><span className="fake-check"><Check size={13} /></span><span>{item}</span></label>)}</div>
    <button className="print-button" onClick={() => window.print()}><Printer size={15} /> Print checklist</button>
    <small className="muted">Your ticks are saved on this browser only.</small>
  </div>;
}
