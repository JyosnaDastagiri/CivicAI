/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        civic: {
          50: "#eef4fb",
          100: "#d7e6f5",
          200: "#b0cdeb",
          300: "#83b1de",
          400: "#5493d0",
          500: "#2f75b8",
          600: "#215d97",
          700: "#1a4a79",
          800: "#173e63",
          900: "#153452",
        },
      },
    },
  },
  plugins: [],
};
