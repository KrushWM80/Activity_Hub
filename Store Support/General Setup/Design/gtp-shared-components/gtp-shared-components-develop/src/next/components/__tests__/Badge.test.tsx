import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Badge';
import {render} from '@testing-library/react-native';
import renderer from 'react-test-renderer';

import {Badge} from '../Badge';

type BadgeColor =
  | 'blue'
  | 'gray'
  | 'green'
  | 'purple'
  | 'red'
  | 'spark'
  | 'white';

describe.each<BadgeColor>([
  'blue',
  'gray',
  'green',
  'purple',
  'red',
  'spark',
  'white',
])('Test %s Badge', (color) => {
  test('Should match snapshot correctly.', async () => {
    const spinner = renderer.create(<Badge color={color} />).toJSON();
    expect(spinner).toMatchSnapshot();
  });

  test('Should render text correctly.', async () => {
    const rootQueries = render(<Badge color={color}>Test</Badge>);
    const badge = await rootQueries.findByTestId('Badge');
    const iconElement = await rootQueries.findByText('Test');
    expect(badge).toContainElement(iconElement);
  });

  test('Should render style correctly.', async () => {
    const rootQueries = render(<Badge color={color}>Test</Badge>);
    const text = await rootQueries.findByText('Test');

    expect(text).toHaveStyle({
      fontSize: token.componentBadgeTextLabelFontSize,
      lineHeight: token.componentBadgeTextLabelLineHeight,
      marginTop: color === 'spark' || color === 'white' ? -1 : undefined,
    });
  });
});
