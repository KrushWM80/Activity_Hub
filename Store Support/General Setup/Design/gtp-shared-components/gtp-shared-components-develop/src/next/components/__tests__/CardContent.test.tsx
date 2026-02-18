import * as React from 'react';

import {render} from '@testing-library/react-native';

import {CardContent} from '../CardContent';

describe('Testing CardMedia', () => {
  it('should display correctly', () => {
    const component = render(<CardContent>This is the content</CardContent>);
    expect(component).toMatchSnapshot();
  });
});
