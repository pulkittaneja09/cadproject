/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#14151b",
        surface: "#1b1c24",
        surfaceLight: "#252630",
        primary: "#b4a7fa",
        primaryLight: "#c8baff",
        accent: "#a79cf5",
        accentLight: "#c8baff",
        success: "#65c9ab",
        warning: "#d6b773",
        danger: "#e18f9d",
        gray: {
          100: "#eeeef4",
          300: "#c2c2ce",
          400: "#a1a3b2",
          500: "#8d909f",
          600: "#434450",
          700: "#30313c",
        },
      },
    },
  },
  plugins: [],
};
