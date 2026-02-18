import * as React from 'react';

import {fireEvent, render, screen} from '@testing-library/react-native';
import {Icons} from '@walmart/gtp-shared-icons';

import {colors} from '../../../next/utils';
import {FilterToggle} from '../FilterToggle';

describe('FilterToggle', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should render default successfully', () => {
    render(<FilterToggle>Test Filter</FilterToggle>);
    const filter = screen.getByTestId('FilterToggle');
    expect(filter).toHaveTextContent('Test Filter');
    expect(filter).toBeOnTheScreen();
    expect(filter).toBeVisible();
  });

  test('should render pressed style when pressed', () => {
    render(<FilterToggle testOnly_pressed>Test Filter</FilterToggle>);
    const filter = screen.getByTestId('FilterToggle');
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.gray['160'], // '#BABBBE',
      backgroundColor: colors.white, // '#FFFFFF',
    });

    render(
      <FilterToggle testOnly_pressed isApplied>
        Test Filter
      </FilterToggle>,
    );
    const filterApplied = screen.getByTestId('FilterToggle');
    expect(filterApplied).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.blue['160'], // '#005CB8',
      backgroundColor: colors.blue['20'], // '#CCE3F8'
    });
  });

  test('should render applied style when applied', () => {
    render(<FilterToggle isApplied>Test Filter</FilterToggle>);
    const filter = screen.getByTestId('FilterToggle');
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.blue['100'], // '#0071DC',
      backgroundColor: colors.blue['5'], // '#F2F8FD',
    });
  });

  test('should render disabled style when disabled', () => {
    render(<FilterToggle disabled>Test Filter</FilterToggle>);
    const filter = screen.getByTestId('FilterToggle');
    expect(filter).toBeDisabled();
    expect(filter).toHaveStyle({
      borderWidth: 1,
      borderColor: colors.gray['50'], // '#BABBBE',
      backgroundColor: colors.white, // '#FFFFFF',
    });
  });

  test('should have correct accessibility', () => {
    render(<FilterToggle>Test Filter</FilterToggle>);
    const filter = screen.getByTestId('FilterToggle');
    expect(filter).toHaveProp('accessibilityRole', 'button');
    expect(filter).not.toBeSelected();
    expect(filter).toHaveAccessibleName('Filter by Test Filter, not selected');

    render(<FilterToggle isApplied>Test Filter</FilterToggle>);
    const filterApplied = screen.getByTestId('FilterToggle');
    expect(filterApplied).toBeSelected();
    expect(filterApplied).toHaveAccessibleName(
      'Filter by Test Filter, selected',
    );
  });

  test('should call onPress when pressed', () => {
    const onPress = jest.fn();
    render(<FilterToggle onPress={onPress}>Test Filter</FilterToggle>);
    const filter = screen.getByTestId('FilterToggle');
    fireEvent.press(filter);
    expect(onPress).toHaveBeenCalledTimes(1);
  });

  test('should not call onPress when disabled', () => {
    const onPress = jest.fn();
    render(
      <FilterToggle onPress={onPress} disabled>
        Test Filter
      </FilterToggle>,
    );
    const filter = screen.getByTestId('FilterToggle');
    fireEvent.press(filter);
    expect(onPress).not.toHaveBeenCalled();
  });

  test('should have leading element', () => {
    render(
      <FilterToggle leading={<Icons.AssociateIcon />}>
        Test Filter
      </FilterToggle>,
    );
    const filter = screen.getByTestId('FilterToggle');
    expect(filter).toContainElement(screen.getByTestId('AssociateIcon'));
  });
});
