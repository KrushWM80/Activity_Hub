import * as React from 'react';
import {
  ImageStyle,
  Pressable,
  StyleProp,
  StyleSheet,
  Text,
  TextStyle,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Chip';

import {capitalize} from '../../next/utils';
import {getFont} from '../../theme/font';
import type {CommonViewProps} from '../types/ComponentTypes';
import {a11yRole} from '../utils';

import {_LeadingTrailing as _Leading} from './_LeadingTrailing';

export type ChipSize = 'small' | 'large';
type ChipInteractionState = 'Default' | 'Selected' | 'Disabled';
export type ChipId = number | string;

// ---------------
// Props
// ---------------
export type ChipProps = CommonViewProps & {
  /**
   * The id of the chip. A string or a number used
   * in a ChipGroup to identify each Chip
   */
  id: ChipId;
  /**
   * The content for the chip.
   * Typically a string label.
   */
  children: React.ReactNode;
  /**
   * Whether the chip is disabled.
   * @default false
   */
  disabled?: boolean;
  /**
   * The leading content for the chip.
   * Typically an icon.
   */
  leading?: React.ReactElement;
  /**
   * The trailing content for the chip.
   * Typically an icon
   */
  trailing?: React.ReactElement;
  /**
   * The callback fired when the chip is clicked.
   * @default () => {}
   */
  onPress?: (id: ChipId, selected: boolean) => void;
  /**
   * Whether the chip is selected.
   * @default false
   */
  selected?: boolean;
  /**
   * The size for the chip.
   * @default small
   */
  size?: ChipSize;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<TextStyle>;

  ///**** Non LD Props ****///
  /**
   * To disable the OnPress on Chip.
   * @default false
   */
  disableOnPress?: boolean;
};

/**
 * Chips allow users to make selections, filter content, or trigger actions.
 *
 * ## Usage
 * ```js
 * import {Chip} from '@walmart/gtp-shared-components`;
 *
 * <Chip
 *   id={0}
 *   selected
 *   children="Sam's Choice"
 *   onPress={(id, sel) => console.log(id, sel)}
 * />
 * ```
 */
const Chip: React.FC<ChipProps> = (props: ChipProps) => {
  const {
    id,
    children,
    size = 'small',
    selected = false,
    disabled,
    leading,
    trailing,
    onPress: propOnPress = () => {},
    UNSAFE_style,
    disableOnPress = false,
    ...rest
  } = props;

  const [interactionState, setInteractionState] =
    React.useState<ChipInteractionState>('Default');

  React.useEffect(() => {
    if (disabled) {
      setInteractionState('Disabled');
    } else if (selected) {
      setInteractionState('Selected');
    } else {
      setInteractionState('Default');
    }
  }, [disabled, selected]);

  // ---------------
  // Styles
  // ---------------
  const [containerStyle, setContainerStyle] = React.useState<
    Array<StyleProp<ViewStyle>>
  >([styles.containerDefault]);
  const [textStyle, setTextStyle] = React.useState<Array<StyleProp<TextStyle>>>(
    [styles.textDefault],
  );
  const [leadingStyle, setLeadingStyle] = React.useState<ImageStyle>();
  const [trailingStyle, setTrailingStyle] = React.useState<ImageStyle>();

  const resolveStyles = React.useCallback(() => {
    setContainerStyle([
      styles.containerDefault,
      styles[`container${interactionState}`],
      styles[`container${capitalize(size)}` as keyof typeof styles],
      UNSAFE_style ? UNSAFE_style : {},
    ]);
    setTextStyle([
      styles.textDefault,
      styles[`text${interactionState}`],
      styles[`text${capitalize(size)}` as keyof typeof styles],
    ]);
    setLeadingStyle([
      styles[`leading${interactionState}` as keyof typeof styles],
      styles[`leading${capitalize(size)}` as keyof typeof styles],
    ] as ImageStyle);
    setTrailingStyle([
      styles[`trailing${interactionState}` as keyof typeof styles],
      styles[`trailing${capitalize(size)}` as keyof typeof styles],
    ] as ImageStyle);
  }, [UNSAFE_style, interactionState, size]);

  React.useEffect(() => {
    resolveStyles();
  }, [resolveStyles]);

  // ---------------
  // Interactions
  // ---------------
  const handleOnPress = (chipId: ChipId, sel: boolean): void => {
    propOnPress(chipId, sel);
  };

  // ---------------
  // Rendering
  // ---------------
  const renderLeading = (pressed: boolean, node: React.ReactNode) => {
    return (
      <_Leading
        node={node}
        iconProps={{
          UNSAFE_style:
            pressed && !disableOnPress
              ? ([leadingStyle, styles.leadingPressed] as ImageStyle)
              : leadingStyle,
        }}
      />
    );
  };

  const renderTrailing = (pressed: boolean, node: React.ReactNode) => {
    return (
      <_Leading
        node={node}
        iconProps={{
          UNSAFE_style:
            pressed && !disableOnPress
              ? ([trailingStyle, styles.trailingPressed] as ImageStyle)
              : trailingStyle,
        }}
      />
    );
  };

  const renderText = (pressed: boolean) => {
    let tStyle = textStyle;
    if (pressed && !disableOnPress) {
      tStyle = [tStyle, styles.textPressed];
    }
    return <Text style={tStyle}>{children}</Text>;
  };

  const resolveOnPressProps = (cId: ChipId, intState: ChipInteractionState) => {
    if (intState === 'Disabled' || disableOnPress) {
      return {};
    }
    return {
      onPress: () => handleOnPress(cId, intState !== 'Selected'),
    };
  };

  return (
    <Pressable
      accessibilityRole={a11yRole('togglebutton')}
      accessibilityState={{disabled: disabled || disableOnPress, selected}}
      testID={Chip.displayName}
      disabled={disabled}
      // @ts-ignore
      unstable_pressDelay={130}
      {...resolveOnPressProps(id, interactionState)}
      {...rest}
      style={({pressed}) => {
        return pressed && !disableOnPress
          ? [containerStyle, styles.containerPressed]
          : containerStyle;
      }}>
      {({pressed}) => (
        <>
          {leading ? renderLeading(pressed, leading) : null}
          {renderText(pressed)}
          {trailing ? renderTrailing(pressed, trailing) : null}
        </>
      )}
    </Pressable>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  // ---------------
  // Container
  // ---------------
  containerDefault: {
    justifyContent: 'space-around',
    marginHorizontal: 4,
    alignItems: token.componentChipContainerAlignVertical as 'center',
    backgroundColor: token.componentChipContainerBackgroundColorDefault,
    borderRadius: token.componentChipContainerBorderRadius,
    borderWidth: token.componentChipContainerBorderWidthDefault,
    borderColor: token.componentChipContainerBorderColorDefault,
    flexDirection: 'row',
    paddingHorizontal:
      token.componentChipContainerPaddingHorizontal -
      token.componentChipContainerBorderWidthDefault,
    paddingVertical:
      token.componentChipContainerPaddingVertical -
      token.componentChipContainerBorderWidthDefault,
  },
  containerSelected: {
    backgroundColor: token.componentChipContainerStateSelectedBackgroundColor,
    borderColor: token.componentChipContainerStateSelectedBorderColor,
    borderWidth: token.componentChipContainerStateSelectedBorderWidth,
    paddingHorizontal:
      token.componentChipContainerPaddingHorizontal -
      token.componentChipContainerStateSelectedBorderWidth,
    paddingVertical:
      token.componentChipContainerPaddingVertical -
      token.componentChipContainerStateSelectedBorderWidth,
  },
  containerDisabled: {
    backgroundColor: token.componentChipContainerBackgroundColorDisabled,
    borderColor: token.componentChipContainerBorderColorDisabled,
    borderWidth: token.componentChipContainerBorderWidthDisabled,
    paddingHorizontal:
      token.componentChipContainerPaddingHorizontal -
      token.componentChipContainerBorderWidthDisabled,
    paddingVertical:
      token.componentChipContainerPaddingVertical -
      token.componentChipContainerBorderWidthDisabled,
  },
  containerPressed: {
    backgroundColor: token.componentChipContainerBackgroundColorActive,
    borderWidth: token.componentChipContainerBorderWidthActive,
    borderColor: token.componentChipContainerBackgroundColorActive,
    paddingHorizontal:
      token.componentChipContainerPaddingHorizontal -
      token.componentChipContainerBorderWidthActive,
    paddingVertical:
      token.componentChipContainerPaddingVertical +
      token.componentChipContainerStateSelectedBorderWidth,
  },
  containerSmall: {},
  containerLarge: {},
  // ---------------
  // Text
  // ---------------
  textDefault: {
    ...getFont(),
    fontSize: token.componentChipTextLabelFontSize,
    color: token.componentChipTextLabelStateSelectedTextColor,
  } as TextStyle,
  textSelected: {
    color: token.componentChipTextLabelStateSelectedTextColor,
  } as TextStyle,
  textDisabled: {
    color: token.componentChipTextLabelTextColorDisabled,
  } as TextStyle,
  textPressed: {
    color: token.componentChipTextLabelTextColorActive,
  },
  textSmall: {
    lineHeight: token.componentChipTextLabelSizeSmallLineHeight,
  },
  textLarge: {
    lineHeight: token.componentChipTextLabelSizeLargeLineHeight,
  },
  // ---------------
  // Leading
  // ---------------
  leadingDefault: {
    marginRight: token.componentChipLeadingIconMarginEnd,
  },
  leadingDisabled: {
    tintColor: token.componentChipTextLabelTextColorDisabled,
  },
  leadingSelected: {
    tintColor: token.componentChipTextLabelStateSelectedTextColor,
  },
  leadingPressed: {
    tintColor: token.componentChipTextLabelTextColorActive,
  },
  leadingSmall: {
    marginRight: token.componentChipLeadingIconMarginEnd,
  },
  leadingLarge: {
    marginRight: token.componentChipLeadingIconMarginEnd,
  },
  // ---------------
  // Trailing
  // ---------------
  trailingDefault: {
    marginLeft: token.componentChipTrailingIconMarginStart,
  },
  trailingDisabled: {
    tintColor: token.componentChipTextLabelTextColorDisabled,
  },
  trailingSelected: {
    tintColor: token.componentChipTextLabelStateSelectedTextColor,
  },
  trailingPressed: {
    tintColor: token.componentChipTextLabelTextColorActive,
  },
  trailingSmall: {
    marginLeft: token.componentChipTrailingIconMarginStart,
  },
  trailingLarge: {
    marginLeft: token.componentChipTrailingIconMarginStart,
  },
});

Chip.displayName = 'Chip';
export {Chip};
