# Web App ReadMe Info

# Overview

With my extensive board and card game collection I am often asked for recommendations. I wanted to create this software to make it easier to find recommendations that match various people's preferences. I decided for this school module to learn more about Web Applications and improve upon my Typescript project. I also wanted to connect a database so I could have experience with that.

[Software Demo Video](https://youtu.be/0_HLeavMLDo)

# Web Pages

The pages that I have are an intro page to select one of the two quiz styles and then the quiz pages. They are simply navigated to by button press updating the URL and I tried to implement a restart for my adventure quiz so it didn't need to reload the page.

# Development Environment

- Vite
- React
- Tailwind
- ESLint
- Supabase

I used Typescript as the main language for this program.

# Useful Websites

- [TypeScript Documention](https://www.typescriptlang.org/)
- [What is Typescript](https://www.contentful.com/blog/what-is-typescript-and-why-should-you-use-it/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Supabase Site](https://supabase.com/)

# Future Work

- Greatly enhance the database entries so that more options are available
- Implement MVC for React
- Expand the available adventure stories

# Getting Started

1. Clone the repository

   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. Install dependencies

   npm install

   # or

   yarn install

3. Configure environment variables
   1. Copy the example file:

      cp .env.example .env

   2. Fill in your Supabase project info:

      # Safe for frontend

      VITE_SUPABASE_URL=https://your-project.supabase.co
      VITE_SUPABASE_ANON_KEY=your-anon-key

      # Secret key for backend (service role)

      SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

   ⚠ Important: Do NOT expose the SUPABASE*SERVICE_ROLE_KEY in frontend code. Only the VITE* prefixed variables are safe for React/Vite apps.

4. Run the project

   npm run dev

   # or

   yarn dev
   - Frontend will automatically pick up VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY.
   - Backend (if any) can access SUPABASE_SERVICE_ROLE_KEY via process.env.SUPABASE_SERVICE_ROLE_KEY.

5. Add new contributors
   - Make sure contributors also copy .env.example and fill in their own keys.
   - Never commit your .env file — it is already ignored via .gitignore.

# TypeScript ReadMe Info

# Overview

With my extensive board and card game collection I am often asked for recommendations. I wanted to create this software to make it easier to find recommendations that match various people's preferences. I decided for this school module to learn more about the Typescript language. I also wanted to have more of a UI interface since my last project was just a console application.

[Software Demo Video](https://youtu.be/iju-knFiSTA)

# Development Environment

- Vite
- React
- Tailwind
- ESLint

I used Typescript as the main language for this program.

# Useful Websites

- [TypeScript Documention](https://www.typescriptlang.org/)
- [What is Typescript](https://www.contentful.com/blog/what-is-typescript-and-why-should-you-use-it/)
- [Tailwind CSS](https://tailwindcss.com/)

# Future Work

- Connect to a database so that the games aren't just stored in a local file
- Expand the list of game recommendations
- Add a Random button that will randomize the answers to all the questions at one time

# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default defineConfig([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs["recommended-typescript"],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```
