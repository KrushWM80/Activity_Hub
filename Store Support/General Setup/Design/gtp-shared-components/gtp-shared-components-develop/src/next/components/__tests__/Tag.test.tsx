import * as React from 'react';
import {TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Tag';
import {render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {iconSizes, IconSizesKey} from '../../utils';
import {Tag, TagColor, TagVariant, variantStyles} from '../Tag';

jest.useFakeTimers({legacyFakeTimers: true});

describe.each<TagVariant>(['primary', 'secondary', 'tertiary'])(
  'Should render Tag correctly for Variants',
  (variant) => {
    describe.each<TagColor>([
      'red',
      'spark',
      'green',
      'blue',
      'purple',
      'gray',
    ])('Should render Tag correctly for all colors ', (color) => {
      test(`Test Tag variant="${variant} color="${color}"`, async () => {
        const wrapper = render(
          <Tag variant={variant} color={color} leading={<Icons.CheckIcon />}>
            {`Tag variant="${variant} color="${color}"`}
          </Tag>,
        );
        const tagIcon = await wrapper.findByTestId('CheckIcon');
        expect(tagIcon).toHaveStyle([
          {
            height:
              iconSizes[token.componentTagLeadingIconIconSize as IconSizesKey],
            width:
              iconSizes[token.componentTagLeadingIconIconSize as IconSizesKey],
            tintColor: variantStyles[variant][color].tintColor,
          },
          {
            marginRight: token.componentTagLeadingIconMarginEnd,
          },
        ]);

        const tagText = await wrapper.findByTestId('Tag-content');
        expect(tagText).toHaveStyle({
          fontFamily: 'Bogle',
          fontWeight: token.componentTagTextLabelFontWeight.toString(),
          fontStyle: 'normal',
          fontSize: token.componentTagTextLabelFontSize,
          color: variantStyles[variant][color].textColor,
        } as TextStyle);

        const TagTextLabel = await wrapper.findByTestId('Tag');
        expect(TagTextLabel).toHaveStyle({
          flexDirection: 'row',
          alignSelf: 'flex-start',
          backgroundColor: variantStyles[variant][color].backgroundColor,
          borderRadius: token.componentTagContainerBorderRadius,
          margin: 2,
          borderColor:
            variant === 'secondary'
              ? variantStyles.secondary[color].borderColor
              : undefined,
          borderWidth:
            variant === 'secondary'
              ? variantStyles.secondary[color].borderWidth
              : 0,
          lineHeight: token.componentTagTextLabelLineHeight,
          justifyContent: token.componentTagContainerAlignVertical,
          paddingHorizontal: token.componentTagContainerPaddingHorizontal,
          paddingVertical: token.componentTagContainerPaddingVertical
            ? token.componentTagContainerPaddingVertical
            : 2,
        });
      });
    });
  },
);
