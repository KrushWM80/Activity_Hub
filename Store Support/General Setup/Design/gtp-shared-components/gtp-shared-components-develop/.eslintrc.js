module.exports = {
  root: true,
  extends: ['@react-native'],
  ignorePatterns: [
    'dist/',
    'docs/',
    'website/',
    'coverage/',
    'transforms/__testfixtures__/',
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint', 'import'],
  overrides: [
    {
      files: ['*.ts', '*.tsx'],
      rules: {
        '@typescript-eslint/no-shadow': ['error'],
        '@typescript-eslint/no-unused-vars': [
          'error',
          {
            argsIgnorePattern: '^_',
            ignoreRestSiblings: true,
          },
        ],
        'no-console': 'error',
        // this is for sorting WITHIN an import
        'sort-imports': [
          'error',
          {ignoreCase: true, ignoreDeclarationSort: true},
        ],
        // this is for sorting imports
        'import/order': [
          'error',
          {
            groups: [
              ['external', 'builtin'],
              'internal',
              'parent',
              'sibling',
              'index',
            ],
            pathGroups: [
              {
                pattern: '@(react|react-native)',
                group: 'external',
                position: 'before',
              },
              {
                pattern: '@src/**',
                group: 'internal',
              },
            ],
            pathGroupsExcludedImportTypes: ['internal', 'react'],
            'newlines-between': 'always',
            alphabetize: {
              order: 'asc',
              caseInsensitive: true,
            },
          },
        ],
      },
    },
  ],
};
