import {defineTest} from 'jscodeshift/src/testUtils';

describe('Update Jest Config', () => {
  //@ts-ignore
  defineTest(__dirname, './updateJestConfig', null, './jest.config.includeSC', {
    parser: 'tsx',
  });
  defineTest(__dirname, './updateJestConfig', null, './jest.config.NOSCSI', {
    parser: 'tsx',
  });
  defineTest(
    __dirname,
    './updateJestConfig',
    null,
    './jest.config.includeSCSI',
    {
      parser: 'tsx',
    },
  );
  defineTest(__dirname, './updateJestConfig', null, './jest.config.includeSI', {
    parser: 'tsx',
  });
});
