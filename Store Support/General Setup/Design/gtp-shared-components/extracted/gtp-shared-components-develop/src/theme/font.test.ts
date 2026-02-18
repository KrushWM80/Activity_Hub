import {getFont, isValidWeight, isWeightValue, weights, Weights} from './font';
import * as fixtures from './font.fixtures';

describe('Test isValidWeight', () => {
  test('it returns true for valid weights', () => {
    weights.map((w) => {
      expect(isValidWeight(w)).toBeTruthy();
    });
  });
  test('it returns false for invalid weights', () => {
    ['200', '600', '800', 'bogus'].map((w) => {
      expect(isValidWeight(w)).toBeFalsy();
    });
  });
});

describe('Test isWeightValue', () => {
  test('it returns true for valid weights', () => {
    ['100', '300', '400', '500', '700', '900'].map((w) => {
      expect(isWeightValue(w)).toBeTruthy();
    });
  });
  test('it returns false for invalid weights', () => {
    [
      '200',
      '600',
      '800',
      '2000',
      'thin',
      'light',
      'medium',
      'bold',
      'black',
    ].map((w) => {
      expect(isWeightValue(w)).toBeFalsy();
    });
  });
});

describe('Test iOS fonts styles - regular', () => {
  test('Should resolve font style correctly.', () => {
    Object.keys(fixtures.expectedStylesIOS.regular).map((weight) => {
      const res = getFont(weight as Weights, false, 'ios');
      expect(res).toEqual(fixtures.expectedStylesIOS.regular[`${weight}`]);
    });
  });
  test('Should resolve font style correctly - defaults.', () => {
    const res = getFont(undefined, undefined, 'ios');
    expect(res).toEqual(fixtures.expectedStylesDefaultsIOS);
  });
});

describe('Test iOS fonts styles - monospace', () => {
  test('Should resolve font style correctly.', () => {
    Object.keys(fixtures.expectedStylesIOS.regular).map((weight) => {
      const res = getFont(weight as Weights, true, 'ios');
      expect(res).toEqual(fixtures.expectedStylesIOS.monospace[`${weight}`]);
    });
  });
});

describe('Test Android fonts styles - regular', () => {
  test('Should resolve font style correctly.', () => {
    Object.keys(fixtures.expectedStylesAndroid.regular).map((weight) => {
      const res = getFont(weight as Weights, false, 'android');
      expect(res).toEqual(fixtures.expectedStylesAndroid.regular[`${weight}`]);
    });
  });
  test('Should resolve font style correctly - defaults.', () => {
    const res = getFont(undefined, undefined, 'android');
    expect(res).toEqual(fixtures.expectedStylesDefaultsAndroid);
  });
});

describe('Test Android fonts styles - monospace', () => {
  test('Should resolve font style correctly.', () => {
    Object.keys(fixtures.expectedStylesAndroid.regular).map((weight) => {
      const res = getFont(weight as Weights, true, 'android');
      expect(res).toEqual(
        fixtures.expectedStylesAndroid.monospace[`${weight}`],
      );
    });
  });
});
