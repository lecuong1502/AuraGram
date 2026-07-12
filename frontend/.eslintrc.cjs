module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
  ],
  settings: {
    react: { version: "18.3" },
    "import/resolver": {
      alias: {
        map: [["@", "./src"]],
        extensions: [".js", ".jsx"],
      },
    },
  },
  rules: {
    "react/prop-types": "warn",
    "react/react-in-jsx-scope": "off",
    "no-unused-vars": "warn",
  },
};