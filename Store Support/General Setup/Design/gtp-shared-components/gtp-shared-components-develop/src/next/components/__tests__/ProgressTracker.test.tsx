import * as React from 'react';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/ProgressTracker';
import {render} from '@testing-library/react-native';

import {
  measureMarginLeft,
  ProgressTracker,
  ProgressTrackerVariant,
  resolveChildStyle,
  variantsStyle,
} from '../ProgressTracker';
import {ProgressTrackerItem} from '../ProgressTrackerItem';

describe.each<ProgressTrackerVariant>(['info', 'warning', 'error', 'success'])(
  'Should render ProgressTracker correctly for Variants',
  (variant) => {
    test(`Test ProgressTracker variant="${variant} `, async () => {
      const wrapper = render(
        <ProgressTracker variant={variant} activeIndex={2}>
          {[...Array(4).keys()].map((val) => (
            <ProgressTrackerItem key={val} children={`Label${val}`} />
          ))}
        </ProgressTracker>,
      );
      const ProgressTrackerContainer = await wrapper.findByTestId(
        'ProgressTracker',
      );
      expect(ProgressTrackerContainer).toHaveStyle({
        flexDirection: 'row',
        height: token.componentProgressTrackerTrackContainerHeight, //16
        width: token.componentProgressTrackerTrackContainerWidth, //"100%"
        paddingHorizontal:
          token.componentProgressTrackerTrackContainerPaddingHorizontal, //6
        paddingVertical:
          token.componentProgressTrackerTrackContainerPaddingVertical, //0
        justifyContent:
          token.componentProgressTrackerTrackContainerAlignHorizontal, //"center"
        alignItems: token.componentProgressTrackerTrackContainerAlignVertical, //"center"});
      });
      const stepOuternotExist = await wrapper.findByTestId(
        'ProgressTracker-step-outer-0',
      );
      expect(stepOuternotExist.props.style[0].borderColor).toBeUndefined();

      const stepOuterExist = await wrapper.findByTestId(
        'ProgressTracker-step-outer-2',
      );
      expect(stepOuterExist.props.style[0].borderColor).toEqual(
        variantsStyle[variant].borderColor,
      );

      const uncompletedstep = await wrapper.findByTestId(
        'ProgressTracker-step-3',
      );
      expect(uncompletedstep.props.style[1].backgroundColor).toEqual(
        token.componentProgressTrackerItemIndicatorInnerBackgroundColor,
      );

      const completedstep = await wrapper.findByTestId(
        'ProgressTracker-step-1',
      );
      expect(completedstep.props.style[1].backgroundColor).toEqual(
        variantsStyle[variant].backgroundColor,
      );

      const completedTrack = await wrapper.findByTestId(
        'ProgressTracker-completed-track',
      );
      expect(completedTrack.props.style[0].backgroundColor).toEqual(
        variantsStyle[variant].completedBackgroundColor,
      );

      const defaultTrack = await wrapper.findByTestId(
        'ProgressTracker-default-track',
      );
      expect(defaultTrack.props.style.backgroundColor).toEqual(
        token.componentProgressTrackerTrackBackgroundColor,
      );

      const activeLabel = await wrapper.findByText('Label2');

      expect(activeLabel.props.style[0].color).toEqual(
        token.componentProgressTrackerItemTextLabelStateIsCurrentTextColor,
      );
      const nonActiveLabel = await wrapper.findByText('Label1');

      expect(nonActiveLabel.props.style[1][1][2]?.color).toBeUndefined();
      expect(nonActiveLabel.props.style[1][1].color).toEqual(
        token.componentProgressTrackerItemTextLabelTextColor,
      );
    });
    test(`resolveChildStyle variant="${variant}`, () => {
      const firstItem = resolveChildStyle(0, 2, 5, 200, variant);
      expect(firstItem).toEqual({
        color: '#74767c',
        marginLeft: 0,
        textAlign: 'left',
        width: 200,
      });
      const secondItem = resolveChildStyle(1, 2, 5, 200, variant);
      expect(secondItem).toEqual({marginLeft: 1, color: '#74767c', width: 200});
      const thirdItem = resolveChildStyle(2, 2, 5, 200, variant);
      expect(thirdItem).toEqual({
        color: '#2e2f32',
        marginLeft: 20,
        width: 200,
      });
      const fourthItem = resolveChildStyle(3, 2, 5, 200, variant);
      expect(fourthItem).toEqual({
        marginLeft: 30,
        color: '#74767c',
        width: 200,
      });
      const fifthItem = resolveChildStyle(4, 2, 5, 200, variant);
      expect(fifthItem).toEqual({
        color: '#74767c',
        marginLeft: 0,
        paddingRight: 0,
        textAlign: 'right',
        width: 200,
      });
    });
  },
);

describe('measureMarginLeft', () => {
  test('Measure MarginLeft for different index', () => {
    const firstMarginLeft = measureMarginLeft(0, 5, 2);
    expect(firstMarginLeft).toEqual(0);
    const secondMarginLeft = measureMarginLeft(1, 5, 2);
    expect(secondMarginLeft).toEqual(1);
    const thirdMarginLeft = measureMarginLeft(2, 5, 2);
    expect(thirdMarginLeft).toEqual(20);
    const fourthMarginLeft = measureMarginLeft(3, 5, 2);
    expect(fourthMarginLeft).toEqual(30);
    const fifthMarginLeft = measureMarginLeft(4, 5, 2);
    expect(fifthMarginLeft).toEqual(0);
  });
});
