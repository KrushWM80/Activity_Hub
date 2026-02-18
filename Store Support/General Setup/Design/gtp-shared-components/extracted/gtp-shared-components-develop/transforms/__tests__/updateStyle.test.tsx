import {defineTest} from 'jscodeshift/src/testUtils';

describe('Update Style', () => {
  //@ts-ignore
  defineTest(__dirname, './updateStyle', null, './updateStyle-type1', {
    parser: 'tsx',
  });

  //@ts-ignore
  defineTest(__dirname, './updateStyle', null, './updateStyle-type2', {
    parser: 'tsx',
  });

  //@ts-ignore
  defineTest(__dirname, './updateStyle', null, './updateStyle-type3', {
    parser: 'tsx',
  });

  //@ts-ignore
  defineTest(__dirname, './updateStyle', null, './updateStyle-type4', {
    parser: 'tsx',
  });

  //@ts-ignore
  defineTest(__dirname, './updateStyle', null, './updateStyle-type5', {
    parser: 'tsx',
  });
});
