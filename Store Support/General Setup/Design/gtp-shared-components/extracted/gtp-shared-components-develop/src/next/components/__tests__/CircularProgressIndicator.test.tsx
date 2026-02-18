import * as React from 'react';

import {render, screen} from '@testing-library/react-native';

import {
  CircularProgressIndicatorDirection,
  CircularProgressIndicatorOrigin,
} from '../CircularProgressIndicator';
import {CircularProgressIndicator} from '../CircularProgressIndicator';
describe.each<CircularProgressIndicatorDirection>([
  'clockwise',
  'counterclockwise',
])('CircularProgressIndicator', (fillDirection) => {
  describe.each<CircularProgressIndicatorOrigin>([
    'left',
    'top',
    'right',
    'bottom',
  ])('CircularProgressIndicator', (origin) => {
    test(`renders origin=${origin} fillDirection=${fillDirection} successfully with label`, () => {
      render(
        <CircularProgressIndicator
          value={50}
          origin={origin}
          fillDirection={fillDirection}
          color="green"
          label="test"
        />,
      );
      const element = screen.getByTestId('CircularProgressIndicator');
      const value = screen.getByTestId('CircularProgressIndicator-value');
      const label = screen.getByTestId('CircularProgressIndicator-label');
      expect(element).toBeDefined();
      expect(value.children[0]).toEqual('50%');
      expect(label.children[0]).toEqual('test');
    });
    test(`renders origin=${origin} fillDirection=${fillDirection} successfully without label`, () => {
      render(
        <CircularProgressIndicator
          value={50}
          origin={origin}
          fillDirection={fillDirection}
          color="green"
        />,
      );
      const element = screen.getByTestId('CircularProgressIndicator');
      const value = screen.getByTestId('CircularProgressIndicator-value');
      const label = screen.queryAllByTestId('CircularProgressIndicator-label');
      expect(element).toBeDefined();
      expect(value.children[0]).toEqual('50%');
      expect(label.length).toEqual(0);
    });
  });
});
