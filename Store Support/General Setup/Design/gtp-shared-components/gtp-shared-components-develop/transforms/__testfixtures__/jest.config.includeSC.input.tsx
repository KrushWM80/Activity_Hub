// @ts-nocheck
module.exports = {
  preset: 'react-native',
  roots: ['<rootDir>/__tests__'],
  setupFiles: ['<rootDir>/__tests__/setup.ts'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  coverageReporters: ['lcov', 'text'],
  testResultsProcessor: 'jest-sonar-reporter',
  collectCoverageFrom: [
    '<rootDir>/src/**/*.{js,jsx,ts,tsx}',
    '<rootDir>/src/**/index.{ts,tsx}',
    '!<rootDir>/src/*.{ts,tsx}',
    '!<rootDir>/src/returns/containers/index.ts',
    '!<rootDir>/src/returns/transforms/index.ts',
    '!<rootDir>/src/returns/actionTypes.ts',
    '!<rootDir>/src/returns/services/print/**/*.*',
    '!<rootDir>/src/returns/utils/telemetry/index.ts',
    '!<rootDir>/src/returns/config/index.ts',
  ],
  modulePathIgnorePatterns: [
    '<rootDir>/src/returns/styles/',
    '<rootDir>/src/returns/index.ts',
    '<rootDir>/src/index.tsx',
    '<rootDir>/src/types.ts',
    '<rootDir>/src/ui-components.d.ts',
    '<rootDir>/src/functional-components.d.ts',
  ],
  coverageThreshold: {
    global: {
      statements: 90,
      branches: 90,
      functions: 90,
      lines: 90,
    },
  },
  transformIgnorePatterns: [
    '<rootDir>/node_modules/(?!(react-native|@react-native|@livingdesign|@react-native-community/datetimepicker|@walmart/gtp-shared-components|@react-native-community/picker|@walmart/react-native-logger|@walmart/redux-store|@react-native-firebase|react-native-iphone-x-helper|react-native-gesture-handler|@react-native/polyfills|@react-native/normalize-color|@walmart/ui-components)|@walmart/core-services)',
  ],
  testPathIgnorePatterns: [
    '/node_modules/',
    '<rootDir>/__tests__/setup.ts',
    '<rootDir>/__tests__/__mocks__/',
  ],
  moduleNameMapper: {
    '@walmart/gtp-shared-components':
      '<rootDir>/__tests__/__mocks__/@walmart/gtp-shared-components.js',
  },
};