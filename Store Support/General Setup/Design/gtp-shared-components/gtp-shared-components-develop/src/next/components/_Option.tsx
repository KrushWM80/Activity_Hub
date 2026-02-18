import * as React from 'react';
import {Pressable, StyleSheet, Text, TextStyle, View} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Select';
import {Icons} from '@walmart/gtp-shared-icons';

import {getFont, Weights} from '../../theme/font';
import {CommonPressableProps} from '../types/ComponentTypes';

// ---------------
// Props
// ---------------
export type OptionSize = 'large' | 'small';

export type OptionProps = CommonPressableProps & {
  /**
   * The size for the option.
   *
   * @default "large"
   */
  size?: OptionSize;
  /**
   * The text of the option
   */
  text: string;
  /**
   * The index of the option.
   * @default 0
   */
  index?: number;
  /**
   * Whether this option is selected
   * @default false
   */
  isSelected?: boolean;
  /**
   * The callback fired when the option is pressed.
   * @default () => {}
   */
  onPress?: (index: number, text: string) => void;
  /**
   * Whether the option is disabled.
   *
   * @default false
   */
  disabled?: boolean;
};

/**
 * @internal
 */
const _Option: React.FC<OptionProps> = (props) => {
  const {
    text,
    index = 0,
    isSelected = false,
    onPress = () => {},
    disabled = false,
    size = 'large',
  } = props;
  const [textColor, setTextColor] = React.useState<string>(
    token.componentSelectValueTextColorDefault, // "#2e2f32"
  );

  React.useLayoutEffect(() => {
    if (disabled) {
      setTextColor(token.componentSelectValueTextColorDisabled); // "#babbbe"
    } else if (isSelected) {
      setTextColor(token.componentSelectValueTextColorFocus); // "#2e2f32"
    }
  }, [disabled, isSelected]);

  const handleOnPress = () => {
    onPress?.(index, text);
  };

  // ---------------
  // Rendering
  // ---------------
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityState={{selected: isSelected, disabled}}
      testID={`${_Option.displayName}_${index}`}
      style={ss(size).button}
      disabled={disabled}
      onPress={handleOnPress}>
      <View style={ss(size).iconContainer}>
        {isSelected ? (
          <Icons.CheckIcon
            size={size === 'large' ? 'medium' : 'small'}
            color={textColor}
          />
        ) : null}
      </View>
      <Text style={[ss(size).text, {color: textColor}]}>{text}</Text>
    </Pressable>
  );
};

// ---------------
// Styles
// ---------------
const ss = (size: OptionSize) => {
  return StyleSheet.create({
    button: {
      flexDirection: 'row',
      justifyContent: 'flex-start',
      alignItems: 'center',
      backgroundColor: token.componentSelectContainerBackgroundColor, // "#fff"
      paddingVertical: 4,
    },
    text: {
      ...getFont(token.componentSelectValueFontWeight.toString() as Weights), // 400
      flex: 1,
      fontSize:
        size === 'large'
          ? token.componentSelectValueSizeLargeFontSize // 16
          : token.componentSelectValueSizeSmallFontSize, // 14
      lineHeight:
        size === 'large'
          ? token.componentSelectValueSizeLargeLineHeight // 24
          : token.componentSelectValueSizeSmallLineHeight, // 24
      marginLeft: 6,
    } as TextStyle,
    iconContainer: {
      paddingLeft: 8,
      width: size === 'large' ? 32 : 24,
    },
  });
};

_Option.displayName = '_Option';
export {_Option};
