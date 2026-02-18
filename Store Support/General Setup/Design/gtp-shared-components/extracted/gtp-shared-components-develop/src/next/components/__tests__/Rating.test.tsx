import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Rating';
import {render} from '@testing-library/react-native';

import {Rating, RatingSize} from '../Rating';

describe.each<RatingSize>(['small', 'large'])(
  'Should render Rating correctly for size',
  (size) => {
    test(`Test Rating size="${size} with 2`, async () => {
      const wrapper = render(<Rating size={size} value={2} />);
      const iconSize =
        size === 'small' ? token.componentRatingIconSizeSmallHeight : 24;
      const starIcon = await wrapper.findAllByTestId('StarFillIcon');
      expect(starIcon[0]).toHaveStyle({
        height: iconSize,
        width: iconSize,
        tintColor: token.componentRatingIconVariantFilledBackgroundColor,
      });
      const halfIcon = wrapper.queryAllByTestId('StarHalfIcon');
      expect(halfIcon.length).toEqual(0);
    });
    test(`Test Rating size="${size} with 3.5`, async () => {
      const wrapper = render(<Rating size={size} value={3.5} />);
      const iconSize =
        size === 'small' ? token.componentRatingIconSizeSmallHeight : 24;
      const starIcon = await wrapper.findAllByTestId('StarFillIcon');
      expect(starIcon[0]).toHaveStyle({
        height: iconSize,
        width: iconSize,
        tintColor: token.componentRatingIconVariantFilledBackgroundColor,
      });
      const halfIcon = wrapper.queryAllByTestId('StarHalfIcon');
      expect(halfIcon.length).toEqual(1);
    });
    test(`Test Rating size="${size} with 0`, async () => {
      const wrapper = render(<Rating size={size} />);
      const iconSize =
        size === 'small' ? token.componentRatingIconSizeSmallHeight : 24;
      const starIcon = await wrapper.findAllByTestId('StarIcon');
      expect(starIcon[0]).toHaveStyle({
        height: iconSize,
        width: iconSize,
        tintColor: token.componentRatingIconVariantFilledBackgroundColor,
      });
      const fillIcon = wrapper.queryAllByTestId('StarFillIcon');
      expect(fillIcon.length).toEqual(0);
      const halfIcon = wrapper.queryAllByTestId('StarHalfIcon');
      expect(halfIcon.length).toEqual(0);
    });
  },
);
