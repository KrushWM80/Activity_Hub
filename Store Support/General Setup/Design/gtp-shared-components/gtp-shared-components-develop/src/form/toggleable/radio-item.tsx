import * as React from 'react';
import {
  StyleSheet,
  TextStyle,
  TouchableOpacity,
  View,
  ViewStyle,
} from 'react-native';

import {Body} from '../../next/components/Body';
import {colors} from '../../next/utils';
import {getFont} from '../../theme/font';

import Radio, {RadioExternalProps} from './radio';

export type RadioItemProps = RadioExternalProps & {
  label: string;
};

type RadioItemState = 'Default' | 'Checked' | 'Disabled' | 'CheckedDisabled';

/**
 * @deprecated use Radio instead
 */
const RadioItem: React.FC<RadioItemProps> = ({
  accessible = true,
  accessibilityElementsHidden = true,
  accessibilityRole = 'radio',
  disabled,
  label,
  value,
  style,
  accessibilityLabel,
  testID,
  hitSlop,
  onChange,
  ...rest
}: RadioItemProps) => {
  const [state, setState] = React.useState<RadioItemState>('Default');
  const [containerStyle, setContainerStyle] = React.useState<
    ViewStyle | Array<ViewStyle>
  >(styles.containerDefault);
  const [labelStyle, setLabelStyle] = React.useState<
    TextStyle | Array<TextStyle>
  >(styles.labelDefault);

  const setValue = (localValue: boolean) => {
    onChange?.(localValue);
  };

  const resolveCurrentState = React.useCallback(
    ({value: localValue, disabled: localDisabled}: RadioExternalProps) => {
      if (localValue && localDisabled) {
        setState('CheckedDisabled');
      } else if (localValue) {
        setState('Checked');
      } else if (localDisabled) {
        setState('Disabled');
      } else {
        setState('Default');
      }
    },
    [],
  );

  const resolveStyles = React.useCallback((curState: RadioItemState) => {
    setContainerStyle([
      styles.containerDefault,
      styles[`container${curState}`],
    ]);
    setLabelStyle([styles.labelDefault, styles[`label${curState}`]]);
  }, []);

  React.useEffect(() => {
    resolveCurrentState({value, disabled});
  }, [resolveCurrentState, value, disabled]);

  React.useEffect(() => {
    resolveStyles(state);
  }, [resolveStyles, state]);

  return (
    <TouchableOpacity
      activeOpacity={1}
      {...{
        accessibilityLabel,
        accessibilityRole,
        accessible,
        hitSlop,
        testID,
      }}
      accessibilityState={{selected: value, disabled}}
      onPress={() => setValue(!value)}
      disabled={disabled}
      style={StyleSheet.flatten(style)}>
      <View
        style={containerStyle}
        accessibilityElementsHidden={accessibilityElementsHidden}>
        <Radio
          onChange={setValue}
          disabled={disabled}
          style={styles.radio}
          {...rest}
          value={value}
        />
        <Body UNSAFE_style={labelStyle}>{label}</Body>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  containerDefault: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  containerChecked: {
    backgroundColor: colors.gray['5'],
  },
  containerDisabled: {
    borderColor: colors.gray['50'],
  },
  containerCheckedDisabled: {
    borderColor: colors.gray['50'],
    backgroundColor: colors.gray['5'],
  },
  labelDefault: {
    color: colors.gray['140'],
    flexShrink: 1,
  },
  labelChecked: {
    ...getFont('bold'),
  } as TextStyle,
  labelDisabled: {
    color: colors.gray['50'],
    fontSize: 14,
    lineHeight: 20,
  },
  labelCheckedDisabled: {
    color: colors.gray['50'],
    fontSize: 14,
    lineHeight: 20,
  },
  radio: {
    marginRight: 12,
  },
});

RadioItem.displayName = 'RadioItem';
export default RadioItem;
