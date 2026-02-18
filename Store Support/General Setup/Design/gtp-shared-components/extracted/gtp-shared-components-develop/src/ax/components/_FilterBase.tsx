import * as React from 'react';
import {
  GestureResponderEvent,
  Pressable,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  ViewStyle,
} from 'react-native';

import {
  _LeadingTrailing as _Leading,
  _LeadingTrailing as _Trailing,
} from '../../next/components/_LeadingTrailing';
import type {CommonPressableProps} from '../../next/types/ComponentTypes';
import {colors} from '../../next/utils';
import {getFont} from '../../theme/font';

// TODO: Add large when LD specs are finalized
export type FilterSize = 'small';
// export type FilterSize = 'small' | 'large';

export type FilterBaseProps = CommonPressableProps & {
  // size?: FilterSize;
  /**
   * The leading content for the filter.
   * (typically an icon)
   */
  leading?: React.ReactNode;
  /**
   * The trailing content for the filter.
   * (typically an icon)
   */
  trailing?: React.ReactNode;
  /**
   * The text content for the filter.
   */
  children?: React.ReactNode;
  /**
   * If the filter settings trigger is disabled.
   * @default false
   */
  disabled?: boolean;
  /**
   * If the filter select trigger is applied.
   * @default false
   */
  applied?: boolean;
  /**
   * The function to call when the filter is pressed.
   */
  onPress?: (event: GestureResponderEvent) => void;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * If provided, the `style` to override the default pressed style.
   */
  containerPressedStyle?: StyleProp<ViewStyle>;
  /**
   * If provided, the `style` to override the default disabled style.
   */
  containerDisabledStyle?: StyleProp<ViewStyle>;
};

/**
 * @internal
 */
const _FilterBase: React.FC<FilterBaseProps> = (props) => {
  const {
    // size = 'small',
    leading,
    trailing,
    applied = false,
    disabled = false,
    onPress,
    children,
    UNSAFE_style,
    containerPressedStyle,
    containerDisabledStyle,
    ...rest
  } = props;

  const hasContent =
    typeof children !== 'boolean' &&
    children !== null &&
    typeof children !== 'undefined';

  const ss = styles(applied, disabled);

  const renderLeading = (node: React.ReactNode) => {
    if (node) {
      return (
        <_Leading
          node={node}
          iconProps={{
            color: disabled ? '#BABBBE' : undefined,
            UNSAFE_style: {marginRight: hasContent ? 8 : 0},
          }}
        />
      );
    } else {
      return null;
    }
  };

  const renderTrailing = (node: React.ReactNode) => {
    if (node) {
      return (
        <_Trailing
          node={node}
          iconProps={{
            color: disabled ? '#BABBBE' : undefined,
            UNSAFE_style: {marginLeft: 8},
          }}
        />
      );
    } else {
      return null;
    }
  };

  const renderTextLabel = () => {
    return <Text style={ss.textStyle}>{children}</Text>;
  };

  return (
    <Pressable
      testID={_FilterBase.displayName}
      accessible={true}
      accessibilityRole="button"
      accessibilityState={{disabled}}
      hitSlop={{top: 8, bottom: 8}}
      disabled={disabled}
      style={({pressed}) => {
        return pressed
          ? [ss.container, ss.containerPressed, containerPressedStyle]
          : [
              ss.container,
              UNSAFE_style,
              disabled ? containerDisabledStyle : null,
            ];
      }}
      onPress={onPress}
      {...rest}>
      {renderLeading(leading)}
      {renderTextLabel()}
      {renderTrailing(trailing)}
    </Pressable>
  );
};

const styles = (applied: boolean, disabled: boolean) => {
  return StyleSheet.create({
    container: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      borderRadius: 10000,
      borderWidth: applied ? 2 : 1,
      borderColor: disabled
        ? colors.gray['50'] // '#BABBBE'
        : applied
        ? colors.blue['100'] // #0071DC'
        : colors.gray['80'], // '#909196'
      backgroundColor: disabled
        ? colors.white // '#FFFFFF'
        : applied
        ? colors.blue['5'] // #F2F8FD'
        : colors.white, // '#FFFFFF'
      height: 32,
      paddingHorizontal: 8,
      marginVertical: 4,
    } as ViewStyle,
    containerPressed: {
      borderWidth: 2,
      borderColor: applied
        ? colors.blue['160'] // '#002D58'
        : colors.gray['160'], // '#2E2F32'
      backgroundColor: applied
        ? colors.blue['20'] // '#CCE3F8'
        : colors.white, // '#FFFFFF'
    },
    textStyle: {
      ...getFont(),
      fontSize: 14,
      color: disabled
        ? colors.gray['50'] // '#BABBBE'
        : colors.gray['160'], // '#2E2F32'
    } as TextStyle,
  });
};

_FilterBase.displayName = '_FilterBase';
export {_FilterBase};
