import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // ── HTTP Security & SEO Headers ──────────────────────────────────────────
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          // ── Core Security ───────────────────────────────────────────────
          {
            key: "X-Frame-Options",
            value: "SAMEORIGIN",
          },
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
          {
            key: "X-XSS-Protection",
            value: "1; mode=block",
          },
          {
            key: "Referrer-Policy",
            value: "strict-origin-when-cross-origin",
          },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=(), interest-cohort=()",
          },
          {
            key: "Strict-Transport-Security",
            value: "max-age=63072000; includeSubDomains; preload",
          },
          // ── Robots / Crawlers ───────────────────────────────────────────
          {
            key: "X-Robots-Tag",
            value: "index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1",
          },
          // ── Performance ─────────────────────────────────────────────────
          {
            key: "X-DNS-Prefetch-Control",
            value: "on",
          },
        ],
      },
      // ── Static assets: long-term caching ─────────────────────────────────
      {
        source: "/(_next/static|fonts|images)/(.*)",
        headers: [
          {
            key: "Cache-Control",
            value: "public, max-age=31536000, immutable",
          },
        ],
      },
    ];
  },

  // ── Image optimisation ───────────────────────────────────────────────────
  images: {
    formats: ["image/avif", "image/webp"],
    minimumCacheTTL: 86400,
  },

  // ── Compression ──────────────────────────────────────────────────────────
  compress: true,

  // ── Power-user: trailing slash normalisation ─────────────────────────────
  trailingSlash: false,
};

export default nextConfig;
