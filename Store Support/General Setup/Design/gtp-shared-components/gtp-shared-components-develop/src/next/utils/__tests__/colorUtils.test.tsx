import * as utils from '../';

describe('Test formatColor', () => {
  test('gray160, should return #2e2f32', () => {
    expect(utils.formatColor('gray160')).toEqual('#2e2f32');
  });
  test('black, should return #000', () => {
    expect(utils.formatColor('black')).toEqual('#000');
  });
});
