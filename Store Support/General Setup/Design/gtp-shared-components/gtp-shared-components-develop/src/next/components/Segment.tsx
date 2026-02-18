import * as React from 'react';
import {
  GestureResponderEvent,
  Pressable,
  PressableProps,
  StyleProp,
  StyleSheet,
  ViewStyle,
} from 'react-native';
import {TextStyle} from 'react-native';

import {getFont, Weights} from '../../theme/font';
import {a11yRole, colors} from '../utils';

import {Body} from './Body';
import {SegmentSize} from './Segmented';

type SegmentSelectionState =
  | 'default'
  | 'selected'
  | 'disabled'
  | 'selectedDisabled';

// ---------------
// Props
// ---------------

export type SegmentProps = PressableProps & {
  /**
   * The content for the Segment.
   * It is marked as optional for backwards compatibility only
   */
  children?: React.ReactNode;

  /** Size of the Segment.
   * @default small
   */
  size?: SegmentSize;

  /** onPress event handler when this Segment is clicked */
  onPress?: (event: GestureResponderEvent) => void;

  /**
   * Selected denotes whether this segment is currently selected.
   * @default false
   */
  selected?: boolean;

  /**
   * Disabled denotes whether the segment is enabled/disabled.
   * @default false
   */
  disabled?: boolean;

  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;

  /**
   * @deprecated it has no effect. Use <strong>size</strong> instead
   */
  small?: boolean;
};

export type SegmentExternalProps = SegmentProps;

/**
 * Segments are used as children of Segmented.
 *
 * ## Usage
 * ```js
 * import {Segment} from '@walmart/gtp-shared-components';
 *
 * <Segment selected={true}>First</Segment>
 * <Segment selected={false}>Second</Segment>
 * ```
 */
const Segment: React.FC<SegmentProps> = (props) => {
  const {
    selected = false,
    disabled = false,
    size = 'small',
    onPress,
    children,
    UNSAFE_style = {},
    ...rest
  } = props;

  const [segmentSelectionState, setSegmentSelectionState] =
    React.useState<SegmentSelectionState>('default');

  React.useEffect(() => {
    if (selected && disabled) {
      setSegmentSelectionState('selectedDisabled');
    } else if (selected) {
      setSegmentSelectionState('selected');
    } else if (disabled) {
      setSegmentSelectionState('disabled');
    } else {
      setSegmentSelectionState('default');
    }
  }, [disabled, selected]);

  // ---------------
  // Rendering
  // ---------------

  return (
    <Pressable
      accessibilityRole={a11yRole('radio')}
      accessibilityState={{selected, disabled}}
      testID={Segment.displayName}
      onPress={onPress}
      disabled={disabled}
      {...rest}
      style={[ss(segmentSelectionState, size).container, UNSAFE_style]}>
      <Body UNSAFE_style={[ss(segmentSelectionState, size).text]}>
        {children}
      </Body>
    </Pressable>
  );
};

// ---------------
// Styles
// ---------------

export const selectionStyles = {
  default: {
    backgroundColor: colors.gray['20'],
    textColor: colors.black,
    fontWeight: 'normal',
  },
  selected: {
    backgroundColor: colors.white,
    textColor: colors.black,
    fontWeight: 'bold',
  },
  disabled: {
    backgroundColor: colors.gray['20'],
    textColor: colors.gray['50'],
    fontWeight: 'normal',
  },
  selectedDisabled: {
    backgroundColor: colors.white,
    textColor: colors.gray['50'],
    fontWeight: 'bold',
  },
};

const ss = (
  selectionState: SegmentSelectionState,
  size: SegmentSize | undefined,
) => {
  const _backgroundColor = selectionStyles[selectionState].backgroundColor;
  const _textColor = selectionStyles[selectionState].textColor;
  const _fontWeight = selectionStyles[selectionState].fontWeight as Weights;
  const _paddingVertical = size === 'small' ? 4 : 8;

  return StyleSheet.create({
    container: {
      borderRadius: 4,
      paddingVertical: _paddingVertical,
      justifyContent: 'center',
      backgroundColor: _backgroundColor,
      alignSelf: 'stretch',
      flex: 1,
    },
    text: {
      ...getFont(_fontWeight),
      fontSize: 14,
      lineHeight: 20,
      color: _textColor,
      textAlign: 'center',
    } as TextStyle,
  });
};

Segment.displayName = 'Segment';
export {Segment};
