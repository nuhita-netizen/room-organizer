/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary-rose': '#ce6b7f',
        'soft-blush': '#fae5e5',
        'deep-maroon': '#3d2327',
        'clean-white': '#ffffff',
        'warm-sand': '#fbf2eb',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Nunito', 'sans-serif'],
        display: ['Quicksand', 'sans-serif'],
      },
      borderRadius: {
        'xl': '24px',
        '2xl': '32px',
        'full': '9999px',
      },
      boxShadow: {
        'rose': '0 8px 24px rgba(206, 107, 127, 0.3)',
        'soft': '0 12px 40px rgba(61, 35, 39, 0.05)',
      }
    },
  },
  plugins: [],
}
