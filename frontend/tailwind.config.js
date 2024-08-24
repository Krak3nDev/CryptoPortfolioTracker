/** @type {import("tailwindcss").Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        "button-primary": "#3B82F6",
        "button-text": "#FFFFFF"
      },
      fontFamily: {
        sans: ["Roboto", "ui-sans-serif", "system-ui"]
      }
    }
  },
  plugins: []
}
