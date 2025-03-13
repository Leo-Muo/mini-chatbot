import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  rewrites: async () => {
    return [
      {
        source: "/api/py/:path*",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://localhost:8000/api/:path*"
            : "/api/",
      },
      {
        source: "/api/docs",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://localhost:8000/api/docs"
            : "/api/docs",
      },
      {
        source: "/api/openapi.json",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://localhost:8000/api/openapi.json"
            : "/api/openapi.json",
      },
      {
        source: "/api/chat",
        destination:
          process.env.NODE_ENV === "development"
            ? "http://localhost:8000/api/chat"
            : "/api/chat",
      },
    ];
  },
};

export default nextConfig;
