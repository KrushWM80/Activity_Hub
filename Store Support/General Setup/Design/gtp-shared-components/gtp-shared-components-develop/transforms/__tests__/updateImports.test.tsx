import {defineTest} from 'jscodeshift/src/testUtils';

describe('Update Imports', () => {
  //@ts-ignore
  defineTest(__dirname, './updateImports', null, './updateImports-type1', {
    parser: 'tsx',
  });

  //@ts-ignore
  defineTest(__dirname, './updateImports', null, './updateImports-type2', {
    parser: 'tsx',
  });

  //@ts-ignore
  // Test - Ignore the files which doesn't use old gtp imports from `@walmart/gtp-shared-components/dist
  defineTest(__dirname, './updateImports', null, './updateImports-type3', {
    parser: 'tsx',
  });
});
