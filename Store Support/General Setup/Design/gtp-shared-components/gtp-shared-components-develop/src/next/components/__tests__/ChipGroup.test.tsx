import * as React from 'react';

import {fireEvent, render} from '@testing-library/react-native';

import {Chip, ChipId} from '../Chip';
import {ChipGroup} from '../ChipGroup';

jest.useFakeTimers({legacyFakeTimers: true});
const mockFn: jest.Mock = jest.fn((selectedIds: Array<ChipId>) => {
  return selectedIds;
});
const chipList = ['All', 'Last 7 Days', 'Last Month', 'Last 6 Months', '2022'];
beforeEach(() => {
  jest.clearAllMocks();
});

describe('Test ChipGroup', () => {
  test('Should render elements.', async () => {
    const screen = render(
      <ChipGroup onPress={(ids) => mockFn(ids)}>
        <Chip id={0}>{chipList[0]}</Chip>
        <Chip id={1}>{chipList[1]}</Chip>
        <Chip id={2}>{chipList[2]}</Chip>
        <Chip id={3}>{chipList[3]}</Chip>
        <Chip id={4}>{chipList[4]}</Chip>
      </ChipGroup>,
    );
    const chipGroup = screen.getByTestId('ChipGroup');
    const firstChip = await screen.findByText(chipList[0]);
    const secondChip = await screen.findByText(chipList[1]);
    const thirdChip = await screen.findByText(chipList[2]);
    const fourthChip = await screen.findByText(chipList[3]);
    const lastChip = await screen.findByText(chipList[4]);
    expect(chipGroup).toContainElement(firstChip);
    expect(chipGroup).toContainElement(secondChip);
    expect(chipGroup).toContainElement(thirdChip);
    expect(chipGroup).toContainElement(fourthChip);
    expect(chipGroup).toContainElement(lastChip);
  });

  test('Should trigger onPress with multiple selection.', async () => {
    const screen = render(
      <ChipGroup multiple onPress={(ids) => mockFn(ids)}>
        <Chip id={0}>{chipList[0]}</Chip>
        <Chip id={1}>{chipList[1]}</Chip>
        <Chip id={2}>{chipList[2]}</Chip>
        <Chip id={3}>{chipList[3]}</Chip>
        <Chip id={4}>{chipList[4]}</Chip>
      </ChipGroup>,
    );
    const firstChip = await screen.findByText(chipList[0]);
    const secondChip = await screen.findByText(chipList[1]);
    const thirdChip = await screen.findByText(chipList[2]);
    const fourthChip = await screen.findByText(chipList[3]);
    const lastChip = await screen.findByText(chipList[4]);
    fireEvent.press(firstChip);
    fireEvent.press(secondChip);
    fireEvent.press(thirdChip);
    fireEvent.press(fourthChip);
    fireEvent.press(lastChip);
    expect(mockFn).toHaveBeenCalledTimes(6);
  });

  test('Should trigger onPress with single selection.', async () => {
    const screen = render(
      <ChipGroup multiple onPress={(ids) => mockFn(ids)}>
        <Chip id={0}>{chipList[0]}</Chip>
        <Chip id={1}>{chipList[1]}</Chip>
        <Chip id={2}>{chipList[2]}</Chip>
        <Chip id={3}>{chipList[3]}</Chip>
        <Chip id={4}>{chipList[4]}</Chip>
      </ChipGroup>,
    );
    const fourthChip = await screen.findByText(chipList[3]);
    fireEvent.press(fourthChip);
    expect(mockFn).toHaveBeenCalledTimes(2);
  });
});
