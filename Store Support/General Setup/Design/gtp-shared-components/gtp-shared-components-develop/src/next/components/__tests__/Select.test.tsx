import * as React from 'react';
import {Platform, TextStyle} from 'react-native';

import * as modalToken from '@livingdesign/tokens/dist/react-native/light/regular/components/Modal';
import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Select';
import * as taToken from '@livingdesign/tokens/dist/react-native/light/regular/components/TextArea';
import {fireEvent, render, screen, within} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {getFont, Weights} from '../../../theme/font';
import {Button} from '../Button';
import {PopoverPosition} from '../Popover';
import {
  distanceBottomY,
  distanceTopY,
  dropdownPositionBasedStyle,
  initialSelectedOptions,
  renderChevron,
  renderHelperTextAndError,
  renderLabel,
  renderLeading,
  renderValue,
  Select,
  SelectOptions,
  SelectSize,
  SelectState,
} from '../Select';
import {TextField} from '../TextField';

// test initialSelectedOption

jest.useFakeTimers({legacyFakeTimers: true});
jest.mock('react-native/Libraries/EventEmitter/NativeEventEmitter');
jest.mock('react-native-device-info', () => {
  return {
    __esModule: true,
    default: {
      isEmulator: jest
        .fn()
        .mockReturnValueOnce(true)
        .mockReturnValueOnce(false)
        .mockReturnValueOnce(true)
        .mockReturnValueOnce(false),
      ...jest.fn(() => {}),
    },
  };
});

const showHideSelectComponent = jest.fn();
const selectOptions: SelectOptions = [
  {text: 'Mug'},
  {text: 'Shirt'},
  {text: 'Sticker'},
  {text: 'HatNotAvailable', disabled: true},
  {text: 'Hoodie'},
];

const defaultState = (_size: SelectSize) => {
  return {
    value: 'Select your swag...',
    textColor: token.componentSelectValueTextColorDefault,
    labelTextColor: token.componentSelectValueTextColorDefault,
    helperTextColor: token.componentSelectValueTextColorDefault,
    isExpanded: false,
    buttonContainerBorderWidth:
      token.componentSelectContainerBorderWidthDefault,
    buttonContainerPaddingVertical:
      (_size === 'large'
        ? token.componentSelectContainerSizeLargePaddingVertical
        : token.componentSelectContainerSizeSmallPaddingVertical) -
      token.componentSelectContainerBorderWidthDefault,
    buttonContainerTopBorderRadius: token.componentSelectContainerBorderRadius,
    buttonContainerBottomBorderRadius:
      token.componentSelectContainerBorderRadius,
    buttonContainerBorderColor:
      token.componentSelectContainerBorderColorDefault,
  };
};

const disabledState = (_size: SelectSize) => {
  return {
    value: 'Select your swag...',
    textColor: token.componentSelectValueTextColorDisabled,
    labelTextColor: token.componentSelectValueTextColorDisabled,
    helperTextColor: token.componentSelectValueTextColorDisabled,
    isExpanded: false,
    buttonContainerPaddingVertical:
      (_size === 'large'
        ? token.componentSelectContainerSizeLargePaddingVertical
        : token.componentSelectContainerSizeSmallPaddingVertical) -
      token.componentSelectContainerBorderWidthDisabled,
    buttonContainerTopBorderRadius: token.componentSelectContainerBorderRadius,
    buttonContainerBottomBorderRadius:
      token.componentSelectContainerBorderRadius,
    buttonContainerBorderColor:
      token.componentSelectContainerBorderColorDisabled,
    buttonContainerBorderWidth:
      token.componentSelectContainerBorderWidthDisabled,
  };
};

