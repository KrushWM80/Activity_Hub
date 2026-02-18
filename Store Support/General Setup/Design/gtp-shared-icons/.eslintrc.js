module.exports = {
  root: true,
  extends: ['@react-native'],
  ignorePatterns: ['dist/', 'docs/'],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  overrides: [
    {
      files: ['*.ts', '*.tsx'],
      rules: {
        '@typescript-eslint/no-shadow': ['error'],
        'no-console': 'error',
      },
    },
  ],
};
