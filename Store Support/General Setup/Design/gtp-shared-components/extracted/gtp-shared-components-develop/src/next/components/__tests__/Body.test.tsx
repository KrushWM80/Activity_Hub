import * as React from 'react';
import {TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Text';
import {render, screen} from '@testing-library/react-native';

import {formatColor, TypographyColors} from '../../utils';
import {
  _getFontSize,
  _getLineHeight,
  Body,
  BodySize,
  BodyWeight,
} from '../Body';

test('Should match snapshot of Body with default props.', async () => {
  render(<Body>Test Children</Body>);
  expect(screen).toMatchSnapshot();
});

test('Should match snapshot of Body with monospace text.', async () => {
  render(<Body isMonospace>Test Children</Body>).toJSON();
  expect(screen).toMatchSnapshot();
});

describe.each<BodySize>(['large', 'medium', 'small'])(
  'Should render Body with correct size, ',
  (size) => {
    describe.each<boolean>([false, true])(
      'and correct monospace text: ',
      (mono) => {
        test('Test Body with %s size.', async () => {
          render(
            <Body size={size} isMonospace={mono}>
              Test Children
            </Body>,
          );
          const text = await screen.findByText('Test Children');
          expect(text).toHaveStyle({
            fontSize: _getFontSize(size),
            lineHeight: _getLineHeight(size),
            color: token.componentTextBodyTextColor,
            fontFamily: `Bogle${mono ? ' Mono' : ''}`,
          });
        });
      },
    );
  },
);
const weights = [
  'thin',
  'light',
  'normal',
  'medium',
  'bold',
  'black',
] as Array<BodyWeight>;
describe.each<BodyWeight>(weights)(
  'Should provide backward compatibility for deprecated weights: ',
  (weight) => {
    test('Test Body with deprecated %s weight.', async () => {
      const rootQueries = render(<Body weight={weight}>Test Children</Body>);
      const text = await rootQueries.findByText('Test Children');
      expect(text).toHaveStyle({
        fontWeight: ['thin', 'light', 'normal'].includes(weight)
          ? token.componentTextCaptionWeight400FontWeight.toString()
          : token.componentTextCaptionWeight700FontWeight.toString(),
      } as TextStyle);
    });
  },
);

const colors = [
  'black',
  'blue5',
  'gray5',
  'orange110',
  'green5',
  'pink5',
  'purple5',
  'red5',
  'spark5',
  'yellow5',
  'white',
] as Array<TypographyColors>;
describe.each<TypographyColors>(colors)('Test %s Body: ', (color) => {
  test('Should match with %s color.', async () => {
    const rootQueries = render(<Body color={color}>Test Children</Body>);
    const text = await rootQueries.findByText('Test Children');
    const localColor = formatColor(color) as TypographyColors;
    expect(text).toHaveStyle({
      color: localColor,
    });
  });
});
