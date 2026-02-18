import * as React from 'react';
import {TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Radio';
import {fireEvent, render} from '@testing-library/react-native';

import {Radio} from '../Radio';

const mockFn = jest.fn();
const _radioButtonOuter = 'Radio-buttonOuter';
const _radioButtonInner = 'Radio-buttonInner';
describe('Test Radio', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  test('Should trigger onPress correctly', async () => {
    const rootQueries = render(
      <Radio testID="Enabled" label="Enabled" onPress={mockFn} />,
    );

    expect(mockFn).toHaveBeenCalledTimes(0);
    const radio = await rootQueries.findByTestId('Enabled');
    fireEvent.press(radio);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
  test('Should not trigger onPress when disabled', async () => {
    const rootQueries = render(
      <Radio testID="Disabled" label="Disabled" disabled onPress={mockFn} />,
    );

    expect(mockFn).toHaveBeenCalledTimes(0);
    const radio = await rootQueries.findByTestId('Disabled');
    fireEvent.press(radio);
    expect(mockFn).toHaveBeenCalledTimes(0);
  });
  test('Should render Unchecked correctly', async () => {
    const rootQueries = render(
      <Radio testID="Unchecked" label="Unchecked" onPress={mockFn} />,
    );
    // Check Outer style
    const buttonOuter = await rootQueries.findByTestId(_radioButtonOuter);
    expect(buttonOuter).toHaveStyle({
      borderWidth: token.componentRadioInputOuterBorderWidthDefault,
      borderColor: token.componentRadioInputOuterBorderColorDefault,
    });
    // Check Inner Style
    const buttonInner = await rootQueries.findByTestId(_radioButtonInner);
    expect(buttonInner).toHaveStyle({
      backgroundColor: token.componentRadioInputInnerBackgroundColorDefault,
    });
    const label = await rootQueries.findByText('Unchecked');
    expect(label).toHaveStyle({
      fontFamily: 'Bogle',
      fontWeight: token.componentRadioTextLabelFontWeight.toString(),
      color: token.componentRadioTextLabelTextColorDefault,
    } as TextStyle);
  });
  test('Should render Unchecked disabled correctly', async () => {
    const rootQueries = render(
      <Radio
        testID="UncheckedDisabled"
        label="UncheckedDisabled"
        disabled
        onPress={mockFn}
      />,
    );
    // Check Outer style
    const buttonOuter = await rootQueries.findByTestId(_radioButtonOuter);
    expect(buttonOuter).toHaveStyle({
      borderWidth: token.componentRadioInputOuterBorderWidthDisabled,
      borderColor: token.componentRadioInputOuterBorderColorDisabled,
    });
    // Check Inner Style
    const buttonInner = await rootQueries.findByTestId(_radioButtonInner);
    expect(buttonInner).toHaveStyle({
      backgroundColor: token.componentRadioInputInnerBackgroundColorDisabled,
    });
    const label = await rootQueries.findByText('UncheckedDisabled');
    expect(label).toHaveStyle({
      fontFamily: 'Bogle',
      fontWeight: token.componentRadioTextLabelFontWeight.toString(),
      color: token.componentRadioTextLabelTextColorDisabled,
    } as TextStyle);
  });
  test('Should render Checked correctly', async () => {
    const rootQueries = render(
      <Radio testID="Checked" label="Checked" checked onPress={mockFn} />,
    );
    // Check Outer style
    const buttonOuter = await rootQueries.findByTestId(_radioButtonOuter);
    expect(buttonOuter).toHaveStyle({
      borderWidth: token.componentRadioInputOuterBorderWidthDefault,
      borderColor: token.componentRadioInputOuterBorderColorDefault,
    });
    // Check Inner Style
    const buttonInner = await rootQueries.findByTestId(_radioButtonInner);
    expect(buttonInner).toHaveStyle({
      backgroundColor:
        token.componentRadioInputInnerStateCheckedBackgroundColorDefault,
    });
    const label = await rootQueries.findByText('Checked');
    expect(label).toHaveStyle({
      fontFamily: 'Bogle',
      fontWeight:
        token.componentRadioTextLabelStateCheckedFontWeight.toString(),
      color: token.componentRadioTextLabelTextColorDefault,
    } as TextStyle);
  });
  test('Should render Checked disabled correctly', async () => {
    const rootQueries = render(
      <Radio
        testID="CheckedDisabled"
        label="CheckedDisabled"
        checked
        disabled
        onPress={mockFn}
      />,
    );
    // Check Outer style
    const buttonOuter = await rootQueries.findByTestId(_radioButtonOuter);
    expect(buttonOuter).toHaveStyle({
      borderWidth: token.componentRadioInputOuterBorderWidthDisabled,
      borderColor: token.componentRadioInputOuterBorderColorDisabled,
    });
    // Check Inner Style
    const buttonInner = await rootQueries.findByTestId(_radioButtonInner);
    expect(buttonInner).toHaveStyle({
      backgroundColor:
        token.componentRadioInputInnerStateCheckedBackgroundColorDisabled,
    });
    const label = await rootQueries.findByText('CheckedDisabled');
    expect(label).toHaveStyle({
      fontFamily: 'Bogle',
      fontWeight:
        token.componentRadioTextLabelStateCheckedFontWeight.toString(),
      color: token.componentRadioTextLabelTextColorDisabled,
    } as TextStyle);
  });
});

describe('Test Radio accessability', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should be accessible w/ radio role & correct label', () => {
    const {getByTestId} = render(<Radio label="Agree to terms" />);
    const checkbox = getByTestId('Radio');
    expect(checkbox).toHaveProp('accessible', true);
    expect(checkbox).toHaveProp('accessibilityRole', 'radio');
    expect(checkbox).toHaveProp('accessibilityLabel', 'Agree to terms');
  });

  it('should not be accessible', () => {
    const {getByTestId} = render(<Radio accessible={false} />);
    const checkbox = getByTestId('Radio');
    expect(checkbox).toHaveProp('accessible', false);
  });

  it('should have accessibilityState checked=false', () => {
    const {getByTestId} = render(<Radio />);
    const checkbox = getByTestId('Radio');
    expect(checkbox.props.accessibilityState.checked).toBeFalsy();
  });

  it('should have accessibilityState checked=true', () => {
    const {getByTestId} = render(<Radio checked />);
    const checkbox = getByTestId('Radio');
    expect(checkbox.props.accessibilityState.checked).toBeTruthy();
  });

  it('should have accessibilityState disabled=false', () => {
    const {getByTestId} = render(<Radio />);
    const checkbox = getByTestId('Radio');
    expect(checkbox.props.accessibilityState.disabled).toBeFalsy();
  });

  it('should have accessibilityState disabled=true', () => {
    const {getByTestId} = render(<Radio disabled />);
    const checkbox = getByTestId('Radio');
    expect(checkbox.props.accessibilityState.disabled).toBeTruthy();
  });
});
