import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Checkbox';
import {fireEvent, render, screen} from '@testing-library/react-native';
import {getHostChildren} from '@testing-library/react-native/build/helpers/component-tree';

import {Checkbox} from '../Checkbox';

const mockFn = jest.fn();

describe('Test Checkbox', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  test('Should trigger onPress correctly', async () => {
    const rootQueries = render(<Checkbox label="Enabled" onPress={mockFn} />);

    expect(mockFn).toHaveBeenCalledTimes(0);
    const checkbox = await rootQueries.findByText('Enabled');
    fireEvent.press(checkbox);
    expect(mockFn).toHaveBeenCalledTimes(1);
  });
  test('Should not trigger onPress when disabled', async () => {
    const rootQueries = render(
      <Checkbox label="Disabled Checkbox" disabled onPress={mockFn} />,
    );

    expect(mockFn).toHaveBeenCalledTimes(0);
    const checkbox = await rootQueries.findByText('Disabled Checkbox');
    fireEvent.press(checkbox);
    expect(mockFn).toHaveBeenCalledTimes(0);
  });
  test('Should render Unchecked correctly', async () => {
    const rootQueries = render(
      <Checkbox testID="Unchecked" label="Unchecked" onPress={mockFn} />,
    );
    const checkbox = await rootQueries.findByTestId('Unchecked');
    const checkIcon = rootQueries.queryByTestId('CheckIcon');
    expect(checkbox).not.toContainElement(checkIcon);
    const indeterminateIcon = rootQueries.queryByTestId('MinusIcon');
    expect(checkbox).not.toContainElement(indeterminateIcon);
    expect(getHostChildren(checkbox)[0]).toHaveStyle({
      borderColor: token.componentCheckboxInputBorderColorDefault,
      borderWidth: token.componentCheckboxInputBorderWidthDefault,
      backgroundColor: token.componentCheckboxInputBackgroundColorDefault,
    });
    expect(getHostChildren(checkbox)[1]).toHaveStyle({
      fontFamily: 'Bogle',
      fontWeight: '400',
      color: token.componentCheckboxLabelTextColorDefault,
    });
  });
  test('Should render Disabled Unchecked correctly', async () => {
    const rootQueries = render(
      <Checkbox
        testID="DisabledUnchecked"
        label="DisabledUnchecked"
        disabled
        onPress={mockFn}
      />,
    );
    const checkbox = await rootQueries.findByTestId('DisabledUnchecked');
    const checkIcon = rootQueries.queryByTestId('CheckIcon');
    expect(checkbox).not.toContainElement(checkIcon);
    const indeterminateIcon = rootQueries.queryByTestId('MinusIcon');
    expect(checkbox).not.toContainElement(indeterminateIcon);
    expect(getHostChildren(checkbox)[0]).toHaveStyle({
      borderColor: token.componentCheckboxInputBorderColorDisabled,
      borderWidth: token.componentCheckboxInputBorderWidthDisabled,
      backgroundColor: token.componentCheckboxInputBackgroundColorDisabled,
    });
    expect(getHostChildren(checkbox)[1]).toHaveStyle({
      fontFamily: 'Bogle',
      fontWeight: '400',
      color: token.componentCheckboxLabelTextColorDisabled,
    });
  });
  test('Should render Checked correctly', async () => {
    const rootQueries = render(
      <Checkbox testID="Checked" label="Checked" checked onPress={mockFn} />,
    );
    const checkbox = await rootQueries.findByTestId('Checked');
    const iconElement = rootQueries.queryByTestId('CheckIcon');
    expect(checkbox).toContainElement(iconElement);
    expect(getHostChildren(checkbox)[0]).toHaveStyle({
      borderColor: token.componentCheckboxInputBorderColorDefault,
      borderWidth: token.componentCheckboxInputBorderWidthDefault,
      backgroundColor:
        token.componentCheckboxInputStateCheckedBackgroundColorDefault,
    });
    expect(getHostChildren(checkbox)[1]).toHaveStyle({
      fontFamily: 'Bogle',
      fontWeight: '700',
      color: token.componentCheckboxLabelTextColorDefault,
    });
  });
  test('Should render Disabled Checked correctly', async () => {
    const rootQueries = render(
      <Checkbox
        testID="DisabledChecked"
        label="Disabled Checked"
        checked
        disabled
        onPress={mockFn}
      />,
    );
    const checkbox = await rootQueries.findByTestId('DisabledChecked');
    const iconElement = rootQueries.queryByTestId('CheckIcon');
    expect(checkbox).toContainElement(iconElement);
    expect(getHostChildren(checkbox)[0]).toHaveStyle({
      borderColor: token.componentCheckboxInputBorderColorDisabled,
      borderWidth: token.componentCheckboxInputBorderWidthDisabled,
      backgroundColor:
        token.componentCheckboxInputStateCheckedBackgroundColorDisabled,
    });
    expect(getHostChildren(checkbox)[1]).toHaveStyle({
      fontFamily: 'Bogle',
      fontWeight: '700',
      color: token.componentCheckboxLabelTextColorDisabled,
    });
  });
  test('Should render Indeterminate correctly', async () => {
    const rootQueries = render(
      <Checkbox
        testID="Indeterminate"
        label="Indeterminate"
        indeterminate
        onPress={mockFn}
      />,
    );
    const checkbox = await rootQueries.findByTestId('Indeterminate');
    const iconElement = rootQueries.queryByTestId('MinusIcon');
    expect(checkbox).toContainElement(iconElement);
    expect(getHostChildren(checkbox)[0]).toHaveStyle({
      borderColor: token.componentCheckboxInputBorderColorDefault,
      borderWidth: token.componentCheckboxInputBorderWidthDefault,
      backgroundColor:
        token.componentCheckboxInputStateIndeterminateBackgroundColorDefault,
    });
    expect(getHostChildren(checkbox)[1]).toHaveStyle({
      fontFamily: 'Bogle',
      fontWeight: '700',
      color: token.componentCheckboxLabelTextColorDefault,
    });
  });
  test('Should render Disabled Indeterminate correctly', async () => {
    const rootQueries = render(
      <Checkbox
        testID="Disabled Indeterminate"
        label="Disabled Indeterminate"
        indeterminate
        disabled
        onPress={mockFn}
      />,
    );
    const checkbox = await rootQueries.findByTestId('Disabled Indeterminate');
    const iconElement = rootQueries.queryByTestId('MinusIcon');
    expect(checkbox).toContainElement(iconElement);
    expect(getHostChildren(checkbox)[0]).toHaveStyle({
      borderColor: token.componentCheckboxInputBorderColorDisabled,
      borderWidth: token.componentCheckboxInputBorderWidthDisabled,
      backgroundColor:
        token.componentCheckboxInputStateIndeterminateBackgroundColorDisabled,
    });
    expect(getHostChildren(checkbox)[1]).toHaveStyle({
      fontFamily: 'Bogle',
      fontWeight: '700',
      color: token.componentCheckboxLabelTextColorDisabled,
    });
  });
});

