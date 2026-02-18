import * as React from 'react';

import {render, screen} from '@testing-library/react-native';

import {colors} from '../../../next/utils';
import {FilterTriggerSingle} from '../FilterTriggerSingle';

describe('FilterTriggerSingle', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should render default successfully', () => {
    render(<FilterTriggerSingle>Test Filter</FilterTriggerSingle>);
    const filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toContainElement(screen.getByText('Test Filter'));
    expect(filter).toBeOnTheScreen();
    expect(filter).toBeVisible();

    const chevronIcon = screen.getByTestId('ChevronDownIcon');
    expect(filter).toContainElement(chevronIcon);
  });

  test('should render open and applied successfully', () => {
    render(<FilterTriggerSingle isOpen>Test Filter</FilterTriggerSingle>);
    let filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toHaveStyle({
      borderWidth: 1,
      borderColor: colors.gray['160'], // '#2E2F32',
      backgroundColor: colors.white, // '#FFFFFF'
    });

    render(<FilterTriggerSingle isApplied>Test Filter</FilterTriggerSingle>);
    filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.blue['100'], // #0071DC'
      backgroundColor: colors.blue['5'], // #F2F8FD'
    });

    render(
      <FilterTriggerSingle isOpen isApplied>
        Test Filter
      </FilterTriggerSingle>,
    );
    filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.blue['160'], // '#002D58',
      backgroundColor: colors.blue['5'], // #F2F8FD'
    });
  });

  test('should render pressed successfully', () => {
    render(
      <FilterTriggerSingle testOnly_pressed>Test Filter</FilterTriggerSingle>,
    );
    let filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.gray['160'], // '#2E2F32',
      backgroundColor: colors.white, // '#FFFFFF'
    });

    render(
      <FilterTriggerSingle isOpen testOnly_pressed>
        Test Filter
      </FilterTriggerSingle>,
    );
    filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.gray['160'], // '#2E2F32',
      backgroundColor: colors.white, // '#FFFFFF'
    });

    render(
      <FilterTriggerSingle isApplied testOnly_pressed>
        Test Filter
      </FilterTriggerSingle>,
    );
    filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.blue['100'], // '#0071DC',
      backgroundColor: colors.blue['5'], // #F2F8FD'
    });

    render(
      <FilterTriggerSingle isOpen isApplied testOnly_pressed>
        Test Filter
      </FilterTriggerSingle>,
    );
    filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.blue['160'], // '#002D58',
      backgroundColor: colors.blue['5'], // #F2F8FD'
    });
  });

  test('should render disabled successfully', () => {
    render(<FilterTriggerSingle disabled>Test Filter</FilterTriggerSingle>);
    let filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toBeDisabled();
    expect(filter).toHaveStyle({
      borderWidth: 1,
      borderColor: colors.gray['50'], // '#BABBBE',
      backgroundColor: colors.white, // '#FFFFFF'
    });

    const chevronIcon = screen.getByTestId('ChevronDownIcon');
    expect(chevronIcon).toHaveStyle({
      tintColor: colors.gray['50'].toUpperCase(), // '#BABBBE',
    });

    render(
      <FilterTriggerSingle isOpen disabled>
        Test Filter
      </FilterTriggerSingle>,
    );
    filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toBeDisabled();
    expect(filter).toHaveStyle({
      borderWidth: 1,
      borderColor: colors.gray['50'], // '#BABBBE',
      backgroundColor: colors.white, // '#FFFFFF'
    });

    render(
      <FilterTriggerSingle isApplied disabled>
        Test Filter
      </FilterTriggerSingle>,
    );
    filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toBeDisabled();
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.gray['50'], // '#BABBBE',
      backgroundColor: colors.white, // '#FFFFFF'
    });

    render(
      <FilterTriggerSingle isOpen isApplied disabled>
        Test Filter
      </FilterTriggerSingle>,
    );
    filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toBeDisabled();
    expect(filter).toHaveStyle({
      borderWidth: 2,
      borderColor: colors.gray['50'], // '#BABBBE',
      backgroundColor: colors.white, // '#FFFFFF'
    });
  });

  test('should have correct accessibility', () => {
    render(<FilterTriggerSingle>Test Filter</FilterTriggerSingle>);
    let filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toHaveProp('accessibilityRole', 'button');
    expect(filter).toHaveProp('accessibilityState', {disabled: false});
    expect(filter).toHaveAccessibleName(
      'Filter by Test Filter, not applied, activate to change filter',
    );

    render(<FilterTriggerSingle isApplied>Test Filter</FilterTriggerSingle>);
    filter = screen.getByTestId('FilterTriggerSingle');
    expect(filter).toHaveAccessibleName(
      'Filter by Test Filter, applied, activate to change filter',
    );
  });
});