describe('Test render helpers', () => {
  describe.each<boolean>([true, false])(
    'Test Select with helperText, disabled: %s ',
    (disabled): void => {
      describe.each<SelectSize>(['small', 'large'])('size="%s"', (size) => {
        test('should renderLabel correctly', async () => {
          const rootQueries = render(
            <>
              {renderLabel(
                size,
                disabled ? disabledState(size) : defaultState(size),
                'Label text',
              )}
            </>,
          );
          if (Select.displayName) {
            const labelContainer = await rootQueries.findByTestId(
              Select.displayName + '-label-container',
            );
            expect(labelContainer).toBeTruthy();
            expect(labelContainer).toHaveStyle({
              marginBottom: token.componentSelectTextLabelMarginBottom,
            });
            const label = await rootQueries.findByText('Label text');
            expect(label).toBeTruthy();
            expect(label).toHaveStyle({
              ...getFont('bold'),
              color: disabled
                ? disabledState(size).helperTextColor
                : defaultState(size).helperTextColor,
            } as TextStyle);
          }
        });

        test('should renderHelperTextAndError with helperText correctly', async () => {
          const rootQueries = render(
            <>
              {renderHelperTextAndError(
                size,
                disabled ? disabledState(size) : defaultState(size),
                undefined,
                'Helper text',
              )}
            </>,
          );
          const helperText = await rootQueries.findByText('Helper text');
          expect(helperText).toBeTruthy();
          expect(helperText).toHaveStyle({
            ...getFont(),
            color: disabled
              ? token.componentSelectValueTextColorDisabled
              : token.componentSelectValueTextColorDefault,
            ...getFont(
              taToken.componentTextAreaMaxLengthFontWeight.toString() as Weights,
            ),
            fontSize: taToken.componentTextAreaMaxLengthFontSize,
            lineHeight: taToken.componentTextAreaMaxLengthLineHeight,
            marginTop: taToken.componentTextAreaHelperTextContainerMarginTop,
          });
        });

        test('should renderHelperTextAndError with error correctly', async () => {
          const rootQueries = render(
            <>
              {renderHelperTextAndError(
                size,
                disabled ? disabledState(size) : defaultState(size),
                'Error text',
                undefined,
              )}
            </>,
          );

          const errorText = await rootQueries.findByText('Error text');
          expect(errorText).toBeTruthy();
          expect(errorText).toHaveStyle({
            ...getFont(
              taToken.componentTextAreaMaxLengthFontWeight.toString() as Weights,
            ),
            fontSize: taToken.componentTextAreaMaxLengthFontSize,
            color:
              taToken.componentTextAreaContainerStateErrorBorderColorDefault,
          } as TextStyle);
        });
      });
    },
  );
});

describe.each<boolean>([true, false])(
  'Test Select with helperText, disabled: %s ',
  (disabled) => {
    describe.each<SelectSize>(['small', 'large'])('size="%s"', (size) => {
      test('Should render correctly with helperText', async () => {
        const rootQueries = render(
          <Select
            size={size}
            label="Label text"
            helperText="Helper text"
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            disabled={disabled}
            onChange={jest.fn()}
          />,
        );
        if (Select.displayName && rootQueries) {
          const select = await rootQueries.findByTestId(Select.displayName);
          expect(select).toBeTruthy();
          expect(select).toHaveStyle({
            alignItems: 'flex-start',
          });

          const buttonContainer = await rootQueries.findByTestId(
            Select.displayName + '-button-container',
          );
          expect(buttonContainer).toBeTruthy();
          expect(buttonContainer).toHaveStyle({
            ...getFont(),
            flexDirection: 'row',
            alignItems: 'center',
            color: disabled
              ? token.componentSelectValueTextColorDisabled
              : token.componentSelectValueTextColorDefault,
            borderColor: disabled
              ? token.componentSelectContainerBorderColorDisabled
              : token.componentSelectContainerBorderColorDefault,
            backgroundColor: token.componentSelectContainerBackgroundColor,
            borderWidth: token.componentSelectContainerBorderWidthDefault,
            borderRadius: token.componentSelectContainerBorderRadius, // (see CEEMP-2802)
          });

          const button = rootQueries.root.findByProps({
            testID: Select.displayName + '-button',
          });
          expect(button).toBeTruthy();

          const styleObject = {
            ...button.props.style[0],
            ...button.props.style[1],
          };
          expect(styleObject).toEqual({
            flex: 1,
            marginVertical:
              (size === 'large'
                ? token.componentSelectContainerSizeLargePaddingVertical
                : token.componentSelectContainerSizeSmallPaddingVertical) -
              token.componentSelectContainerBorderWidthDefault,
            height: '100%',
            flexDirection: 'row',
            justifyContent: 'flex-start',
            alignItems: 'center',
            marginLeft:
              size === 'large'
                ? token.componentSelectLeadingIconSizeLargeOffsetStart
                : token.componentSelectLeadingIconSizeSmallOffsetStart,
            paddingRight: 8,
          });
        }
      });
    });
  },
);