describe('Test Checkbox accessability', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should be accessible w/ checkbox role & correct label and state', () => {
    render(<Checkbox label="Agree to terms" />);
    let checkbox = screen.getByTestId('Checkbox');
    expect(checkbox).toHaveProp(
      'accessibilityLabel',
      'Agree to terms checkbox',
    );
    expect(checkbox).toHaveProp('accessibilityState', {
      busy: undefined,
      checked: false,
      disabled: false,
      expanded: undefined,
      selected: undefined,
    });

    render(<Checkbox label="Agree to terms" disabled />);
    checkbox = screen.getByTestId('Checkbox');
    expect(checkbox).toHaveProp('accessibilityState', {
      busy: undefined,
      checked: false,
      disabled: true,
      expanded: undefined,
      selected: undefined,
    });

    render(<Checkbox label="Agree to terms" checked />);
    checkbox = screen.getByTestId('Checkbox');
    expect(checkbox).toHaveProp('accessibilityState', {
      busy: undefined,
      checked: true,
      disabled: false,
      expanded: undefined,
      selected: undefined,
    });

    render(<Checkbox label="Agree to terms" checked disabled />);
    checkbox = screen.getByTestId('Checkbox');
    expect(checkbox).toHaveProp('accessibilityState', {
      busy: undefined,
      checked: true,
      disabled: true,
      expanded: undefined,
      selected: undefined,
    });
  });

  it('should not be accessible', () => {
    const {getByTestId} = render(<Checkbox accessible={false} />);
    const checkbox = getByTestId('Checkbox');
    expect(checkbox).toHaveProp('accessible', false);
  });

  it('should have accessibilityState checked=false', () => {
    const {getByTestId} = render(<Checkbox />);
    const checkbox = getByTestId('Checkbox');
    expect(checkbox.props.accessibilityState.checked).toBeFalsy();
  });

  it('should have accessibilityState checked=true', () => {
    const {getByTestId} = render(<Checkbox checked />);
    const checkbox = getByTestId('Checkbox');
    expect(checkbox.props.accessibilityState.checked).toBeTruthy();
  });

  it('should have accessibilityState disabled=false', () => {
    const {getByTestId} = render(<Checkbox />);
    const checkbox = getByTestId('Checkbox');
    expect(checkbox.props.accessibilityState.disabled).toBeFalsy();
  });

  it('should have accessibilityState disabled=true', () => {
    const {getByTestId} = render(<Checkbox disabled />);
    const checkbox = getByTestId('Checkbox');
    expect(checkbox.props.accessibilityState.disabled).toBeTruthy();
  });
});
