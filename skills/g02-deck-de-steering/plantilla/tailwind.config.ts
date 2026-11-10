import type { Config } from 'tailwindcss';

// Zest "Citrus" tokens, from design/uploads/zest-wireframe-design/app/globals.css.
// Colors are CSS variables (src/styles/tokens.css) so a theme can swap them.
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        background: 'rgb(var(--background) / <alpha-value>)',
        foreground: 'rgb(var(--foreground) / <alpha-value>)',
        card: 'rgb(var(--card) / <alpha-value>)',
        muted: 'rgb(var(--muted) / <alpha-value>)',
        'muted-foreground': 'rgb(var(--muted-foreground) / <alpha-value>)',
        border: 'rgb(var(--border) / <alpha-value>)',
        grapefruit: 'rgb(var(--grapefruit) / <alpha-value>)',
        coral: 'rgb(var(--coral) / <alpha-value>)',
        lemon: 'rgb(var(--lemon) / <alpha-value>)',
        lime: 'rgb(var(--lime) / <alpha-value>)',
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        sans: ['Geist', 'system-ui', 'sans-serif'],
        mono: ['"Geist Mono"', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
} satisfies Config;