describe.each<boolean>([true, false])(
  'Test Select events, disabled: %s ',
  (disabled) => {
    describe.each<SelectSize>(['small', 'large'])('size="%s"', (size) => {
      test('Should trigger events correctly', async () => {
        const mockOnChange = jest.fn();

        const component = render(
          <Select
            size={size}
            label="Label text"
            helperText="Helper text"
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            disabled={disabled}
            onChange={mockOnChange}
          />,
        );
        if (Select.displayName && component && screen) {
          const select = await screen.findByTestId(Select.displayName);
          expect(select).toBeTruthy();

          const button = await screen.UNSAFE_getByProps({
            testID: Select.displayName + '-button',
          });
          expect(button).toBeTruthy();

          const caretDownIcon = screen.root.findByProps({
            testID: 'CaretDownIcon',
          });
          expect(caretDownIcon).toBeTruthy();

          if (!disabled) {
            fireEvent.press(button);

            const _option0 = screen.getByTestId('_Option_0');
            const _option1 = screen.getByTestId('_Option_1');
            const _option2 = screen.getByTestId('_Option_2');
            const _option3 = screen.getByTestId('_Option_3');
            const _option4 = screen.getByTestId('_Option_4');
            const caretUpIcon = screen.root.findByProps({
              testID: 'CaretUpIcon',
            });
            expect(caretUpIcon).toBeTruthy();

            expect(within(_option0).getByText('Mug')).toBeTruthy();
            expect(within(_option1).getByText('Shirt')).toBeTruthy();
            expect(within(_option2).getByText('Sticker')).toBeTruthy();
            expect(within(_option3).getByText('HatNotAvailable')).toBeTruthy();
            expect(within(_option4).getByText('Hoodie')).toBeTruthy();

            fireEvent.press(_option4);
            expect(within(_option4).getByTestId('CheckIcon')).toBeTruthy();
          }
        }
      });
    });
  },
);

describe.each<boolean>([true, false])(
  'Test Select events, close should be enabled again when reopened : disabled: %s ',
  (disabled) => {
    describe.each<SelectSize>(['small', 'large'])('size="%s"', (size) => {
      test('Should trigger events correctly when reopened', async () => {
        const mockOnChange = jest.fn();

        let component = await render(
          <Select
            size={size}
            label="Label text"
            helperText="Helper text"
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            disabled={disabled}
            onChange={mockOnChange}
            componentType={{
              android: 'Modal',
              ios: 'Modal',
            }}
          />,
        );
        if (Select.displayName && component && screen) {
          const select = await component.root.findByProps({
            testID: Select.displayName,
          });
          expect(select).toBeTruthy();

          const button = await component.root.findByProps({
            testID: Select.displayName + '-button',
          });
          expect(button).toBeTruthy();

          if (!disabled) {
            fireEvent.press(button);

            const closeButton = screen.getByTestId('Modal-close-button');
            expect(closeButton).toBeTruthy();

            const _option0 = screen.getByTestId('_Option_0');
            const _option1 = screen.getByTestId('_Option_1');
            const _option2 = screen.getByTestId('_Option_2');
            const _option3 = screen.getByTestId('_Option_3');
            const _option4 = screen.getByTestId('_Option_4');
            const caretUpIcon = await component.root.findByProps({
              testID: 'CaretUpIcon',
            });
            expect(caretUpIcon).toBeTruthy();

            expect(within(_option0).getByText('Mug')).toBeTruthy();
            expect(within(_option1).getByText('Shirt')).toBeTruthy();
            expect(within(_option2).getByText('Sticker')).toBeTruthy();
            expect(within(_option3).getByText('HatNotAvailable')).toBeTruthy();
            expect(within(_option4).getByText('Hoodie')).toBeTruthy();

            fireEvent.press(_option4);
            expect(within(_option4).getByTestId('CheckIcon')).toBeTruthy();

            // reopen the modal:
            fireEvent.press(button);
            const closeButton2 = await component.root.findByProps({
              testID: 'Modal-close-button',
            });
            expect(closeButton2).toBeTruthy();
          }
        }
      });
    });
  },
);

