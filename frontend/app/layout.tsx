import type { Metadata } from "next";
import "./globals.css";

const SITE_URL = "https://guardrailai.in";
const SITE_NAME = "Guardrail.ai";
const TITLE = "Guardrail.ai | Sovereign AI Governance & Safety Platform";
const DESCRIPTION =
  "The world's only hardware-anchored, zero-cycle liability AI governance platform. Post-quantum compliant, Trinity Consensus veto engine, $14.8M liability buffer proven by Chaos Drill 24. Enterprise-grade agentic AI safety for 2026 and beyond.";
const KEYWORDS = [
  "AI governance platform",
  "AI safety enterprise",
  "agentic AI compliance",
  "AI veto system",
  "post-quantum AI security",
  "NIST AI RMF compliance",
  "EU AI Act compliance",
  "AI liability management",
  "autonomous agent governance",
  "constitutional AI guardrails",
  "LLM safety enterprise",
  "AI audit trail",
  "legal forensic AI proof",
  "sovereign AI platform",
  "multi-agent security",
  "hardware-anchored AI",
  "AI circuit breaker",
  "AI regulatory compliance 2026",
  "trinity consensus veto",
  "agentic AI risk management",
];

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),

  // ── Core ───────────────────────────────────────────────────────────────────
  title: {
    default: TITLE,
    template: `%s | ${SITE_NAME}`,
  },
  description: DESCRIPTION,
  keywords: KEYWORDS,
  authors: [{ name: "Praveen Rai", url: SITE_URL }],
  creator: "Praveen Rai",
  publisher: SITE_NAME,
  generator: "Next.js",
  applicationName: SITE_NAME,
  referrer: "origin-when-cross-origin",

  // ── Canonical & Robots ─────────────────────────────────────────────────────
  alternates: {
    canonical: SITE_URL,
  },
  robots: {
    index: true,
    follow: true,
    nocache: false,
    googleBot: {
      index: true,
      follow: true,
      noimageindex: false,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },

  // ── Open Graph ─────────────────────────────────────────────────────────────
  openGraph: {
    type: "website",
    locale: "en_US",
    url: SITE_URL,
    siteName: SITE_NAME,
    title: TITLE,
    description: DESCRIPTION,
    images: [
      {
        url: `${SITE_URL}/og-image.png`,
        width: 1200,
        height: 630,
        alt: "Guardrail.ai — Sovereign AI Governance Platform",
        type: "image/png",
      },
    ],
  },

  // ── Twitter / X Card ────────────────────────────────────────────────────────
  twitter: {
    card: "summary_large_image",
    site: "@guardrailai",
    creator: "@guardrailai",
    title: TITLE,
    description: DESCRIPTION,
    images: [`${SITE_URL}/og-image.png`],
  },

  // ── Icons ──────────────────────────────────────────────────────────────────
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      { url: "/icon-16.png", sizes: "16x16", type: "image/png" },
      { url: "/icon-32.png", sizes: "32x32", type: "image/png" },
      { url: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { url: "/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: [{ url: "/apple-touch-icon.png", sizes: "180x180" }],
    shortcut: "/favicon.ico",
  },

  // ── PWA / Manifest ─────────────────────────────────────────────────────────
  manifest: "/manifest.json",

  // ── Verification ───────────────────────────────────────────────────────────
  verification: {
    google: "iyqz7DOMDrVLAX7FK05DbY2bhx8ZULvX8C4wG9bx7hk",
  },

  // ── Category ───────────────────────────────────────────────────────────────
  category: "technology",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" dir="ltr">
      <head>
        {/* Preconnect for performance */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />

        {/* JSON-LD Structured Data — SoftwareApplication */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@graph": [
                {
                  "@type": "SoftwareApplication",
                  "@id": `${SITE_URL}/#software`,
                  name: SITE_NAME,
                  url: SITE_URL,
                  description: DESCRIPTION,
                  applicationCategory: "BusinessApplication",
                  operatingSystem: "Cloud",
                  offers: {
                    "@type": "Offer",
                    priceCurrency: "USD",
                    availability: "https://schema.org/InStock",
                    seller: {
                      "@type": "Organization",
                      name: SITE_NAME,
                      url: SITE_URL,
                    },
                  },
                  featureList: [
                    "Hardware-anchored AI constitution (EFI-locked)",
                    "Post-quantum cryptography (SPHINCS+, ML-KEM-1024)",
                    "Trinity Consensus 3-of-3 veto engine",
                    "$14.8M liability buffer (Chaos Drill 24 validated)",
                    "EU AI Act V2, DPDP-2026, NIST AI RMF compliance",
                    "Judicial-grade forensic certificates (JUD-CERT)",
                    "2-Natural-Person biometric liveness root",
                    "WORM archive — 12-month immutable audit log",
                    "Federated global immunity mesh (Mumbai, Frankfurt, US-East)",
                    "Day-Zero regulatory ingestor — autonomous mandate neutralisation",
                  ],
                  aggregateRating: {
                    "@type": "AggregateRating",
                    ratingValue: "5",
                    bestRating: "5",
                    ratingCount: "96",
                    reviewCount: "24",
                  },
                },
                {
                  "@type": "Organization",
                  "@id": `${SITE_URL}/#organization`,
                  name: SITE_NAME,
                  url: SITE_URL,
                  logo: {
                    "@type": "ImageObject",
                    url: `${SITE_URL}/icon-512.png`,
                    width: 512,
                    height: 512,
                  },
                  sameAs: [
                    "https://twitter.com/guardrailai",
                    "https://linkedin.com/company/guardrailai",
                    "https://github.com/guardrailai",
                  ],
                  description:
                    "Guardrail.ai is the world's first hardware-anchored, post-quantum sovereign AI governance platform, purpose-built for enterprise agentic AI safety and regulatory compliance.",
                  foundingDate: "2025",
                  knowsAbout: [
                    "AI Governance",
                    "AI Safety",
                    "Post-Quantum Cryptography",
                    "Regulatory Compliance",
                    "Agentic AI",
                    "Enterprise Risk Management",
                  ],
                },
                {
                  "@type": "WebSite",
                  "@id": `${SITE_URL}/#website`,
                  url: SITE_URL,
                  name: SITE_NAME,
                  description: DESCRIPTION,
                  publisher: { "@id": `${SITE_URL}/#organization` },
                  potentialAction: {
                    "@type": "SearchAction",
                    target: {
                      "@type": "EntryPoint",
                      urlTemplate: `${SITE_URL}/?q={search_term_string}`,
                    },
                    "query-input": "required name=search_term_string",
                  },
                },
                {
                  "@type": "WebPage",
                  "@id": `${SITE_URL}/#webpage`,
                  url: SITE_URL,
                  name: TITLE,
                  isPartOf: { "@id": `${SITE_URL}/#website` },
                  about: { "@id": `${SITE_URL}/#software` },
                  description: DESCRIPTION,
                  breadcrumb: {
                    "@type": "BreadcrumbList",
                    itemListElement: [
                      {
                        "@type": "ListItem",
                        position: 1,
                        name: "Home",
                        item: SITE_URL,
                      },
                    ],
                  },
                },
                {
                  "@type": "FAQPage",
                  "@id": `${SITE_URL}/#faq`,
                  mainEntity: [
                    {
                      "@type": "Question",
                      name: "What is Guardrail.ai?",
                      acceptedAnswer: {
                        "@type": "Answer",
                        text: "Guardrail.ai is the world's first hardware-anchored, post-quantum sovereign AI governance platform. It provides a Trinity Consensus veto engine, $14.8M liability buffer, and judicial-grade audit certificates for enterprise agentic AI deployments.",
                      },
                    },
                    {
                      "@type": "Question",
                      name: "Is Guardrail.ai compliant with EU AI Act and NIST?",
                      acceptedAnswer: {
                        "@type": "Answer",
                        text: "Yes. Guardrail.ai autonomously ingests and neutralises mandates including EU AI Act V2, DPDP-2026, NIST AI RMF, SEC-800-REV3, BaFin AI Governance 2025, and RBI AI Governance Framework via its Day-Zero Ingestor and Shadow Amendment protocol.",
                      },
                    },
                    {
                      "@type": "Question",
                      name: "What makes Guardrail.ai different from other AI safety platforms?",
                      acceptedAnswer: {
                        "@type": "Answer",
                        text: "Guardrail.ai is the only platform with hardware-locked constitutional AI (EFI-level), post-quantum cryptography (SPHINCS+), 3-of-3 Trinity Consensus veto, 2-Natural-Person biometric liveness root, and a $10B-validated Chaos Drill track record — all in a single sovereign mesh.",
                      },
                    },
                    {
                      "@type": "Question",
                      name: "How fast is the AI veto decision?",
                      acceptedAnswer: {
                        "@type": "Answer",
                        text: "Guardrail.ai's OODA loop completes in under 2.1ms P99 latency — from agent intent observation to hard block and JUD-CERT issuance. A $10B treasury diversion was vetoed in 0.004 seconds during Chaos Drill 23.",
                      },
                    },
                  ],
                },
              ],
            }),
          }}
        />
      </head>
      <body className="antialiased sovereign-scanline" suppressHydrationWarning>
        <a href="#main-content" className="skip-link">Skip to main content</a>
        {children}
      </body>
    </html>
  );
}
