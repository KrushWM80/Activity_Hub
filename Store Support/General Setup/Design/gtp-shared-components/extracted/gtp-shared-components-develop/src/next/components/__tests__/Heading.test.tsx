import * as React from 'react';
import {TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Text';
import {render, screen} from '@testing-library/react-native';

import {formatColor, TypographyColors} from '../../utils';
import {_getFontSize, _getLineHeight, Heading, HeadingSize} from '../Heading';

test('Should match snapshot of Heading with default props.', async () => {
  const heading = render(<Heading>Test Children</Heading>);
  expect(heading).toMatchSnapshot();
});

describe('Heading renders correctly with defaults', () => {
  test('should render correctly', () => {
    render(<Heading>Test heading with defaults</Heading>);

    const heading = screen.getByText('Test heading with defaults');
    expect(heading).toHaveStyle({
      color: '#2e2f32',
      fontFamily: 'Bogle',
      fontSize: 20,
      fontStyle: 'normal',
      fontWeight: '700',
      lineHeight: 28,
    });
  });
});

describe.each<HeadingSize>(['large', 'small'])(
  'Should render Heading with correct size %s, ',
  (size) => {
    describe.each<string>(['400', '700'])(
      'and correct weight %s: ',
      (weight) => {
        test(`Test Heading with size ${size} and weight ${weight}.`, () => {
          render(
            <Heading weight={weight} size={size}>
              Test Children
            </Heading>,
          );
          const text = screen.getByText('Test Children');
          expect(text).toHaveStyle({
            fontSize: _getFontSize(size),
            lineHeight: _getLineHeight(size),
            fontWeight:
              weight === '400'
                ? token.componentTextHeadingWeight400FontWeight.toString()
                : token.componentTextHeadingWeight700FontWeight.toString(),
          } as TextStyle);
        });
      },
    );
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
describe.each<TypographyColors>(colors)('Test %s Heading: ', (color) => {
  test('Should match with %s color.', async () => {
    const rootQueries = render(<Heading color={color}>Test Children</Heading>);
    const text = await rootQueries.findByText('Test Children');
    const localColor = formatColor(color) as TypographyColors;
    expect(text).toHaveStyle({
      color: localColor,
    });
  });
});
