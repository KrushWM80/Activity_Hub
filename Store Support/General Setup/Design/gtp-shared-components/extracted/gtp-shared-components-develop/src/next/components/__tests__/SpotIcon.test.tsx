import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/SpotIcon';
import {render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {iconSizes} from '../../utils';
import {SpotIcon, SpotIconColor, SpotIconSize} from '../SpotIcon';

describe.each<SpotIconSize>(['small', 'large'])(
  'Should render SpotIcon correctly for size',
  (size) => {
    describe.each<SpotIconColor>(['blue', 'white'])(
      'Should render SpotIcon correctly for all colors ',
      (color) => {
        test(`Test SpotIcon size="${size} color="${color}"`, async () => {
          const wrapper = render(
            <SpotIcon size={size} color={color}>
              {<Icons.CheckIcon />}
            </SpotIcon>,
          );
          const containerSize =
            size === 'small'
              ? token.componentSpotIconContainerSizeSmallHeight
              : token.componentSpotIconContainerSizeLargeHeight;
          const iconSize =
            size === 'small' ? iconSizes.medium : iconSizes.large;

          const spotIcon = await wrapper.findByTestId('CheckIcon');
          expect(spotIcon).toHaveStyle([
            {
              height: iconSize,
              width: iconSize,
            },
          ]);

          const borderRadius =
            size === 'small'
              ? token.componentSpotIconContainerSizeSmallBorderRadius
              : token.componentSpotIconContainerSizeLargeBorderRadius;

          const spotIconContainer = await wrapper.findByTestId('SpotIcon');
          expect(spotIconContainer).toHaveStyle({
            alignItems: token.componentSpotIconContainerAlignHorizontal,
            justifyContent: token.componentSpotIconContainerAlignVertical,
            borderRadius: borderRadius,
            backgroundColor:
              color === 'blue'
                ? token.componentSpotIconContainerColorBlueBackgroundColor
                : token.componentSpotIconContainerColorWhiteBackgroundColor,
            height: containerSize,
            width: containerSize,
          });
        });
      },
    );
  },
);
