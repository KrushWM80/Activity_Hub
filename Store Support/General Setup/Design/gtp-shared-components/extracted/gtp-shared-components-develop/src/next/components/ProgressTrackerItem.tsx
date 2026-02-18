import * as React from 'react';
import {StyleProp, StyleSheet, TextStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/ProgressTracker';

import {getFont} from '../../theme/font';
import {CommonViewProps} from '../types/ComponentTypes';

import {Body, BodyWeight} from './Body';

// ---------------
// Props
// ---------------
export type ProgressTrackerItemProps = CommonViewProps & {
  /**
   * The content for the progress tracker item.
   */
  children?: React.ReactNode;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<TextStyle>;
};

/**
 * ProgressTrackerItem are used to provide the content for the ProgressTracker component.
 *
 * ## Usage
 * ```js
 * import {ProgressTrackerItem} from '@walmart/gtp-shared-components`;
 *
 * <ProgressTrackerItem>Label</ProgressTrackerItem>
 * ```
 */
const ProgressTrackerItem: React.FC<ProgressTrackerItemProps> = (props) => {
  const {children, UNSAFE_style = {}, ...rest} = props;
  // --------------->
  // Rendering
  // ---------------
  return (
    <Body
      UNSAFE_style={[ss.label, UNSAFE_style]}
      weight={
        token.componentProgressTrackerItemTextLabelFontWeight.toString() as BodyWeight
      }
      {...rest}>
      {children}
    </Body>
  );
};

// ---------------
// Styles
// ---------------

const ss = StyleSheet.create({
  label: {
    flex: 1,
    ...getFont(),
    fontSize: token.componentProgressTrackerItemTextLabelFontSize, //12
    flexWrap: 'wrap',
    color: token.componentProgressTrackerItemTextLabelTextColor, // "#74767c"
    textAlign: token.componentProgressTrackerItemTextLabelTextAlign, //"center"
  } as TextStyle,
});

ProgressTrackerItem.displayName = 'ProgressTrackerItem';
export {ProgressTrackerItem};
