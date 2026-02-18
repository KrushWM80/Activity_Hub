import * as React from 'react';
import {TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Text';
import {render} from '@testing-library/react-native';

import {formatColor, TypographyColors} from '../../utils';
import {Display, DisplaySize, DisplayWeight} from '../Display';

test('Should match snapshot of Display with default props.', async () => {
  const display = render(<Display>Test Children</Display>);
  expect(display).toMatchSnapshot();
});

describe.each<DisplaySize>(['large', 'small'])(
  'Should render Display with correct size, ',
  (size) => {
    describe.each<string>(['400', '700'])(
      'and correct weight text: ',
      (weight) => {
        test('Test Display with %s size and %s weight.', async () => {
          const rootQueries = render(
            <Display weight={weight} size={size}>
              Test Children
            </Display>,
          );
          const text = await rootQueries.findByText('Test Children');
          expect(text).toHaveStyle({
            fontSize:
              size === 'small'
                ? token.componentTextDisplaySizeSmallFontSizeBS
                : token.componentTextDisplaySizeLargeFontSizeBS,
            lineHeight:
              size === 'small'
                ? token.componentTextDisplaySizeSmallLineHeightBS
                : token.componentTextDisplaySizeLargeLineHeightBS,
            fontWeight:
              weight === '400'
                ? token.componentTextDisplayWeight400FontWeight.toString()
                : token.componentTextDisplayWeight700FontWeight.toString(),
          } as TextStyle);
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
] as Array<DisplayWeight>;
describe.each<DisplayWeight>(weights)(
  'Should provide backward compatibility for depricated weights: ',
  (weight) => {
    test('Test Display with deprecated %s weight.', async () => {
      const rootQueries = render(
        <Display weight={weight}>Test Children</Display>,
      );
      const text = await rootQueries.findByText('Test Children');
      expect(text).toHaveStyle({
        fontWeight: ['thin', 'light', 'normal'].includes(weight)
          ? token.componentTextDisplayWeight400FontWeight.toString()
          : token.componentTextDisplayWeight700FontWeight.toString(),
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
describe.each<TypographyColors>(colors)('Test %s Display: ', (color) => {
  test('Should match with %s color.', async () => {
    const rootQueries = render(<Display color={color}>Test Children</Display>);
    const text = await rootQueries.findByText('Test Children');
    const localColor = formatColor(color) as TypographyColors;
    expect(text).toHaveStyle({
      color: localColor,
    });
  });
});