describe('Test initialSelectedOptions', () => {
  test('return style Correctly ', async () => {
    const selectionOptions = [
      {text: 'Mug'},
      {
        text: 'Shirt ',
        selected: true,
      },
      {
        text: 'Sticker',
      },
      {
        text: 'HatNotAvailable',
        disabled: true,
      },
      {text: 'Hoodie'},
    ];

    const selectedItems = initialSelectedOptions(selectionOptions);
    expect(selectedItems).toEqual([
      {
        index: 1,
        text: 'Shirt ',
        selected: true,
      },
    ]);
    const nonSelectionOptions = [
      {text: 'Mug'},
      {
        text: 'Shirt ',
      },
      {
        text: 'Sticker',
      },
      {
        text: 'HatNotAvailable',
        disabled: true,
      },
      {text: 'Hoodie'},
    ];
    const selected = initialSelectedOptions(nonSelectionOptions);
    expect(selected).toEqual([]);
  });
});

describe.each<PopoverPosition>([
  'bottomCenter',
  'bottomLeft',
  'bottomRight',
  'topCenter',
  'topLeft',
  'topRight',
])('Test dropdownPositionBasedStyle', (position) => {
  test('return style Correctly ', async () => {
    const dropdownStyle = dropdownPositionBasedStyle(position, 'large');
    if (position.includes('top')) {
      expect(dropdownStyle).toEqual({
        paddingTop: 5,
        borderTopLeftRadius: modalToken.componentModalContainerBorderRadius,
        borderTopRightRadius: modalToken.componentModalContainerBorderRadius,
        backgroundColor: modalToken.componentModalContainerBackgroundColor,
        borderTopWidth: token.componentSelectContainerBorderWidthDefault,
        borderLeftWidth: token.componentSelectContainerBorderWidthDefault,
        borderRightWidth: token.componentSelectContainerBorderWidthDefault,
        borderColor: token.componentSelectContainerBorderColorDisabled,
      });
    } else {
      expect(dropdownStyle).toEqual({
        maxHeight: 300,
        paddingBottom: 5,
        borderBottomLeftRadius: modalToken.componentModalContainerBorderRadius,
        borderBottomRightRadius: modalToken.componentModalContainerBorderRadius,
        backgroundColor: modalToken.componentModalContainerBackgroundColor,
        borderBottomWidth: token.componentSelectContainerBorderWidthDefault,
        borderLeftWidth: token.componentSelectContainerBorderWidthDefault,
        borderRightWidth: token.componentSelectContainerBorderWidthDefault,
        borderColor: token.componentSelectContainerBorderColorDisabled,
      });
    }
  });
});
describe.each<boolean>([true, false])(
  'Test Select renderLabel ',
  (disabled) => {
    test('render SelectLabel', async () => {
      const labelTextColor = disabled
        ? token.componentSelectValueTextColorDisabled
        : token.componentSelectValueTextColorDefault;
      render(
        renderLabel(
          'large',
          {labelTextColor: labelTextColor} as SelectState,
          'Select Label',
        ),
      );
      const label = await screen.findByText('Select Label');
      expect(label).toBeTruthy();
    });
  },
);

