module.exports = {
  preset: "jest-preset-angular",
  setupFilesAfterEnv: ["<rootDir>/setup-jest.ts"],
  globalSetup: "jest-preset-angular/global-setup",
  testPathIgnorePatterns: ["<rootDir>/node_modules/", "<rootDir>/dist/"],
  coverageDirectory: "./coverage",
  coverageReporters: ["html", "lcov", "text-summary"],
  collectCoverageFrom: [
    "src/**/*.ts",
    "!src/**/*.module.ts",
    "!src/main.ts",
    "!src/environments/*.ts",
    "!src/**/*.stories.ts",
    "!src/**/*.spec.ts"
  ]
}
