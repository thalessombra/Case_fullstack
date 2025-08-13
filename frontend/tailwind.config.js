/** @type {import('tailwindcss').Config} */
const tailwindAnimate = import("tailwindcss-animate");

module.exports = {
  content: [
    "./app/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: { extend: {} },
  plugins: [tailwindAnimate],
};
