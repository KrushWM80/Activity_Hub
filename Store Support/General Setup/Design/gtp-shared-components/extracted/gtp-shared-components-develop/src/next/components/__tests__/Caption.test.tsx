import * as React from 'react';
import {TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Text';
import {render, screen} from '@testing-library/react-native';

import {formatColor, TypographyColors} from '../../utils';
import {Caption, CaptionWeight} from '../Caption';

test('Should match snapshot of Caption with default weight.', async () => {
  const caption = render(<Caption>Caption Test</Caption>);
  expect(caption).toMatchSnapshot();
});

test('Should match snapshot of Caption with weight of 400.', async () => {
  const caption = render(<Caption weight="400">Caption Test</Caption>);
  expect(caption).toMatchSnapshot();
});

test('Should match snapshot of Caption with weight of 700.', async () => {
  const caption = render(<Caption weight="700">Caption Test</Caption>);
  expect(caption).toMatchSnapshot();
});

test('Should match snapshot of Caption with UNSAFE_style.', async () => {
  const custStyle = {
    backgroundColor: 'red',
  };
  const caption = render(
    <Caption UNSAFE_style={custStyle}>Caption Test</Caption>,
  );
  expect(caption).toMatchSnapshot();
});

const weights = [
  'thin',
  'light',
  'normal',
  'medium',
  'bold',
  'black',
] as Array<CaptionWeight>;
describe.each<CaptionWeight>(weights)(
  'Should provide backward compatibility for deprecated weights: ',
  (weight) => {
    test('Test Caption with deprecated %s weight.', async () => {
      render(<Caption weight={weight}>Caption Test</Caption>);

      const text = await screen.findByText('Caption Test');
      expect(text).toHaveStyle({
        color: token.componentTextBodyTextColor,
        fontWeight: ['thin', 'light', 'normal'].includes(weight)
          ? token.componentTextCaptionWeight400FontWeight.toString()
          : token.componentTextCaptionWeight700FontWeight.toString(),
        fontFamily: 'Bogle',
        lineHeight: token.componentTextCaptionLineHeight,
        fontStyle: 'normal',
        fontSize: token.componentTextCaptionFontSize,
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
describe.each<TypographyColors>(colors)('Test %s Caption: ', (color) => {
  test('Should match with %s color.', async () => {
    const rootQueries = render(<Caption color={color}>Test Children</Caption>);
    const text = await rootQueries.findByText('Test Children');
    const localColor = formatColor(color) as TypographyColors;
    expect(text).toHaveStyle({
      color: localColor,
    });
  });
});
