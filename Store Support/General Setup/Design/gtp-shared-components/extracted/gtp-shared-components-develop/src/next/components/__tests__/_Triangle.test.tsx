import * as React from 'react';

import {render, screen} from '@testing-library/react-native';

import {_Triangle, TriangleDirection} from '../_Triangle';

beforeEach(() => {
  jest.clearAllMocks();
});

describe.each<TriangleDirection>([
  'down',
  'down-left',
  'down-right',
  'left',
  'right',
  'up',
  'up-left',
  'up-right',
])('Test _Triangle with position ', (direction) => {
  test(`Should render correctly direction: ${direction}`, async () => {
    const width = 16,
      height = 8,
      color = 'white';
    render(
      <_Triangle
        width={width}
        height={height}
        direction={direction}
        color={'white'}
      />,
    );
    const triangle = await screen.findByTestId('_Triangle');
    if (direction === 'up') {
      expect(triangle).toHaveStyle({
        borderTopWidth: 0,
        borderRightWidth: width / 2.0,
        borderBottomWidth: height,
        borderLeftWidth: width / 2.0,
        borderTopColor: 'transparent',
        borderRightColor: 'transparent',
        borderBottomColor: color,
        borderLeftColor: 'transparent',
      });
    } else if (direction === 'right') {
      expect(triangle).toHaveStyle({
        borderTopWidth: height / 2.0,
        borderRightWidth: 0,
        borderBottomWidth: height / 2.0,
        borderLeftWidth: width,
        borderTopColor: 'transparent',
        borderRightColor: 'transparent',
        borderBottomColor: 'transparent',
        borderLeftColor: color,
      });
    } else if (direction === 'down') {
      expect(triangle).toHaveStyle({
        borderTopWidth: height,
        borderRightWidth: width / 2.0,
        borderBottomWidth: 0,
        borderLeftWidth: width / 2.0,
        borderTopColor: color,
        borderRightColor: 'transparent',
        borderBottomColor: 'transparent',
        borderLeftColor: 'transparent',
      });
    } else if (direction === 'left') {
      expect(triangle).toHaveStyle({
        borderTopWidth: height / 2.0,
        borderRightWidth: width,
        borderBottomWidth: height / 2.0,
        borderLeftWidth: 0,
        borderTopColor: 'transparent',
        borderRightColor: color,
        borderBottomColor: 'transparent',
        borderLeftColor: 'transparent',
      });
    } else if (direction === 'up-left') {
      expect(triangle).toHaveStyle({
        borderTopWidth: height,
        borderRightWidth: width,
        borderBottomWidth: 0,
        borderLeftWidth: 0,
        borderTopColor: color,
        borderRightColor: 'transparent',
        borderBottomColor: 'transparent',
        borderLeftColor: 'transparent',
      });
    } else if (direction === 'up-right') {
      expect(triangle).toHaveStyle({
        borderTopWidth: 0,
        borderRightWidth: width,
        borderBottomWidth: height,
        borderLeftWidth: 0,
        borderTopColor: 'transparent',
        borderRightColor: color,
        borderBottomColor: 'transparent',
        borderLeftColor: 'transparent',
      });
    } else if (direction === 'down-left') {
      expect(triangle).toHaveStyle({
        borderTopWidth: height,
        borderRightWidth: 0,
        borderBottomWidth: 0,
        borderLeftWidth: width,
        borderTopColor: 'transparent',
        borderRightColor: 'transparent',
        borderBottomColor: 'transparent',
        borderLeftColor: color,
      });
    } else if (direction === 'down-right') {
      expect(triangle).toHaveStyle({
        borderTopWidth: 0,
        borderRightWidth: 0,
        borderBottomWidth: height,
        borderLeftWidth: width,
        borderTopColor: 'transparent',
        borderRightColor: 'transparent',
        borderBottomColor: color,
        borderLeftColor: 'transparent',
      });
    }
  });
});
