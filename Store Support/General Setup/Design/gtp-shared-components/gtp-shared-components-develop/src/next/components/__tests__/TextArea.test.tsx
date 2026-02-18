import * as React from 'react';
import {TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/TextArea';
import {fireEvent, render, screen} from '@testing-library/react-native';

import {getFont, Weights} from '../../../theme/font';
import {
  renderCounter,
  renderHelperTextAndError,
  renderLabel,
  TextArea,
  TextAreaSize,
  TextAreaState,
} from '../TextArea';

let defaultState: TextAreaState = {
  focused: false,
  containerBorderColor: token.componentTextAreaContainerBorderColorDefault,
  containerBorderWidth: token.componentTextAreaContainerBorderWidthDefault,
  containerPaddingVertical:
    token.componentTextAreaContainerSizeSmallPaddingVertical,
  containerPaddingHorizontal:
    token.componentTextAreaContainerSizeLargePaddingHorizontal,
  textColor: token.componentTextAreaValueTextColorDefault, // "#2e2f32"
  labelTextColor: token.componentTextAreaValueTextColorDefault, // "#2e2f32"
  helperTextColor: token.componentTextAreaValueTextColorDefault, // "#2e2f32"
  nrOfCharacters: 0,
  counterColor: token.componentTextAreaMaxLengthTextColorDefault, // "#74767c"
};

let disabledState: TextAreaState = {
  focused: false,
  containerBorderColor: token.componentTextAreaContainerBorderColorDisabled,
  containerBorderWidth: token.componentTextAreaContainerBorderWidthDisabled,
  containerPaddingVertical:
    token.componentTextAreaContainerSizeSmallPaddingVertical,
  containerPaddingHorizontal:
    token.componentTextAreaContainerSizeLargePaddingHorizontal,
  textColor: token.componentTextAreaValueTextColorDisabled, // "#babbbe"
  labelTextColor: token.componentTextAreaValueTextColorDisabled, // "#babbbe"
  helperTextColor: token.componentTextAreaValueTextColorDisabled, // "#babbbe"
  nrOfCharacters: 0,
  counterColor: token.componentTextAreaMaxLengthTextColorDisabled, // "#babbbe"
};

describe('Test render helpers', () => {
  describe.each<boolean>([true, false])(
    'Test TextArea with helperText, disabled: %s ',
    (disabled) => {
      describe.each<TextAreaSize>(['small', 'large'])('size="%s"', (size) => {
        test('should renderLabel correctly', async () => {
          const rootQueries = render(
            <>
              {renderLabel(
                size,
                disabled ? disabledState : defaultState,
                'Label text',
              )}
            </>,
          );
          if (TextArea.displayName) {
            const labelContainer = await rootQueries.findByTestId(
              TextArea.displayName + '-label-container',
            );
            expect(labelContainer).toBeTruthy();
            expect(labelContainer).toHaveStyle({
              marginBottom: token.componentTextAreaTextLabelMarginBottom, // 4
            });

            const label = await rootQueries.findByText('Label text');
            expect(label).toBeTruthy();
            expect(label).toHaveStyle({
              ...getFont('bold'),
              color: disabled
                ? disabledState.helperTextColor
                : defaultState.helperTextColor,
            } as TextStyle);
          }
        });

        test('should renderHelperTextAndError with helperText correctly', async () => {
          const rootQueries = render(
            <>
              {renderHelperTextAndError(
                size,
                disabled ? disabledState : defaultState,
                undefined,
                'Helper text',
                140,
              )}
            </>,
          );
          const helperText = await rootQueries.findByText('Helper text');
          expect(helperText).toBeTruthy();
          expect(helperText).toHaveStyle({
            ...getFont(),
            color: disabled
              ? token.componentTextAreaValueTextColorDisabled // "#babbbe"
              : token.componentTextAreaValueTextColorDefault, // "#2e2f32"
            ...getFont(
              token.componentTextAreaMaxLengthFontWeight.toString() as Weights,
            ), // "400"
            fontSize: token.componentTextAreaMaxLengthFontSize, // 12
            lineHeight: token.componentTextAreaMaxLengthLineHeight, // 16,
            marginTop: token.componentTextAreaHelperTextContainerMarginTop, // 4
          });
          const counter = await rootQueries.findByText(/140/);
          expect(counter).toBeTruthy();
          expect(counter).toHaveStyle({
            ...getFont(),
            color: disabled
              ? token.componentTextAreaMaxLengthTextColorDisabled // "#babbbe"
              : token.componentTextAreaMaxLengthTextColorDefault, // "#74767c"
            fontSize: token.componentTextAreaMaxLengthFontSize, // 12
            lineHeight: token.componentTextAreaMaxLengthLineHeight, // 16,
            marginLeft: token.componentTextAreaMaxLengthMarginStart, // 16,
            marginTop: token.componentTextAreaHelperTextContainerMarginTop, // 4
          });
        });

        test('should renderHelperTextAndError with error correctly', async () => {
          const rootQueries = render(
            <>
              {renderHelperTextAndError(
                size,
                disabled ? disabledState : defaultState,
                'Error text',
                undefined,
                140,
              )}
            </>,
          );

          const errorText = await rootQueries.findByText('Error text');
          expect(errorText).toBeTruthy();
          expect(errorText).toHaveStyle({
            ...getFont(
              token.componentTextAreaMaxLengthFontWeight.toString() as Weights,
            ), // "400"
            fontSize: token.componentTextAreaMaxLengthFontSize, // 12
            color: token.componentTextAreaContainerStateErrorBorderColorDefault, // "#de1c24"
            marginHorizontal:
              token.componentTextAreaHelperTextContainerMarginHorizontal, // 4
          });
          const counter = await rootQueries.findByText(/140/);
          expect(counter).toBeTruthy();
          expect(counter).toHaveStyle({
            ...getFont(),
            color: disabled
              ? token.componentTextAreaMaxLengthTextColorDisabled // "#babbbe"
              : token.componentTextAreaMaxLengthTextColorDefault, // "#74767c"
            fontSize: token.componentTextAreaMaxLengthFontSize, // 12
            lineHeight: token.componentTextAreaMaxLengthLineHeight, // 16,
            marginLeft: token.componentTextAreaMaxLengthMarginStart, // 16,
            marginTop: token.componentTextAreaHelperTextContainerMarginTop, // 4
          });
        });

        test('should renderCounter correctly', async () => {
          defaultState = {
            ...defaultState,
            nrOfCharacters: 10,
          };
          disabledState = {
            ...disabledState,
            nrOfCharacters: 10,
          };

          const rootQueries = render(
            <>
              {renderCounter(
                size,
                disabled ? disabledState : defaultState,
                140,
              )}
            </>,
          );

          const counter = await rootQueries.findByText(/140/);
          expect(counter).toBeTruthy();
          expect(counter).toHaveStyle({
            ...getFont(),
            color: disabled
              ? token.componentTextAreaMaxLengthTextColorDisabled // "#babbbe"
              : token.componentTextAreaMaxLengthTextColorDefault, // "#74767c"
            fontSize: token.componentTextAreaMaxLengthFontSize, // 12
            lineHeight: token.componentTextAreaMaxLengthLineHeight, // 16,
            marginLeft: token.componentTextAreaMaxLengthMarginStart, // 16,
            marginTop: token.componentTextAreaHelperTextContainerMarginTop, // 4
          });
          expect(counter.props.children[0]).toEqual(10);
          expect(counter.props.children[1]).toEqual('/');
          expect(counter.props.children[2]).toEqual(140);
        });
      });
    },
  );
});

describe.each<boolean>([true, false])(
  'Test TextArea with helperText, disabled: %s ',
  (disabled) => {
    describe.each<TextAreaSize>(['small', 'large'])('size="%s"', (size) => {
      test('Should render correctly with helperText', async () => {
        const rootQueries = render(
          <TextArea
            size={size}
            label="Label text"
            helperText="Helper text"
            placeholder="Placeholder text"
            disabled={disabled}
          />,
        );
        if (TextArea.displayName) {
          const textArea = await rootQueries.findByTestId(TextArea.displayName);
          expect(textArea).toBeTruthy();
          expect(textArea).toHaveStyle({
            flex: 1,
            justifyContent: 'center',
          });

          const inputContainer = await rootQueries.findByTestId(
            TextArea.displayName + '-input-container',
          );
          expect(inputContainer).toBeTruthy();
          expect(inputContainer).toHaveStyle({
            ...getFont(),
            flexDirection: 'row',
            alignItems: 'center',
            color: disabled
              ? token.componentTextAreaValueTextColorDisabled // "#babbbe"
              : token.componentTextAreaValueTextColorDefault, // "#2e2f32"
            borderColor: disabled
              ? token.componentTextAreaContainerBorderColorDisabled
              : token.componentTextAreaContainerBorderColorDefault,
            paddingVertical:
              (size === 'large'
                ? token.componentTextAreaContainerSizeLargePaddingVertical
                : token.componentTextAreaContainerSizeSmallPaddingVertical) -
              token.componentTextAreaContainerBorderWidthDefault,
            backgroundColor: token.componentTextAreaContainerBackgroundColor,
            borderWidth: token.componentTextAreaContainerBorderWidthDefault, // 1
            borderRadius: token.componentTextAreaContainerBorderRadius, // 4
          });

          const input = await rootQueries.findByTestId(
            TextArea.displayName + '-input',
          );
          expect(input).toBeTruthy();
          expect(input.props.multiline).toBeTruthy();
          expect(input.props.numberOfLines).toEqual(8);
          expect(input.props.editable).toEqual(disabled ? false : true);
          expect(input.props.placeholder).toEqual('Placeholder text');
          expect(input.props.autoCapitalize).toEqual('none');
          expect(input.props.showSoftInputOnFocus).toBeTruthy();
          expect(input.props.spellCheck).toBeFalsy();
          expect(input).toHaveStyle({
            ...getFont(),
            fontSize:
              size === 'large'
                ? token.componentTextAreaValueSizeLargeFontSize // 16,
                : token.componentTextAreaValueSizeSmallFontSize, // 14,
            lineHeight:
              size === 'large'
                ? token.componentTextAreaValueSizeLargeLineHeight // 24,
                : token.componentTextAreaValueSizeSmallLineHeight, // 20,
            height:
              size === 'large'
                ? token.componentTextAreaContainerSizeLargeMinHeight // 128
                : token.componentTextAreaContainerSizeSmallMinHeight, // 90
            minHeight:
              size === 'large'
                ? token.componentTextAreaContainerSizeLargeMinHeight // 128
                : token.componentTextAreaContainerSizeSmallMinHeight, // 90
            textAlignVertical: 'top',
          });
        }
      });
    });
  },
);

describe.each<boolean>([true, false])(
  'Test TextArea events, disabled: %s ',
  (disabled) => {
    describe.each<TextAreaSize>(['small', 'large'])('size="%s"', () => {
      test('Should trigger events correctly', async () => {
        const mockOnFocus = jest.fn();
        const mockOnBlur = jest.fn();
        const mockOnSubmitEditing = jest.fn();
        const mockOnChangeText = jest.fn();

        const rootQueries = render(
          <TextArea
            label="Label text"
            disabled={disabled}
            onChangeText={mockOnChangeText}
            onSubmitEditing={mockOnSubmitEditing}
            onFocus={mockOnFocus}
            onBlur={mockOnBlur}
          />,
        );
        if (TextArea.displayName) {
          const textArea = await rootQueries.findByTestId(TextArea.displayName);
          expect(textArea).toBeTruthy();

          const input = await rootQueries.findByTestId(
            TextArea.displayName + '-input',
          );
          expect(input).toBeTruthy();
          fireEvent.changeText(input, 'Thou shalt');
          fireEvent(input, 'onSubmitEditing');
          expect(input.props.value).toEqual(undefined);
          if (!disabled) {
            fireEvent(input, 'onFocus');
            expect(mockOnFocus).toHaveBeenCalledTimes(1);
            fireEvent(input, 'onBlur');
            expect(mockOnBlur).toHaveBeenCalledTimes(1);
          }
        }
      });
    });
  },
);

describe.each<boolean>([true, false])(
  'Test TextArea value style, disabled: %s ',
  (disabled) => {
    describe.each<TextAreaSize>(['small', 'large'])('size="%s"', () => {
      test('Should render correctly with value', async () => {
        render(
          <TextArea
            label="Label text"
            value="Label value"
            disabled={disabled}
          />,
        );
        const textAreaValue = await screen.findByTestId('TextArea-input');
        expect(textAreaValue).toHaveStyle([
          {
            color: disabled
              ? token.componentTextAreaValueTextColorDisabled // "#babbbe"
              : token.componentTextAreaValueTextColorDefault, // "#2e2f32"
          },
        ]);
      });
    });
  },
);

describe.each<boolean>([true, false])(
  'Test TextArea placeholder style, disabled: %s ',
  (disabled) => {
    describe.each<TextAreaSize>(['small', 'large'])('size="%s"', () => {
      test('Should render correctly with placeholder', async () => {
        render(
          <TextArea
            label="Label text"
            placeholder="Placeholder text"
            disabled={disabled}
          />,
        );
        const textAreaValue = await screen.findByTestId('TextArea-input');
        expect(textAreaValue).toHaveStyle([
          {
            color: disabled
              ? token.componentTextAreaValueTextColorDisabled // "#babbbe"
              : token.componentTextAreaValueTextColorDefault, // "#2e2f32"
          },
        ]);
      });
    });
  },
);
