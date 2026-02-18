import * as React from 'react';

import {render, screen} from '@testing-library/react-native';

import {_ColorPalette} from '../_ColorPalette';

describe('Test ColorPalette', () => {
  test('Should match snapshot correctly.', async () => {
    render(<_ColorPalette />);
    expect(screen).toMatchSnapshot();
  });
});