describe('Test Select renderLeading ', () => {
  describe.each<boolean>([false, true])('disabled:%s', (disabled) => {
    describe.each<boolean>([true, false])('isExpanded:%s', (isExpanded) => {
      test('render SelectLeading', async () => {
        render(
          <>
            {renderLeading(
              <Icons.EmailIcon />,
              {isExpanded: isExpanded} as SelectState,
              disabled,
              'large',
            )}
          </>,
        );
        const emailIcon = screen.findByTestId('EmailIcon');
        expect(emailIcon).toBeTruthy();
        const style = (await emailIcon).props.style;
        if (disabled) {
          expect(style).toEqual([
            {
              height: 24,
              tintColor: token.componentSelectLeadingIconStateDisabledIconColor,
              width: 24,
            },
            {marginRight: 12},
          ]);
        } else if (isExpanded) {
          expect(style).toEqual([
            {
              height: 24,
              tintColor: token.componentSelectIconIconColorFocus,
              width: 24,
            },
            {marginRight: 12},
          ]);
        } else {
          expect(style).toEqual([
            {
              height: 24,
              tintColor: token.componentSelectLeadingIconIconColor,
              width: 24,
            },
            {marginRight: 12},
          ]);
        }
      });
    });
  });
});
describe('Test Select renderChevron ', () => {
  describe.each<boolean>([false, true])('disabled:%s', (disabled) => {
    describe.each<boolean>([true, false])('isExpanded:%s', (isExpanded) => {
      test('render SelectChevron', async () => {
        render(
          <>
            {renderChevron(
              {isExpanded: isExpanded} as SelectState,
              disabled,
              showHideSelectComponent,
            )}
          </>,
        );
        if (isExpanded) {
          const CaretUpIcon = screen.root.findByProps({testID: 'CaretUpIcon'});
          expect(CaretUpIcon).toBeTruthy();
          const style = (await CaretUpIcon).props.style;
          if (disabled) {
            expect(style).toEqual([
              {
                height: 24,
                tintColor: token.componentSelectIconIconColorDisabled,
                width: 24,
              },
              {},
            ]);
          } else {
            expect(style).toEqual([
              {
                height: 24,
                tintColor: token.componentSelectIconIconColorFocus,
                width: 24,
              },
              {},
            ]);
          }
        } else {
          const CaretDownIcon = screen.root.findByProps({
            testID: 'CaretDownIcon',
          });
          expect(CaretDownIcon).toBeTruthy();
          const style = (await CaretDownIcon).props.style;
          if (disabled) {
            expect(style).toEqual([
              {
                height: 24,
                tintColor: token.componentSelectIconIconColorDisabled,
                width: 24,
              },
              {},
            ]);
          } else {
            expect(style).toEqual([
              {
                height: 24,
                tintColor: token.componentSelectIconIconColorDefault,
                width: 24,
              },
              {},
            ]);
          }
        }
      });
    });
  });
});

describe.each<boolean>([false, true])(
  'Test Select renderValue ',
  (disabled) => {
    test('render SelectValue', async () => {
      const textColor = disabled
        ? token.componentSelectValueTextColorDisabled
        : token.componentSelectValueTextColorDefault;
      render(
        <>
          {renderValue(
            'mug, jug',
            {textColor: textColor} as SelectState,
            'large',
          )}
        </>,
      );
      const value = await screen.findByTestId('Select-value');
      expect(value).toBeTruthy();
    });
  },
);

describe.each<boolean>([false, true])(
  'Test Select distanceBottomY ',
  (isInsideModal) => {
    describe.each<boolean>([true, false])('isEmulator : %s', (isEmulator) => {
      test(`test android ${isEmulator}`, async () => {
        Platform.OS = 'android';
        const distance = await distanceBottomY(isInsideModal, 240, 56);
        if (isInsideModal) {
          if (isEmulator) {
            expect(distance).toEqual(272);
          } else {
            expect(distance).toEqual(261.5);
          }
        } else {
          expect(distance).toEqual(296);
        }
      });
      test('test ios', async () => {
        Platform.OS = 'ios';
        const distance = await distanceBottomY(isInsideModal, 240, 56);
        expect(distance).toEqual(296);
      });
    });
  },
);

