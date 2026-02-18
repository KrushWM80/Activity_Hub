module.exports = {
  setupFilesAfterEnv: ['./jest.setupFilesAfterEnv.ts'],
  collectCoverage: true,
  preset: 'react-native',
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  modulePathIgnorePatterns: ['dist/', 'example/'],
  transformIgnorePatterns: [
    'node_modules/(?!@ngrx|(?!livingdesign))',
    'jest-runner',
  ],
  testResultsProcessor: 'jest-sonar-reporter',
  collectCoverageFrom: [
    'src/**/*.{js,jsx,tsx,ts}',
    '!**/node_modules/**',
    '!**/vendor/**',
  ],
  coverageReporters: ['lcov'],
  coveragePathIgnorePatterns: ['ComponentTypes.tsx'],
  coverageProvider: 'v8',
  testTimeout: 20000,
};
