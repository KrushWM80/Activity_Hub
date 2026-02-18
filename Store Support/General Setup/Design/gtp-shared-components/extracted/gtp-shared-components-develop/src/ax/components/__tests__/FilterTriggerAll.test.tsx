import * as React from 'react';

import {render, screen} from '@testing-library/react-native';

import {colors} from '../../../next/utils';
import {FilterTriggerAll} from '../FilterTriggerAll';

describe('FilterTriggerAll', () => {
  jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
  jest.useFakeTimers({legacyFakeTimers: true});

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should render default successfully', () => {
    render(<FilterTriggerAll />);
    const filter = screen.getByTestId('FilterTriggerAll');
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

    const slidersIcon = screen.getByTestId('FilterTriggerAll-slidersIcon');
    expect(filter).toContainElement(slidersIcon);
  });

  test('should render with children successfully', () => {
    render(<FilterTriggerAll>Test Filter</FilterTriggerAll>);
    const filter = screen.getByTestId('FilterTriggerAll');
    expect(filter).toContainElement(screen.getByText('Test Filter'));
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

    const slidersIcon = screen.getByTestId('FilterTriggerAll-slidersIcon');
    expect(filter).toContainElement(slidersIcon);
  });

  test('should render appliedCount successfully', () => {
    render(<FilterTriggerAll appliedCount={1}>Test Filter</FilterTriggerAll>);
    const filter = screen.getByTestId('FilterTriggerAll');
    expect(filter).toContainElement(screen.getByText('Test Filter'));
    const appliedCount = screen.getByTestId('FilterTriggerAll-appliedCount  ');
    expect(filter).toContainElement(appliedCount);
    expect(appliedCount).toHaveStyle({
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: colors.blue['130'],
      borderRadius: 1000,
      width: 16,
      height: 16,
      marginLeft: 8,
    });
    const appliedCountText = screen.getByText('1');
    expect(appliedCount).toContainElement(appliedCountText);
    expect(appliedCountText).toHaveStyle({
      color: 'white',
      fontSize: 12,
      lineHeight: 16,
      textAlign: 'center',
    });

    const slidersIcon = screen.getByTestId('FilterTriggerAll-slidersIcon');
    expect(filter).toContainElement(slidersIcon);
  });

  test('should render disabled successfully', () => {
    render(<FilterTriggerAll disabled>Test Filter</FilterTriggerAll>);
    const filter = screen.getByTestId('FilterTriggerAll');
    expect(filter).toContainElement(screen.getByText('Test Filter'));
    expect(filter).toBeDisabled();
    expect(filter).toHaveStyle({
      borderColor: colors.gray['50'], // '#BABBBE',
      backgroundColor: colors.white, // '#FFFFFF',
    });

    const slidersIcon = screen.getByTestId('FilterTriggerAll-slidersIcon');
    expect(slidersIcon).toHaveStyle({
      tintColor: colors.gray['50'].toUpperCase(), // '#BABBBE',
    });
  });

  test('should have correct accessibility', () => {
    render(<FilterTriggerAll />);
    const filter = screen.getByTestId('FilterTriggerAll');
    expect(filter).toHaveProp('accessibilityRole', 'button');
    expect(filter).toHaveProp('accessibilityState', {disabled: false});
    expect(filter).toHaveAccessibleName(
      'Filters, none applied, activate to change filter settings',
    );

    render(<FilterTriggerAll>Test Filter</FilterTriggerAll>);
    const filterWithChildren = screen.getByTestId('FilterTriggerAll');
    expect(filterWithChildren).toHaveAccessibleName(
      'Test Filter, none applied, activate to change filter settings',
    );

    render(<FilterTriggerAll appliedCount={1}>Test Filter</FilterTriggerAll>);
    const filterWithAppliedCount = screen.getByTestId('FilterTriggerAll');
    expect(filterWithAppliedCount).toHaveAccessibleName(
      'Test Filter, 1 applied, activate to change filter settings',
    );
  });
});
