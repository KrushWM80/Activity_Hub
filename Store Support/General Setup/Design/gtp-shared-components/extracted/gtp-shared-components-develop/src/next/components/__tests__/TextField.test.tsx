import * as React from 'react';
import {Platform, TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/TextField';
import {fireEvent, render, screen} from '@testing-library/react-native';
import {
  getHostChildren,
  getHostParent,
} from '@testing-library/react-native/build/helpers/component-tree';
import {Icons} from '@walmart/gtp-shared-icons';

import {getFont} from '../../../theme/font';
import {iconSizes, IconSizesKey} from '../../utils';
import {
  resolveAutoCompleteProps,
  resolveKeyboardType,
  TEXT_FIELD_VERTICAL_SPACE,
  TextField,
  TextFieldInputType,
  TextFieldSize,
} from '../TextField';

type TextFieldDisabled = boolean;

describe.each<TextFieldDisabled>([true, false])(
  'Test TextField Styling for state - Disabled: %s ',
  (textFieldDisabled) => {
    describe.each<TextFieldSize>(['small', 'large'])(
      'Text Input Size: %s',
      (size) => {
        const mockFn = jest.fn();

        // TEST -  TextField with HelperText
        test('Should render Simple TextField with HelperText correctly', async () => {
          render(
            <TextField
              label="Label Text"
              disabled={textFieldDisabled}
              size={size}
              onFocus={mockFn}
              onBlur={mockFn}
              onSubmitEditing={mockFn}
              onChangeText={mockFn}
              helperText="Helper Text"
              placeholder="PlaceHolder Text"
              leading={<Icons.PhoneIcon />}
              trailing={<Icons.HomeIcon />}
            />,
          );

          const textFieldContainer = await screen.findByTestId('TextField');

          // Expect TextField Container Styling
          expect(textFieldContainer).toHaveStyle([
            {
              flex: 1,
              justifyContent: 'center',
            },
          ]);

          const labelText = await screen.findByText('Label Text');

          // Expect TextField Label Container Styling
          expect(getHostParent(labelText)).toHaveStyle([
            {
              marginBottom: token.componentTextFieldTextLabelMarginBottom, // 4,
            },
          ]);

          // Expect Label Text Styling
          expect(labelText).toHaveStyle([
            {
              ...getFont('bold'),
            } as TextStyle,
            {
              color: textFieldDisabled
                ? token.componentTextFieldValueTextColorDisabled // "#babbbe"
                : token.componentTextFieldValueTextColorDefault, // "#2e2f32"
            },
          ]);

          const textFieldInputContainer = await screen.findByTestId(
            'TextField-input-container',
          );
          // Expect Text Wrapper Input Container Styling
          expect(textFieldInputContainer).toHaveStyle([
            {
              borderWidth: token.componentTextFieldContainerBorderWidthDefault, // 1
              borderRadius: token.componentTextFieldContainerBorderRadius, // 4 (see CEEMP-2802)
              backgroundColor: token.componentTextFieldContainerBackgroundColor, // "#fff",
              borderColor: textFieldDisabled
                ? token.componentTextFieldContainerBorderColorDisabled // "#babbbe"
                : token.componentTextFieldContainerBorderColorDefault, // "909196"
            },
          ]);
          if (TextField.displayName) {
            const textInputContainer = await screen.findByTestId(
              TextField.displayName + '-input-container',
            );

            // Expect TextInput Container Styling
            expect(textInputContainer).toHaveStyle([
              {
                flexDirection: 'row',
                alignItems: 'center',
                ...getFont(),
                paddingHorizontal:
                  (size === 'large'
                    ? token.componentTextFieldContainerSizeLargePaddingHorizontal
                    : token.componentTextFieldContainerSizeSmallPaddingHorizontal) -
                  token.componentTextFieldContainerBorderWidthDefault,

                backgroundColor:
                  token.componentTextFieldContainerBackgroundColor,
                borderWidth:
                  token.componentTextFieldContainerBorderWidthDefault, // 1
                borderRadius: token.componentTextFieldContainerBorderRadius, // 4
                paddingVertical:
                  (size === 'large'
                    ? token.componentTextFieldContainerSizeLargePaddingVertical -
                      TEXT_FIELD_VERTICAL_SPACE
                    : token.componentTextFieldContainerSizeSmallPaddingVertical) -
                  token.componentTextFieldContainerBorderWidthDefault,
                color: textFieldDisabled
                  ? token.componentTextFieldValueTextColorDisabled // "#babbbe"
                  : token.componentTextFieldValueTextColorDefault, // "#2e2f32"
                borderColor: textFieldDisabled
                  ? token.componentTextFieldContainerBorderColorDisabled
                  : token.componentTextFieldContainerBorderColorDefault,
              },
            ]);

            const textInput = await screen.findByTestId(
              TextField.displayName + '-input',
            );

            // Expect MockFn to be called when onFocus, onBlur, onChangeText, onSubmitEditing
            if (!textFieldDisabled) {
              expect(textInput.props.value).toEqual(undefined);
              fireEvent(textInput, 'onFocus');
              fireEvent(textInput, 'onBlur');
              fireEvent.changeText(textInput, 'TEST');
              fireEvent(textInput, 'onSubmitEditing');

              expect(mockFn).toHaveBeenCalledTimes(4);
            } else {
              expect(textInput.props.value).toEqual(undefined);
            }

            // Expect TextInput Styling
            expect(textInput).toHaveStyle([
              {
                flex: 1,
                ...getFont(),
                fontWeight: token.componentTextFieldValueFontWeight.toString(), // "400",
                fontSize:
                  size === 'large'
                    ? token.componentTextFieldValueSizeLargeFontSize // 16,
                    : token.componentTextFieldValueSizeSmallFontSize, // 14,
                ...Platform.select({
                  android: {
                    paddingVertical: size === 'large' ? 3 : 2,
                  },
                  ios: {
                    paddingVertical: size === 'large' ? 1 : 3,
                  },
                }),
              } as TextStyle,
            ]);
            const helperText = await screen.findByText('Helper Text');

            // Expect Helper Text Styling
            expect(helperText).toHaveStyle([
              {
                color: textFieldDisabled
                  ? token.componentTextFieldValueTextColorDisabled // "#babbbe"
                  : token.componentTextFieldValueTextColorDefault, // "#2e2f32",
              },
            ]);

            // Leading Icon
            const phoneIcon = await screen.findByTestId('PhoneIcon');
            const phoneIconSize =
              iconSizes[
                token.componentTextFieldLeadingIconIconSize as IconSizesKey // "medium"
              ];

            // Expect Phone Icon Styling
            expect(phoneIcon).toHaveStyle([
              {
                tintColor: textFieldDisabled
                  ? token.componentTextFieldLeadingIconIconColorDisabled // #babbbe"
                  : token.componentTextFieldLeadingIconIconColorDefault, // "#74767c"
                marginRight: size === 'large' ? 12 : 8,
                height: phoneIconSize,
                width: phoneIconSize,
              },
            ]);

            // Trailing Icon
            const homeIcon = await screen.findByTestId('HomeIcon');
            const homeIconSize =
              iconSizes[
                token.componentTextFieldLeadingIconIconSize as IconSizesKey // "medium"
              ];

            // Expect Home Icon Styling
            expect(homeIcon).toHaveStyle([
              {
                tintColor: textFieldDisabled
                  ? token.componentTextFieldLeadingIconIconColorDisabled // #babbbe"
                  : token.componentTextFieldLeadingIconIconColorDefault, // "#74767c"
                marginLeft: size === 'large' ? 16 : 12,
                height: homeIconSize,
                width: homeIconSize,
              },
            ]);
          }
        });

        // TEST - TextField with value
        test('Should render Simple TextField with value correctly', async () => {
          render(
            <TextField
              label="Label Text"
              disabled={textFieldDisabled}
              size={size}
              value="Value Text"
              placeholder="PlaceHolder Text"
            />,
          );

          const textFieldValue = await screen.findByTestId('TextField-input');
          expect(textFieldValue).toHaveStyle([
            {
              color: textFieldDisabled
                ? token.componentTextFieldValueTextColorDisabled // "#babbbe"
                : token.componentTextFieldValueTextColorDefault, // "#2e2f32"
            },
          ]);
        });

        // TEST - TextField with placeholder and no value
        test('Should render Simple TextField with placeholder and no value correctly', async () => {
          render(
            <TextField
              label="Label Text"
              disabled={textFieldDisabled}
              size={size}
              placeholder="PlaceHolder Text"
            />,
          );

          const textFieldValue = await screen.findByTestId('TextField-input');
          expect(textFieldValue).toHaveStyle([
            {
              color: textFieldDisabled
                ? token.componentTextFieldValueTextColorDisabled // "#babbbe"
                : token.componentTextFieldValueTextColorDefault, // "#2e2f32"
            },
          ]);
        });

        // TEST - TextField with Error
        test('Should render Simple TextField with Error correctly', async () => {
          render(
            <TextField
              label="Label Text"
              disabled={textFieldDisabled}
              size={size}
              error="Error Text"
              placeholder="PlaceHolder Text"
            />,
          );

          const textFieldContainer = await screen.findByTestId('TextField');

          // Expect Text Wrapper Input Container Styling
          expect(getHostChildren(textFieldContainer)[1]).toHaveStyle([
            {
              borderWidth: token.componentTextFieldContainerBorderWidthDefault, // 1
              borderRadius: token.componentTextFieldContainerBorderRadius, // 4
              backgroundColor: token.componentTextFieldContainerBackgroundColor, // "#fff",
              borderColor: textFieldDisabled
                ? token.componentTextFieldContainerBorderColorDisabled
                : token.componentTextFieldContainerStateErrorBorderColorDefault,
            },
          ]);

          const errorText = await screen.findByText('Error Text');

          // Expect Error Text Styling
          expect(errorText).toHaveStyle([
            {
              color:
                token.componentTextFieldContainerStateErrorBorderColorDefault, // "#de1c24"
            },
          ]);

          const errorIcon = await screen.findByTestId(
            'ExclamationCircleFillIcon',
          );

          // Expect Error Icon Styling
          expect(errorIcon).toHaveStyle([
            {
              tintColor: 'red',
            },
          ]);
        });
      },
    );
  },
);

describe.each<TextFieldInputType>([
  'email',
  'password',
  'number',
  'tel',
  'text',
  'search',
  'url',
])('Test TextField for Different InputTypes', (type) => {
  test('Should render TextField with InputType:' + type, async () => {
    render(
      <TextField
        label="Label Text"
        type={type}
        placeholder="PlaceHolder Text"
      />,
    );
    if (TextField.displayName) {
      const textInput = await screen.findByTestId(
        TextField.displayName + '-input',
      );

      expect(textInput.props.keyboardType).toEqual(
        resolveKeyboardType(type, 'ios').keyboardType,
      );
      expect(textInput.props.autoComplete).toEqual(
        resolveAutoCompleteProps(type, 'ios').autoComplete,
      );
    }
  });
});
