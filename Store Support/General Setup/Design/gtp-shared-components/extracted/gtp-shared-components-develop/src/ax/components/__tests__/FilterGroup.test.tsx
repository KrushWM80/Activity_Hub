import * as React from 'react';

import {render, screen} from '@testing-library/react-native';

import {colors} from '../../../next/utils';
import {FilterGroup} from '../FilterGroup';
import {FilterTag} from '../FilterTag';
import {FilterToggle} from '../FilterToggle';
import {FilterTriggerAll} from '../FilterTriggerAll';
import {FilterTriggerSingle} from '../FilterTriggerSingle';

describe('FilterGroup', () => {
  jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper');
  jest.useFakeTimers({legacyFakeTimers: true});

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('should render default successfully', () => {
    render(<FilterGroup />);
    const filterGroup = screen.getByTestId('FilterGroup');
    expect(filterGroup).toBeOnTheScreen();
    expect(filterGroup).toBeVisible();
    expect(filterGroup).toHaveStyle({
      width: '100%',
      backgroundColor: colors.white,
      height: 65,
      flexGrow: 0,
      flexShrink: 0,
      borderBottomWidth: 1,
      borderColor: colors.gray['20'], // '#E3E4E5',
    });
  });

  test('should render with wrapping successfully', () => {
    render(<FilterGroup wrapping />);
    const filterGroup = screen.getByTestId('FilterGroup');
    expect(filterGroup).toHaveStyle({
      width: '100%',
      flexDirection: 'row',
      flexWrap: 'wrap',
      justifyContent: 'flex-start',
      alignItems: 'flex-start',
      backgroundColor: colors.white,
      borderBottomWidth: 1,
      borderColor: colors.gray['20'], // '#E3E4E5',
      padding: 16,
      columnGap: 12,
    });
  });

  test('should render with children successfully', () => {
    render(
      <FilterGroup>
        <FilterTriggerAll />
        <FilterTriggerSingle>Trigger Single</FilterTriggerSingle>
        <FilterToggle>Toggle</FilterToggle>
        <FilterTag>Tag</FilterTag>
      </FilterGroup>,
    );
    const filterGroup = screen.getByTestId('FilterGroup');
    expect(filterGroup).toContainElement(
      screen.getByTestId('FilterTriggerAll'),
    );
    expect(filterGroup).toContainElement(
      screen.getByTestId('FilterTriggerSingle'),
    );
    expect(filterGroup).toContainElement(screen.getByTestId('FilterToggle'));
    expect(filterGroup).toContainElement(screen.getByTestId('FilterTag'));
  });

  test('should render with children and wrapping successfully', () => {
    render(
      <FilterGroup wrapping>
        <FilterTriggerAll />
        <FilterTriggerSingle>Trigger Single</FilterTriggerSingle>
        <FilterToggle>Toggle</FilterToggle>
        <FilterTag>Tag</FilterTag>
      </FilterGroup>,
    );
    const filterGroup = screen.getByTestId('FilterGroup');
    expect(filterGroup).toContainElement(
      screen.getByTestId('FilterTriggerAll'),
    );
    expect(filterGroup).toContainElement(
      screen.getByTestId('FilterTriggerSingle'),
    );
    expect(filterGroup).toContainElement(screen.getByTestId('FilterToggle'));
    expect(filterGroup).toContainElement(screen.getByTestId('FilterTag'));
  });
});
