import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: "#0a0a0f",
          secondary: "#0f0f15",
        },
        panel: {
          DEFAULT: "#111118",
          hover: "#16161f",
          active: "#1a1a25",
        },
        border: {
          DEFAULT: "#222",
          strong: "#2a2a35",
          subtle: "#1a1a22",
        },
        accent: {
          DEFAULT: "#00d4ff",
          hover: "#33dfff",
          muted: "#0099cc",
        },
        sev: {
          critical: "#ff1744",
          high: "#ff6b35",
          medium: "#ffc400",
          low: "#2979ff",
          info: "#00c853",
        },
        status: {
          danger: "#ff1744",
          warning: "#ffc400",
          info: "#2979ff",
          success: "#00c853",
        },
        fg: {
          DEFAULT: "#e6e6ee",
          muted: "#8a8a99",
          subtle: "#5a5a6a",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      boxShadow: {
        glow: "0 0 24px rgba(0, 212, 255, 0.15)",
        panel: "0 4px 16px rgba(0, 0, 0, 0.4)",
      },
      keyframes: {
        "fade-in": {
          "0%": { opacity: "0", transform: "translateY(4px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "pulse-accent": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.5" },
        },
      },
      animation: {
        "fade-in": "fade-in 200ms ease-out",
        "pulse-accent": "pulse-accent 2s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;
