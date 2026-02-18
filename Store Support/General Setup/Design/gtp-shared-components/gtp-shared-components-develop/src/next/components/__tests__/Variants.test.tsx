import * as React from 'react';

import {render} from '@testing-library/react-native';
import {getHostChildren} from '@testing-library/react-native/build/helpers/component-tree';

import {colors} from '../../utils';
import {Variants} from '../Variants';

test('Test Variants with more than 4 colors', async () => {
  const rootQueries = render(
    <Variants
      variants={[
        colors.blue['100'],
        colors.green['100'],
        colors.red['100'],
        colors.spark['100'],
        colors.purple['100'],
        colors.pink['100'],
      ]}
    />,
  );

  const variants = await rootQueries.findByTestId('Variants');

  expect(variants).toHaveStyle({
    alignSelf: 'center',
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
  });

  // Expect Variant 1 Styling
  expect(getHostChildren(variants)[0]).toHaveStyle({
    height: 8,
    width: 8,
    marginVertical: 4,
    borderRadius: 4,
    backgroundColor: colors.blue['100'],
    marginRight: 8,
    flexDirection: 'row',
  });

  // Expect Variant 2 Styling
  expect(getHostChildren(variants)[1]).toHaveStyle({
    height: 8,
    width: 8,
    marginVertical: 4,
    borderRadius: 4,
    backgroundColor: colors.green['100'],
    marginRight: 8,
    flexDirection: 'row',
  });

  // Expect Variant 3 Styling
  expect(getHostChildren(variants)[2]).toHaveStyle({
    height: 8,
    width: 8,
    marginVertical: 4,
    borderRadius: 4,
    backgroundColor: colors.red['100'],
    marginRight: 8,
    flexDirection: 'row',
  });

  const remainingCaption = getHostChildren(variants)[4];
  // Expect Caption Styling
  expect(remainingCaption).toHaveStyle({
    fontSize: 12,
    lineHeight: 16,
    color: '#74767c',
  });

  const remainingCaptionText = `${remainingCaption.children[0]}${remainingCaption.children[1]}`;

  // Expect Remaining Caption = +2 (If Number of Variants > MaxVariants(4).
  // Append Remaining Caption after MaxVariants.
  expect(remainingCaptionText).toEqual('+2');
});

test('Test Variants with no colors', async () => {
  const rootQueries = render(
    <Variants
      variants={[
        colors.blue['100'],
        colors.green['100'],
        colors.red['100'],
        colors.spark['100'],
        colors.purple['100'],
        colors.pink['100'],
      ]}
      colors={false}
    />,
  );

  const optionsCaption = await rootQueries.findByTestId('Body');
  const optionsCaptionText = `${optionsCaption.children[0]}${optionsCaption.children[1]}`;

  // Expect to display the number of options.
  expect(optionsCaptionText).toEqual('6 options');
});
