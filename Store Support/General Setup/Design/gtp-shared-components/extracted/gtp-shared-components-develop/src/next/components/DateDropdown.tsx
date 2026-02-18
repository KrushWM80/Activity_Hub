import * as React from 'react';
import {Pressable, StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import {convertDateToString} from '../utils';

import {_LegacyDatePicker} from './_LegacyDatePicker';
import {TextField, TextFieldProps} from './TextField';

// ---------------
// Props
// ---------------
export type DateDropdownState = {
  expanded: boolean;
  value?: Date;
};
type omitProps =
  | 'trailing'
  | 'onChangeText'
  | 'onBlur'
  | 'value'
  | 'leading'
  | 'editable'
  | 'onFocus'
  | 'textInputProps'
  | 'readOnly'
  | 'type';
export type DateDropdownProps = Omit<TextFieldProps, omitProps> & {
  /**
   * The selected date.
   */
  value?: Date;
  /**
   * The minimum date.
   */
  minimumDate?: Date;
  /**
   * The maximum date.
   */
  maximumDate?: Date;
  /**
   * The date display format.  Formatting documentation available at https://momentjs.com/docs/#/displaying/format/
   * @default 'MM / DD / YYYY'
   */
  dateFormat?: string;
  /**
   * This Dropdown's select handler.
   */
  onSelect: (value?: Date) => void;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * @deprecated use <strong>UNSAFE_style</strong> instead
   * It has no effect
   */
  style?: StyleProp<ViewStyle>;
  /**
   * whether the component is disabled or not
   * @default false
   */
  disabled?: boolean;
};

/**
 * The Date Dropdown gives users the ability to make a single date selection from a number of options.
 *
 * ## Usage
 * ```js
 * import {DateDropdown} from '@walmart/gtp-shared-components`;
 *
 * const [date, setDate] = React.useState<Date | undefined>(undefined);

 * <DateDropdown
 *   label={'Date'}
 *   value={date}
 *   helperText="Select one of these dates!"
 *   onSelect={(dt) => {
 *     if (dt) {
 *       setDate(dt);
 *     }
 *   }}
 * />
 * ```
 */
const DateDropdown: React.FC<DateDropdownProps> = (props) => {
  const {
    value,
    minimumDate,
    maximumDate,
    dateFormat,
    onSelect,
    UNSAFE_style,
    disabled = false,
    ...rest
  } = props;
  const [expanded, setExpanded] = React.useState(false);
  // ---------------
  // Rendering
  // ---------------

  return (
    <Pressable
      disabled={disabled}
      testID={DateDropdown.displayName}
      onPress={() => {
        setExpanded(!expanded);
      }}>
      <View pointerEvents="none" style={ss.container}>
        <TextField
          testID={`${DateDropdown.displayName}-Value`}
          editable={false}
          UNSAFE_style={UNSAFE_style}
          placeholder={rest.label as string}
          leading={<Icons.CalendarIcon />}
          trailing={expanded ? <Icons.CaretUpIcon /> : <Icons.CaretDownIcon />}
          value={convertDateToString(value, dateFormat)}
          {...rest}
        />
      </View>
      <_LegacyDatePicker
        {...{value, minimumDate, maximumDate}}
        visible={expanded}
        onSelect={(selectedDate?: Date) => {
          setExpanded(false);
          onSelect(selectedDate);
        }}
        onCancel={() => {
          setExpanded(false);
        }}
      />
    </Pressable>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
});

DateDropdown.displayName = 'DateDropdown';
export {DateDropdown};
