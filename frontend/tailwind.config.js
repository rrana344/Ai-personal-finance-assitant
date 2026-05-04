/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      },
      colors: {
        ink: "#101828",
        mint: "#31c48d",
        aqua: "#19a7ce",
        coral: "#f9735b",
        gold: "#f5b841"
      },
      boxShadow: {
        glow: "0 24px 80px rgba(25, 167, 206, 0.25)"
      }
    }
  },
  plugins: []
};
