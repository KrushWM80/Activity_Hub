import * as React from 'react';
import {TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/StyledText';
import {render} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {iconSizes, IconSizesKey} from '../../utils';
import {StyledText, StyledTextColor, StyledTextSize} from '../StyledText';

describe.each<StyledTextSize>(['large', 'small'])(
  'Should render StyledText correctly for all sizes ',
  (size) => {
    describe.each<StyledTextColor>(['blue', 'gray', 'green'])(
      'Should render StyledText correctly for all colors ',
      (color) => {
        test(`Test StyledText size="${size} color="${color}"`, async () => {
          const rootQueries = render(
            <StyledText size={size} color={color} leading={<Icons.CheckIcon />}>
              {`StyledText size="${size} color="${color}"`}
            </StyledText>,
          );
          const icon = await rootQueries.findByTestId('CheckIcon');
          expect(icon).toHaveStyle([
            {
              height:
                size === 'small'
                  ? iconSizes[
                      token.componentStyledTextLeadingIconSizeSmallIconSize as IconSizesKey
                    ]
                  : iconSizes[
                      token.componentStyledTextLeadingIconSizeLargeIconSize as IconSizesKey
                    ],
              tintColor:
                color === 'blue'
                  ? token.componentStyledTextLeadingIconColorBlueIconColor
                  : color === 'gray'
                  ? token.componentStyledTextLeadingIconColorGrayIconColor
                  : token.componentStyledTextLeadingIconColorGreenIconColor,
            },
            {
              marginRight: 4,
            },
          ]);

          const content = await rootQueries.findByTestId('StyledText-content');
          expect(content).toHaveStyle({
            fontFamily: 'Bogle',
            fontWeight: token.componentStyledTextTextLabelFontWeight.toString(),
            fontStyle: 'normal',
            fontSize:
              size === 'small'
                ? token.componentStyledTextTextLabelSizeSmallFontSize
                : token.componentStyledTextTextLabelSizeLargeFontSize,
            color:
              color === 'blue'
                ? token.componentStyledTextTextLabelColorBlueTextColor
                : color === 'gray'
                ? token.componentStyledTextTextLabelColorGrayTextColor
                : token.componentStyledTextTextLabelColorGreenTextColor,
            paddingTop: size === 'small' ? 4 : 3,
          } as TextStyle);
        });
      },
    );
  },
);
