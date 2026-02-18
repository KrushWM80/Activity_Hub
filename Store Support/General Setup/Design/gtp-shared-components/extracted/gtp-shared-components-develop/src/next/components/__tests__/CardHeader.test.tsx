import * as React from 'react';

import {render} from '@testing-library/react-native';

import {CardHeader} from '../CardHeader';

describe('Testing CardMedia', () => {
  it('should display correctly', () => {
    const component = render(<CardHeader title="This is the header" />);
    // @ts-ignore
    expect(component).toMatchSnapshot();
  });
});
