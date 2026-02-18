module.exports = {
  preset: 'react-native',
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  modulePathIgnorePatterns: ['dist/', 'example/', '.tmp/'],
  transformIgnorePatterns: [
    'node_modules/(?!@ngrx|(?!livingdesign))',
    'jest-runner',
  ],
};
