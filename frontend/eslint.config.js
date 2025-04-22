// @ts-check
const eslint = require("@eslint/js")
const tseslint = require("typescript-eslint")
const angular = require("angular-eslint")
const unusedImports = require("eslint-plugin-unused-imports")

module.exports = tseslint.config(
  {
    files: ["**/*.ts"],
    plugins: {
      // @ts-ignore
      "unused-imports": unusedImports
    },
    extends: [
      eslint.configs.recommended,
      ...tseslint.configs.recommended,
      ...tseslint.configs.stylistic,
      ...angular.configs.tsRecommended
    ],
    processor: angular.processInlineTemplates,
    rules: {
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": "off",
      "unused-imports/no-unused-imports": "error",
      "unused-imports/no-unused-vars": [
        "warn",
        {
          vars: "all",
          varsIgnorePattern: "^_",
          args: "after-used",
          argsIgnorePattern: "^_"
        }
      ]
    }
  },
  {
    files: ["**/*.html"],
    extends: [
      ...angular.configs.templateRecommended,
      ...angular.configs.templateAccessibility
    ],
    rules: {}
  }
)
