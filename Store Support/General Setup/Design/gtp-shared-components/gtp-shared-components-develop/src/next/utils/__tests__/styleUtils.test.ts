import {Animated} from 'react-native';

import {interpolateStyles} from '../styleUtils';

describe('theme utils', () => {
  describe('interpolateStyles', () => {
    test('It should not throw with empty parameters.', () => {
      expect(() =>
        interpolateStyles(new Animated.Value(0), undefined, undefined),
      ).not.toThrow();
    });

    test('It should return interpolated values.', () => {
      const response = interpolateStyles(
        new Animated.Value(0),
        {
          backgroundColor: '#000',
          borderRadius: 8,
        },
        {
          backgroundColor: '#fff',
        },
      );

      expect(response).toHaveProperty('interpolated');
      expect(response).toHaveProperty('cleaned', {borderRadius: 8});
    });

    test('It should apply an interpolation.', () => {
      const interpolator = {
        interpolate: jest.fn(),
      };

      interpolateStyles(
        interpolator,
        {
          backgroundColor: '#000',
          padding: 0,
        },
        {
          backgroundColor: '#fff',
          padding: 4,
        },
      );

      expect(interpolator.interpolate).toHaveBeenCalledTimes(2);

      expect(interpolator.interpolate).toHaveBeenCalledWith({
        inputRange: [0, 1],
        outputRange: ['#000', '#fff'],
      });

      expect(interpolator.interpolate).toHaveBeenCalledWith({
        inputRange: [0, 1],
        outputRange: [0, 4],
      });
    });
  });
});
