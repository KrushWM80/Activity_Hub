import * as React from 'react';
import {
  FlexStyle,
  LayoutChangeEvent,
  StyleProp,
  StyleSheet,
  TextStyle,
  View,
  ViewProps,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/ProgressTracker';
import flattenChildren from 'react-keyed-flatten-children';

import {a11yRole} from '../utils';

export const variantsStyle = {
  error: {
    backgroundColor:
      token.componentProgressTrackerIndicatorVariantErrorBackgroundColor, // "#de1c24"
    completedBackgroundColor:
      token.componentProgressTrackerItemIndicatorInnerStateIsActiveVariantErrorBackgroundColor, // "#de1c24"
    borderColor:
      token.componentProgressTrackerItemIndicatorOuterStateIsCurrentVariantErrorBorderColor, // "#de1c24"
  },
  info: {
    backgroundColor:
      token.componentProgressTrackerIndicatorVariantInfoBackgroundColor, //"#0071dc"
    completedBackgroundColor:
      token.componentProgressTrackerItemIndicatorInnerStateIsActiveVariantInfoBackgroundColor, //"#0071dc"
    borderColor:
      token.componentProgressTrackerItemIndicatorOuterStateIsCurrentVariantInfoBorderColor, //"#0071dc"
  },
  success: {
    backgroundColor:
      token.componentProgressTrackerIndicatorVariantSuccessBackgroundColor, //"#2a8703"
    completedBackgroundColor:
      token.componentProgressTrackerItemIndicatorInnerStateIsActiveVariantSuccessBackgroundColor, //"#2a8703",
    borderColor:
      token.componentProgressTrackerItemIndicatorOuterStateIsCurrentVariantSuccessBorderColor, //"#2a8703",
  },
  warning: {
    backgroundColor:
      token.componentProgressTrackerIndicatorVariantWarningBackgroundColor, //"#b36a16"
    completedBackgroundColor:
      token.componentProgressTrackerItemIndicatorInnerStateIsActiveVariantWarningBackgroundColor, //"#b36a16"
    borderColor:
      token.componentProgressTrackerItemIndicatorOuterStateIsCurrentVariantWarningBorderColor, //"#b36a16"
  },
};
export type ProgressTrackerVariant = 'error' | 'info' | 'success' | 'warning';

// ---------------
// Props
// ---------------
export type ProgressTrackerProps = ViewProps & {
  /**
   * The active index for the progress tracker..
   * @default 0
   */
  activeIndex?: number;
  /**
   * The content for the progress tracker.
   * It is marked as optional for backwards compatibility only
   */
  children?: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * The variant for the progress tracker.
   * @default info.
   */
  variant?: ProgressTrackerVariant;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  stepCount?: number;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  completeCount?: number;
  /**
   *
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  labels?: any;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  title?: any;
  /**
   *  @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  subtitle?: any;
  /**
   *  @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  button?: any;
  /**
   *  @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  link?: any;
  /**
   * @deprecated it has no effect. Use <strong>variant</strong> instead.
   */
  type?: any;
};

/**
 * Progress tracker is a visual representation of a users progress through a set of steps.
 * They inform the user of the number of steps required to complete a specified process.
 *
 * ## Usage
 * ```js
 * import {ProgressTracker, ProgressTrackerItem} from '@walmart/gtp-shared-components`;
 *
 * <ProgressTracker activeIndex={2} variant="info" >
 *    <ProgressTrackerItem>Label1</ProgressTrackerItem>
 *    <ProgressTrackerItem>Label2</ProgressTrackerItem>
 *    <ProgressTrackerItem>Label3</ProgressTrackerItem>
 *    <ProgressTrackerItem>Label4</ProgressTrackerItem>
 * </ProgressTracker>
 * ```
 */
const ProgressTracker: React.FC<ProgressTrackerProps> = (props) => {
  const {
    activeIndex = 0,
    children,
    UNSAFE_style = {},
    variant = 'info',
    ...rest
  } = props;
  const [labelWidth, setLabelWidth] = React.useState(0);
  const kids = flattenChildren(children);
  const stepCount = kids.length;
  const lastIndex = stepCount > 0 ? stepCount - 1 : 0;
  const validActiveIndex = activeIndex <= lastIndex ? activeIndex : lastIndex;
  // ---------------
  // Rendering
  // ---------------

  const renderChildren = () => {
    return kids.map((child, index) => {
      const childElement = child as React.ReactElement;
      return React.cloneElement(childElement, {
        UNSAFE_style: {
          ...childElement.props?.UNSAFE_style,
          ...resolveChildStyle(
            index,
            validActiveIndex,
            stepCount,
            labelWidth,
            variant,
          ),
        },
      });
    });
  };

  const measureLabelsView = (event: LayoutChangeEvent) => {
    setLabelWidth(event.nativeEvent.layout.width / stepCount);
  };

  const renderTrack = () => {
    return validActiveIndex > 0 ? (
      <View
        testID={ProgressTracker.displayName + '-completed-track'}
        style={[
          ss(variant).trackComplete,
          {width: `${(validActiveIndex * 100) / lastIndex}%`},
        ]}
      />
    ) : null;
  };

  const renderStep = () => {
    return kids.map((child, index) => (
      <View
        key={`stepContainer_${index}`}
        testID={ProgressTracker.displayName + `-step-outer-${index}`}
        style={[
          index === validActiveIndex
            ? ss(variant).stepContainerComplete
            : ss(variant).stepContainer,
          {left: `${(index * 100) / lastIndex}%`},
        ]}>
        <View
          key={`step_${index}`}
          testID={ProgressTracker.displayName + `-step-${index}`}
          style={[
            ss(variant).step,
            {
              backgroundColor:
                index <= validActiveIndex
                  ? variantsStyle[variant].completedBackgroundColor
                  : token.componentProgressTrackerItemIndicatorInnerBackgroundColor, //"#909196"
            },
          ]}
        />
      </View>
    ));
  };

  return (
    <View style={[ss(variant).container, UNSAFE_style]} {...rest}>
      <View
        style={ss(variant).trackContainer}
        testID={ProgressTracker.displayName}>
        <View
          accessibilityRole={a11yRole('progressbar')}
          testID={ProgressTracker.displayName + '-default-track'}
          style={ss(variant).track}>
          {renderTrack()}
          {renderStep()}
        </View>
      </View>
      <View
        style={ss(variant).itemContainer}
        onLayout={(event) => {
          measureLabelsView(event);
        }}>
        {renderChildren()}
      </View>
    </View>
  );
};

export const resolveChildStyle = (
  _index: number,
  _active: number,
  _stepCount: number,
  _labelWidth: number,
  _variant: ProgressTrackerVariant,
) => {
  const style = ss(_variant, _index === _active);
  const avg = Math.trunc(_stepCount / 2);
  return {
    ...(_index === 0 && style.labelFirst),
    ...(_index === _stepCount - 1 && style.labelLast),
    ...style.label,
    width: _labelWidth,
    marginLeft: measureMarginLeft(_index, _stepCount, avg),
  };
};

export const measureMarginLeft = (
  _index: number,
  _stepCount: number,
  _avg: number,
) => {
  return _index !== 0 && _index !== _stepCount - 1
    ? _avg <= _index
      ? 10 * _index
      : _index
    : 0;
};
// ---------------
// Styles
// ---------------

const ss = (_variant: ProgressTrackerVariant, isActive = false) => {
  const stepSize = token.componentProgressTrackerItemIndicatorWidth / 2;
  const stepRadius = stepSize / 2;
  const outerSize = token.componentProgressTrackerItemIndicatorWidth;
  const outerRadius = outerSize / 2;

  return StyleSheet.create({
    container: {
      padding: 10,
    },
    trackContainer: {
      flexDirection: 'row',
      height: token.componentProgressTrackerTrackContainerHeight, //16
      width: token.componentProgressTrackerTrackContainerWidth, //"100%"
      paddingHorizontal:
        token.componentProgressTrackerTrackContainerPaddingHorizontal, //6
      paddingVertical:
        token.componentProgressTrackerTrackContainerPaddingVertical, //0
      justifyContent:
        token.componentProgressTrackerTrackContainerAlignHorizontal as Extract<
          // @cory incorrect TS type here
          FlexStyle,
          'justifyContent'
        >, //"center"
      alignItems:
        token.componentProgressTrackerTrackContainerAlignVertical as Extract<
          // @cory incorrect TS type here
          FlexStyle,
          'alignItems'
        >, //"center"
    },
    track: {
      width: token.componentProgressTrackerTrackWidth, //"100%"
      height: token.componentProgressTrackerTrackHeight, //2
      backgroundColor: token.componentProgressTrackerTrackBackgroundColor, //"#909196"
    },
    trackComplete: {
      width: token.componentProgressTrackerTrackWidth, //"100%"
      height: token.componentProgressTrackerTrackHeight, //2
      backgroundColor: variantsStyle[_variant].backgroundColor,
    },
    stepContainer: {
      position: 'absolute',
      top: -3,
      marginLeft: -3,
      height: stepSize,
      width: stepSize,
      backgroundColor:
        token.componentProgressTrackerItemIndicatorInnerBackgroundColor, //"#909196"
      borderRadius: stepRadius,
    },
    stepContainerComplete: {
      position: 'absolute',
      top: -7,
      marginLeft: -7,
      height: outerSize,
      width: outerSize,
      backgroundColor:
        token.componentProgressTrackerItemIndicatorOuterBackgroundColor, // "#fff"
      borderWidth: token.componentProgressTrackerItemIndicatorOuterBorderWidth, //2
      borderColor: variantsStyle[_variant].borderColor,
      padding: 2,
      borderRadius: outerRadius,
    },
    step: {
      height: stepSize,
      width: stepSize,
      borderRadius: stepRadius,
    },
    labelFirst: {
      marginLeft:
        token.componentProgressTrackerItemTextLabelStateIsFirstPaddingStart, //0
      textAlign:
        token.componentProgressTrackerItemTextLabelStateIsFirstTextAlign, //"left"
    } as TextStyle,
    labelLast: {
      paddingRight:
        token.componentProgressTrackerItemTextLabelStateIsLastPaddingEnd, //0
      textAlign:
        token.componentProgressTrackerItemTextLabelStateIsLastTextAlign, //"right",
    } as TextStyle,
    label: {
      color: isActive
        ? token.componentProgressTrackerItemTextLabelStateIsCurrentTextColor //#2e2f32
        : token.componentProgressTrackerItemTextLabelTextColor, //"#74767c"
    } as TextStyle,
    itemContainer: {
      flexDirection: 'row',
    },
  });
};
ProgressTracker.displayName = 'ProgressTracker';
export {ProgressTracker};
