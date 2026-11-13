import { FileBadge, Landmark, GraduationCap, Wheat, HeartPulse, CreditCard } from "lucide-react";
import type { GovernmentService } from "@/types/service";

export const services: GovernmentService[] = [
  {
    slug: "income-certificate", title: "Income certificate", category: "identity", categoryLabel: "Certificates",
    description: "Understand how income certificates are commonly requested through state revenue services.",
    overview: "An income certificate is a government document used as proof of a person's or family's income for certain applications and benefits.",
    eligibility: ["Applicants should check the issuing state's residence requirements.", "Income details may need to be supported by accepted evidence.", "The required process can differ between states and districts."],
    documents: ["Identity proof", "Address or residence proof", "Income evidence", "Recent photograph", "Application form or acknowledgement"],
    steps: ["Open your state e-District or revenue department portal.", "Find the income certificate service and read the current eligibility rules.", "Prepare the documents listed by your state.", "Submit the application online or at an authorised service centre.", "Save the acknowledgement and track the application status."],
    officialUrl: "https://services.india.gov.in/", icon: <FileBadge size={22} />, tone: "blue"
  },
  {
    slug: "old-age-pension", title: "Old-age pension", category: "pension", categoryLabel: "Pension & welfare",
    description: "A starting guide to checking old-age pension eligibility and application routes.",
    overview: "Old-age pension support is provided through central and state schemes. Age, income, residence and other criteria vary by scheme and state.",
    eligibility: ["Check the minimum age for the specific scheme.", "Review income, residence and other state-specific conditions.", "Confirm whether the applicant is already receiving another pension."],
    documents: ["Age proof", "Identity proof", "Residence proof", "Bank account details", "Income or eligibility certificate, if required"],
    steps: ["Identify the applicable central or state pension scheme.", "Read the latest eligibility criteria on the official department website.", "Collect the documents required for your area.", "Apply through the official portal or local authorised office.", "Keep the application receipt and check the status."],
    officialUrl: "https://nsap.nic.in/", icon: <Landmark size={22} />, tone: "orange"
  },
  {
    slug: "scholarship", title: "Student scholarships", category: "education", categoryLabel: "Education",
    description: "Find out what to check before applying for a student scholarship.",
    overview: "Scholarships may be offered by central ministries, state departments, universities and other institutions. Eligibility depends on the specific scholarship.",
    eligibility: ["Check course, institution and academic requirements.", "Review any family-income or category criteria.", "Confirm the application window and renewal conditions."],
    documents: ["Student ID or admission details", "Previous examination marksheet", "Bank account details", "Income certificate, if required", "Category certificate, if required"],
    steps: ["Search for scholarships relevant to your course and state.", "Read the official scheme guidelines carefully.", "Prepare the required student and family documents.", "Submit the application through the official scholarship portal.", "Track verification and keep a copy of the submitted form."],
    officialUrl: "https://scholarships.gov.in/", icon: <GraduationCap size={22} />, tone: "purple"
  },
  {
    slug: "farmer-support", title: "Farmer support schemes", category: "agriculture", categoryLabel: "Agriculture",
    description: "Explore the checks farmers should make before applying for support schemes.",
    overview: "Agriculture support programmes can include income support, insurance, credit and state-specific benefits. Rules depend on the scheme and land or farmer records.",
    eligibility: ["Check the scheme's farmer and land-record conditions.", "Confirm exclusions and state-specific rules.", "Use only the current official application window."],
    documents: ["Identity proof", "Land or cultivation records, if required", "Bank account details", "Mobile number", "Other scheme-specific records"],
    steps: ["Identify the exact central or state agriculture scheme.", "Check eligibility on the official agriculture department website.", "Confirm the required land and identity records.", "Apply through the official portal or notified office.", "Save the application reference for future tracking."],
    officialUrl: "https://agriwelfare.gov.in/", icon: <Wheat size={22} />, tone: "green"
  },
  {
    slug: "health-benefits", title: "Health benefit schemes", category: "health", categoryLabel: "Healthcare",
    description: "Learn how to verify eligibility and participating facilities for health schemes.",
    overview: "Public health benefit schemes may provide eligible families access to specified healthcare services. Coverage and eligibility must be checked against current scheme rules.",
    eligibility: ["Check the scheme's current beneficiary eligibility rules.", "Confirm whether the hospital or facility participates.", "Review covered services and exclusions."],
    documents: ["Identity or beneficiary ID", "Ration card or family details, if required", "Mobile number", "Relevant medical records"],
    steps: ["Identify the health scheme relevant to your family.", "Verify beneficiary status using the official scheme channel.", "Check the participating hospital or facility list.", "Carry the required identity and beneficiary documents.", "Ask the official helpdesk about coverage before treatment."],
    officialUrl: "https://pmjay.gov.in/", icon: <HeartPulse size={22} />, tone: "red"
  },
  {
    slug: "pan-card", title: "PAN card", category: "identity", categoryLabel: "Identity documents",
    description: "Understand the basic route for applying for or updating a PAN card.",
    overview: "PAN is a tax identification number issued by the Income Tax Department. Applications and corrections are handled through authorised channels.",
    eligibility: ["Check whether you need a new PAN or a correction.", "Use the correct application route for an individual or entity.", "Avoid submitting multiple applications unnecessarily."],
    documents: ["Proof of identity", "Proof of address", "Proof of date of birth", "Recent photograph, if requested"],
    steps: ["Visit the Income Tax Department's official PAN information page.", "Choose the appropriate new PAN or correction service.", "Follow the instructions on the authorised application portal.", "Submit the required documents and fee, if applicable.", "Save the acknowledgement to track your request."],
    officialUrl: "https://www.incometax.gov.in/", icon: <CreditCard size={22} />, tone: "blue"
  }
];
