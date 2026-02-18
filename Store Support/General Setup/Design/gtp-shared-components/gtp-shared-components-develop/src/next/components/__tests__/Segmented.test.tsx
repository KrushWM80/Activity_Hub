import * as React from 'react';
import {TextStyle} from 'react-native';

import {fireEvent, render} from '@testing-library/react-native';

import {getFont, Weights} from '../../../theme/font';
import {colors} from '../../utils';
import {Segment, selectionStyles} from '../Segment';
import {Segmented} from '../Segmented';

const mockFn = jest.fn();

describe('Should render Segments correctly for different selection states', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });
  test('Should render Segments with Default Selection', async () => {
    const rootQueries = render(
      <Segmented onChange={mockFn}>
        <Segment>First</Segment>
        <Segment>Second</Segment>
        <Segment>Third</Segment>
      </Segmented>,
    );

    if (Segmented.displayName) {
      const segmented = await rootQueries.findByTestId(Segmented.displayName);

      // Expect Segmented Container Styling
      expect(segmented).toHaveStyle([
        {
          borderRadius: 4,
          padding: 2,
          alignItems: 'stretch',
          flexDirection: 'row',
          backgroundColor: colors.gray['20'],
        },
      ]);
    }
    if (Segment.displayName) {
      const segment = await rootQueries.findAllByTestId(Segment.displayName);

      // Expect First Segment Container Styling
      // Default First Segment is selected
      // Default Segment Size: PaddingVertical - 8
      expect(segment[0]).toHaveStyle([
        {
          borderRadius: 4,
          paddingVertical: 4,
          justifyContent: 'center',
          backgroundColor: selectionStyles.selected.backgroundColor,
          alignSelf: 'stretch',
          flex: 1,
        },
      ]);

      // Expect First Segment Container Styling
      expect(segment[1]).toHaveStyle([
        {
          borderRadius: 4,
          paddingVertical: 4,
          justifyContent: 'center',
          backgroundColor: selectionStyles.default.backgroundColor,
          alignSelf: 'stretch',
          flex: 1,
        },
      ]);

      // Expect First Segment Text Styling
      const segmentFirstText = await rootQueries.findByText('First');

      expect(segmentFirstText).toHaveStyle([
        {
          ...getFont(selectionStyles.selected.fontWeight as Weights),
          fontSize: 14,
          lineHeight: 20,
          color: selectionStyles.selected.textColor,
          textAlign: 'center',
        } as TextStyle,
      ]);

      // Expect Third Segment to be Selected
      fireEvent.press(segment[2]);
      expect(mockFn).toHaveBeenCalledTimes(1);
    }
  });

  test('Should render Segments with Selection Disabled', async () => {
    const rootQueries = render(
      <Segmented disabled={true}>
        <Segment>First</Segment>
        <Segment>Second</Segment>
        <Segment>Third</Segment>
      </Segmented>,
    );
    if (Segment.displayName) {
      const segment = await rootQueries.findAllByTestId(Segment.displayName);

      // Expect First Segment Container Styling with Selection - SelectedDisabled
      expect(segment[0]).toHaveStyle([
        {
          borderRadius: 4,
          paddingVertical: 4,
          justifyContent: 'center',
          backgroundColor: selectionStyles.selectedDisabled.backgroundColor,
          alignSelf: 'stretch',
          flex: 1,
        },
      ]);

      // Expect Second Segment Container Styling with Selection - Disabled
      expect(segment[1]).toHaveStyle([
        {
          borderRadius: 4,
          paddingVertical: 4,
          justifyContent: 'center',
          backgroundColor: selectionStyles.disabled.backgroundColor,
          alignSelf: 'stretch',
          flex: 1,
        },
      ]);

      // Expect First Segment Text Styling with Selection - SelectionDisabled
      const segmentFirstText = await rootQueries.findByText('First');

      expect(segmentFirstText).toHaveStyle([
        {
          ...getFont(selectionStyles.selectedDisabled.fontWeight as Weights),
          fontSize: 14,
          lineHeight: 20,
          color: selectionStyles.selectedDisabled.textColor,
          textAlign: 'center',
        } as TextStyle,
      ]);

      // Expect Third Segment to be Disabled
      fireEvent.press(segment[2]);
      expect(mockFn).toHaveBeenCalledTimes(0);
    }
  });

  test('Should render Segments with Size Large', async () => {
    const rootQueries = render(
      <Segmented size="large">
        <Segment>First</Segment>
        <Segment>Second</Segment>
        <Segment>Third</Segment>
      </Segmented>,
    );
    if (Segment.displayName) {
      const segment = await rootQueries.findAllByTestId(Segment.displayName);

      // Expect First Segment Container Styling with large size
      // Expect PaddingVertical - 8
      expect(segment[0]).toHaveStyle([
        {
          borderRadius: 4,
          paddingVertical: 8,
          justifyContent: 'center',
          backgroundColor: selectionStyles.selected.backgroundColor,
          alignSelf: 'stretch',
          flex: 1,
        },
      ]);
    }
  });
});
