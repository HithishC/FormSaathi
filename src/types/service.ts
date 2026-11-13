import type { ReactNode } from "react";

export type GovernmentService = {
  slug: string;
  title: string;
  category: string;
  categoryLabel: string;
  description: string;
  overview: string;
  eligibility: string[];
  documents: string[];
  steps: string[];
  officialUrl: string;
  icon: ReactNode;
  tone: string;
};
