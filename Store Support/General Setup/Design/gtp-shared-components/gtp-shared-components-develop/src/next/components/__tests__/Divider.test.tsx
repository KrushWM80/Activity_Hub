import * as React from 'react';

import {render} from '@testing-library/react-native';

import {Divider} from '../Divider';

test('Should match snapshot correctly.', async () => {
  const divider = render(<Divider />);
  expect(divider).toMatchSnapshot();
});
