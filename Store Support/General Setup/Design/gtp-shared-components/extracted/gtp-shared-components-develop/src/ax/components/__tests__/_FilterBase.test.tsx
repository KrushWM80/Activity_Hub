import * as React from 'react';

import {fireEvent, render, screen} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {colors} from '../../../next/utils';
import {_FilterBase} from '../_FilterBase';

describe('_FilterBase', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should render default successfully', () => {
    render(<_FilterBase>Test Filter</_FilterBase>);
    const filter = screen.getByTestId('_FilterBase');
    expect(filter).toHaveTextContent('Test Filter');
    expect(filter).toBeOnTheScreen();
    expect(filter).toBeVisible();
    expect(filter).toHaveStyle({
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      borderRadius: 10000,
      borderWidth: 1,
      borderColor: colors.gray['80'], // '#909196'
      backgroundColor: colors.white, // '#FFFFFF'
      height: 32,
      paddingHorizontal: 8,
      marginVertical: 4,
    });

    const filterText = screen.getByText('Test Filter');
    expect(filterText).toHaveStyle({
      fontSize: 14,
      color: colors.gray['160'], // '#2E2F32'
    });
  });

  test('should render pressed style when pressed', () => {
    render(<_FilterBase testOnly_pressed>Test Filter</_FilterBase>);
    const filter = screen.getByTestId('_FilterBase');
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.gray['160'], // '#2E2F32'
      backgroundColor: colors.white, // '#FFFFFF'
    });
  });

  test('should render applied style when applied', () => {
    render(<_FilterBase applied>Test Filter</_FilterBase>);
    const filter = screen.getByTestId('_FilterBase');
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.blue['100'], // #0071DC'
      backgroundColor: colors.blue['5'], // #F2F8FD'
    });

    const filterText = screen.getByText('Test Filter');
    expect(filterText).toHaveStyle({
      color: colors.gray['160'], // '#2E2F32'
    });

    render(
      <_FilterBase applied testOnly_pressed>
        Test Filter
      </_FilterBase>,
    );
    const filterPressed = screen.getByTestId('_FilterBase');
    expect(filterPressed).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.blue['160'], // '#002D58'
      backgroundColor: colors.blue['20'], // '#CCE3F8'
    });
  });

  test('should render disabled style when disabled', () => {
    render(<_FilterBase disabled>Test Filter</_FilterBase>);
    const filter = screen.getByTestId('_FilterBase');
    expect(filter).toHaveStyle({
      borderColor: colors.gray['50'], // '#BABBBE'
      backgroundColor: colors.white, // '#FFFFFF'
    });

    const filterText = screen.getByText('Test Filter');
    expect(filterText).toHaveStyle({
      color: colors.gray['50'], // '#BABBBE'
    });
  });

  test('should have correct accessibility', () => {
    render(<_FilterBase>Test Filter</_FilterBase>);
    const filter = screen.getByTestId('_FilterBase');
    expect(filter).toHaveProp('accessibilityRole', 'button');
    expect(filter).toHaveProp('accessibilityState', {disabled: false});
    expect(filter).toHaveAccessibleName('Test Filter');
  });

  test('should call onPress when clicked', async () => {
    const mockFn = jest.fn();
    render(<_FilterBase onPress={mockFn}>Test Filter</_FilterBase>);
    const filter = screen.getByTestId('_FilterBase');
    fireEvent.press(filter);

    expect(mockFn).toHaveBeenCalled();
  });

  test('should not call onPress when disabled', async () => {
    const mockFn = jest.fn();
    render(
      <_FilterBase onPress={mockFn} disabled>
        Test Filter
      </_FilterBase>,
    );
    const filter = screen.getByTestId('_FilterBase');
    fireEvent.press(filter);

    expect(mockFn).not.toHaveBeenCalled();
  });

  test('should have leading and trailing elements', () => {
    render(
      <_FilterBase
        leading={<Icons.ArrowDownIcon />}
        trailing={<Icons.ArrowUpIcon />}>
        Test Filter
      </_FilterBase>,
    );
    const filter = screen.getByTestId('_FilterBase');
    const leadingIcon = screen.getByTestId('ArrowDownIcon');
    const trailingIcon = screen.getByTestId('ArrowUpIcon');
    expect(filter).toContainElement(leadingIcon);
    expect(filter).toContainElement(trailingIcon);
    expect(filter).toHaveTextContent('Test Filter');
  });
});