describe.each<boolean>([false, true])('Test distanceTopY ', (isInsideModal) => {
  describe.each<boolean>([true, false])('isEmulator : %s', (isEmulator) => {
    test(`android ${isEmulator}`, async () => {
      Platform.OS = 'android';
      const distance = await distanceTopY(isInsideModal, 240, 300);
      if (isInsideModal) {
        if (isEmulator) {
          expect(distance).toEqual(-70);
        } else {
          expect(distance).toEqual(-80.5);
        }
      } else {
        expect(distance).toEqual(-46.5);
      }
    });
    test(`ios  isInsideModal:${isInsideModal}`, async () => {
      Platform.OS = 'ios';
      const distance = await distanceTopY(isInsideModal, 240, 300);
      if (isInsideModal) {
        expect(distance).toEqual(-46);
      } else {
        expect(distance).toEqual(-46.5);
      }
    });
  });
});

describe('Test Select should show the correct text when locales change ', () => {
  test('Should trigger events correctly when reopened', async () => {
    const mockOnChange = jest.fn();
    const Content = () => {
      const [locale, setLocale] = React.useState('en');
      const spanishOptions: SelectOptions = [
        {text: 'Taza'},
        {
          text: 'Camisa',
        },
        {
          text: 'Pegatina',
        },
        {
          text: 'SombreroNoDisponible',
          selected: true,
        },
        {text: 'Sudadera con capucha'},
      ];

      return (
        <>
          <Button
            onPress={() => setLocale(locale === 'en' ? 'es' : 'en')}
            testID="LocaleButton">
            {'change locale'}
          </Button>
          <Select
            size={'medium'}
            label="Label text"
            helperText="Helper text"
            selectOptions={locale === 'es' ? spanishOptions : selectOptions}
            placeholder="Select your swag..."
            onChange={mockOnChange}
            componentType={{
              android: 'InlineView',
              ios: 'InlineView',
            }}
          />
        </>
      );
    };
    let component = await render(<Content />);
    if (Select.displayName && component && screen) {
      const select = await component.findByTestId(Select.displayName);
      expect(select).toBeTruthy();
      const button = await component.UNSAFE_getByProps({
        testID: Select.displayName + '-button',
      });
      expect(button).toBeTruthy();
      fireEvent.press(button);
      const localeButton = await component.findByTestId('LocaleButton');
      expect(localeButton).toBeTruthy();

      //fireEvent.press(localeButton);

      const _option0 = screen.getByTestId('_Option_0');
      const _option1 = screen.getByTestId('_Option_1');
      const _option2 = screen.getByTestId('_Option_2');
      const _option3 = screen.getByTestId('_Option_3');
      const _option4 = screen.getByTestId('_Option_4');
      const caretUpIcon = await component.UNSAFE_getByProps({
        testID: 'CaretUpIcon',
      });
      expect(caretUpIcon).toBeTruthy();

      expect(within(_option0).getByText('Mug')).toBeTruthy();
      expect(within(_option1).getByText('Shirt')).toBeTruthy();
      expect(within(_option2).getByText('Sticker')).toBeTruthy();
      expect(within(_option3).getByText('HatNotAvailable')).toBeTruthy();
      expect(within(_option4).getByText('Hoodie')).toBeTruthy();

      fireEvent.press(_option4);
      expect(within(_option4).getByTestId('CheckIcon')).toBeTruthy();

      fireEvent.press(localeButton);
      const _opt0 = screen.getByTestId('_Option_0');
      const _opt1 = screen.getByTestId('_Option_1');
      const _opt2 = screen.getByTestId('_Option_2');
      const _opt3 = screen.getByTestId('_Option_3');
      const _opt4 = screen.getByTestId('_Option_4');

      expect(within(_opt0).getByText('Taza')).toBeTruthy();
      expect(within(_opt1).getByText('Camisa')).toBeTruthy();
      expect(within(_opt2).getByText('Pegatina')).toBeTruthy();
      expect(within(_opt3).getByText('SombreroNoDisponible')).toBeTruthy();
      expect(within(_opt4).getByText('Sudadera con capucha')).toBeTruthy();

      fireEvent.press(_opt4);
      expect(within(_opt4).getByTestId('CheckIcon')).toBeTruthy();
    }
  });
});
describe('Test Select should show the ExtraContent for single options', () => {
  test('Should render ExtraContent Done action', async () => {
    const mockOnChange = jest.fn();
    const Content = () => {
      const ExtraContent = () => {
        return <TextField label="" placeholder="Enter quantity" />;
      };
      const _extraContentSelectOptions: SelectOptions = [
        {text: 'Mug'},
        {text: 'Shirt'},
        {text: 'Sticker', extraContent: <ExtraContent />, selected: true},
        {text: 'HatNotAvailable', disabled: true},
        {text: 'Hoodie'},
      ];

      return (
        <>
          <Select
            size={'medium'}
            label="Label text"
            helperText="Helper text"
            selectOptions={_extraContentSelectOptions}
            placeholder="Select your swag..."
            onChange={mockOnChange}
            componentType={{
              android: 'InlineView',
              ios: 'InlineView',
            }}
          />
        </>
      );
    };
    render(<Content />);

    if (Select.displayName) {
      const select = await screen.findByTestId(Select.displayName);
      expect(select).toBeTruthy();
      const caretDownIcon = screen.root.findByProps({testID: 'CaretDownIcon'});
      expect(caretDownIcon).toBeTruthy();
      const button = await screen.root.findByProps({
        testID: Select.displayName + '-button',
      });
      expect(button).toBeTruthy();
      fireEvent.press(button);
      const _option2 = screen.getByTestId('Select-OptionItem-2');
      expect(within(_option2).getByTestId('CheckIcon')).toBeTruthy();
      expect(within(_option2).getByTestId('TextField')).toBeTruthy();
      expect(within(_option2).getByText('Done')).toBeTruthy();
      expect(within(_option2).getByText('Cancel')).toBeTruthy();
      const done = await screen.getByText('Done');
      expect(done).toBeTruthy();
      fireEvent.press(done);
      const CaretUpIcon = screen.root.findByProps({testID: 'CaretUpIcon'});
      expect(CaretUpIcon).toBeTruthy();
      expect(screen.queryAllByTestId('CaretDownIcon')).toEqual([]);
      const selectedValue = screen.root.findByProps({testID: 'Select-value'});

      expect(selectedValue.props.children).toEqual('Sticker');
    }
  });
  test('Should render ExtraContent cancel action', async () => {
    const mockOnChange = jest.fn();
    const Content = () => {
      const ExtraContent = () => {
        return <TextField label="" placeholder="Enter quantity" />;
      };
      const _extraContentSelectOptions: SelectOptions = [
        {text: 'Mug'},
        {text: 'Shirt'},
        {text: 'Sticker', extraContent: <ExtraContent />, selected: true},
        {text: 'HatNotAvailable', disabled: true},
        {text: 'Hoodie'},
      ];

      return (
        <>
          <Select
            size={'medium'}
            label="Label text"
            helperText="Helper text"
            selectOptions={_extraContentSelectOptions}
            placeholder="Select your swag..."
            onChange={mockOnChange}
            componentType={{
              android: 'InlineView',
              ios: 'InlineView',
            }}
          />
        </>
      );
    };
    render(<Content />);

    if (Select.displayName) {
      const select = await screen.findByTestId(Select.displayName);
      expect(select).toBeTruthy();
      const caretDownIcon = screen.root.findByProps({testID: 'CaretDownIcon'});
      expect(caretDownIcon).toBeTruthy();
      const button = await screen.root.findByProps({
        testID: Select.displayName + '-button',
      });
      expect(button).toBeTruthy();
      fireEvent.press(button);
      const _option2 = screen.getByTestId('Select-OptionItem-2');
      expect(within(_option2).getByTestId('CheckIcon')).toBeTruthy();
      expect(within(_option2).getByTestId('TextField')).toBeTruthy();
      expect(within(_option2).getByText('Done')).toBeTruthy();
      expect(within(_option2).getByText('Cancel')).toBeTruthy();
      const cancel = await screen.getByText('Cancel');
      expect(cancel).toBeTruthy();
      fireEvent.press(cancel);
      const CaretUpIcon = screen.root.findByProps({testID: 'CaretUpIcon'});
      expect(CaretUpIcon).toBeTruthy();
      expect(screen.queryAllByTestId('CaretDownIcon')).toEqual([]);
      const selectedValue = screen.root.findByProps({testID: 'Select-value'});
      expect(selectedValue.props.children).toEqual('Sticker');
    }
  });
  test('Should change Value', async () => {
    const mockOnChange = jest.fn();
    const Content = () => {
      const ExtraContent = () => {
        return <TextField label="" placeholder="Enter quantity" />;
      };
      const _extraContentSelectOptions: SelectOptions = [
        {text: 'Mug'},
        {text: 'Shirt'},
        {text: 'Sticker', extraContent: <ExtraContent />, selected: true},
        {text: 'HatNotAvailable', disabled: true},
        {text: 'Hoodie'},
      ];

      return (
        <>
          <Select
            size={'medium'}
            label="Label text"
            helperText="Helper text"
            selectOptions={_extraContentSelectOptions}
            placeholder="Select your swag..."
            onChange={mockOnChange}
            componentType={{
              android: 'InlineView',
              ios: 'InlineView',
            }}
          />
        </>
      );
    };
    let component = await render(<Content />);

    if (Select.displayName && component && screen) {
      const select = await component.findByTestId(Select.displayName);
      expect(select).toBeTruthy();
      const caretDownIcon = component.root.findByProps({
        testID: 'CaretDownIcon',
      });
      expect(caretDownIcon).toBeTruthy();
      const button = await screen.root.findByProps({
        testID: Select.displayName + '-button',
      });
      expect(button).toBeTruthy();
      fireEvent.press(button);
      const _option0 = component.getByTestId('_Option_0');
      expect(_option0).toBeTruthy();
      fireEvent.press(_option0);
      const selectedValue = component.root.findByProps({
        testID: 'Select-value',
      });
      expect(selectedValue.props.children).toEqual('Mug');
    }
  });
  test('should not show out of range selection, after options change', async () => {
    const mockOnChange = jest.fn();
    const _selectOptionsInitial: SelectOptions = [
      {text: 'Mug'},
      {text: 'Shirt'},
      {text: 'Sticker'},
    ];

    const _selectOptionsReducedRange: SelectOptions = [
      {text: 'Hoodie'},
      {text: 'Hat'},
    ];

    const Content = ({
      contentSelectOptions,
    }: {
      contentSelectOptions: SelectOptions;
    }) => (
      <>
        <Select
          size={'medium'}
          label="Label text"
          helperText="Helper text"
          selectOptions={contentSelectOptions}
          placeholder="Select your swag..."
          onChange={mockOnChange}
          componentType={{
            android: 'InlineView',
            ios: 'InlineView',
          }}
        />
      </>
    );
    let component = await render(
      <Content contentSelectOptions={_selectOptionsInitial} />,
    );

    if (Select.displayName && component && screen) {
      const select = await component.findByTestId(Select.displayName);
      expect(select).toBeTruthy();
      const caretDownIcon = component.root.findByProps({
        testID: 'CaretDownIcon',
      });
      expect(caretDownIcon).toBeTruthy();
      const button = await screen.root.findByProps({
        testID: Select.displayName + '-button',
      });
      expect(button).toBeTruthy();
      fireEvent.press(button);
      const _option0 = component.getByTestId('_Option_2');
      expect(_option0).toBeTruthy();
      fireEvent.press(_option0);
      const selectedValue = component.root.findByProps({
        testID: 'Select-value',
      });
      expect(selectedValue.props.children).toEqual('Sticker');

      component.rerender(
        <Content contentSelectOptions={_selectOptionsReducedRange} />,
      );

      const selectedValueRerender = component.root.findByProps({
        testID: 'Select-value',
      });
      expect(selectedValueRerender.props.children).toEqual(
        'Select your swag...',
      );
    }
  });
});
