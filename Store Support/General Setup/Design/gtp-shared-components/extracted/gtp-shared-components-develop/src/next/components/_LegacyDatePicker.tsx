import * as React from 'react';
import {Platform, StyleSheet, Text, TouchableOpacity, View} from 'react-native';

import DateTimePicker from '@react-native-community/datetimepicker';
import {Icons} from '@walmart/gtp-shared-icons';
import moment from 'moment';

import {a11yRole, colors} from '../utils';

import {BottomSheet} from './BottomSheet';

export type _LegacyDatePickerProps = {
  value?: Date;
  minimumDate?: Date;
  maximumDate?: Date;
  onSelect: (value?: Date) => void;
  onChange?: (value: Date) => void;
  onCancel: () => void;
  visible: boolean;
};

/**
 * @internal
 */
const _LegacyDatePicker: React.FC<_LegacyDatePickerProps> = (props) => {
  const {
    value,
    minimumDate,
    maximumDate,
    onSelect,
    onChange,
    onCancel,
    visible = false,
  } = props;

  const [date, setDate] = React.useState(new Date());
  React.useEffect(() => {
    if (value) {
      setDate(value);
    }
  }, [value]);

  const handleClose = () => {
    onSelect(date);
  };
  const handleChange = (_event: any, _value?: Date) => {
    if (Platform.OS === 'android') {
      if (_value && _event.type === 'set') {
        onSelect(_value);
      } else {
        onCancel();
      }
    } else {
      if (_value) {
        setDate(_value);
        onChange?.(_value);
      }
    }
  };
  const selectNext = () => {
    setDate(moment(date).add(1, 'day').toDate());
  };
  const selectPrevious = () => {
    setDate(moment(date).add(-1, 'day').toDate());
  };

  const renderAndroidDatePicker = () => {
    return visible ? (
      <DateTimePicker
        mode="date"
        value={date}
        {...{minimumDate, maximumDate}}
        onChange={handleChange}
      />
    ) : null;
  };

  const renderIOSDatePicker = () => {
    return (
      <BottomSheet
        hideHeader
        showCloseHandle={false}
        onClose={onCancel}
        isOpen={visible}
        UNSAFE_style={ss.bottomSheetStyle}>
        <View style={ss.container} pointerEvents="auto">
          <View style={ss.actionBar}>
            <TouchableOpacity
              activeOpacity={0.5}
              style={ss.action}
              testID={`${_LegacyDatePicker.displayName}-decrease-button`}
              accessibilityRole={a11yRole('button')}
              onPress={selectPrevious}>
              <Icons.ChevronLeftIcon UNSAFE_style={ss.actionIcon} size={24} />
            </TouchableOpacity>
            <TouchableOpacity
              activeOpacity={0.5}
              testID={`${_LegacyDatePicker.displayName}-increase-button`}
              accessibilityRole={a11yRole('button')}
              style={ss.action}
              onPress={selectNext}>
              <Icons.ChevronRightIcon UNSAFE_style={ss.actionIcon} size={24} />
            </TouchableOpacity>
            <View style={ss.spacer} />
            <TouchableOpacity
              testID={`${_LegacyDatePicker.displayName}-done-button`}
              accessibilityRole={a11yRole('button')}
              activeOpacity={0.5}
              style={ss.action}
              onPress={handleClose}>
              <Text style={ss.actionText}>Done</Text>
            </TouchableOpacity>
          </View>
          <DateTimePicker
            mode="date"
            display="spinner"
            textColor={colors.black}
            value={date}
            {...{minimumDate, maximumDate}}
            onChange={handleChange}
          />
        </View>
      </BottomSheet>
    );
  };

  return Platform.OS === 'android'
    ? renderAndroidDatePicker()
    : renderIOSDatePicker();
};

const ss = StyleSheet.create({
  container: {
    backgroundColor: colors.white,
    marginBottom: -100,
    paddingBottom: 100,
  },
  actionBar: {
    paddingHorizontal: 16,
    borderColor: colors.gray['20'],
    borderWidth: 0,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderStyle: 'solid',
    backgroundColor: colors.gray['5'],
    alignItems: 'center',
    flexDirection: 'row',
  },
  action: {
    paddingVertical: 9,
    marginRight: 8,
  },
  actionIcon: {
    tintColor: colors.blue['100'],
  },
  actionText: {
    fontSize: 15,
    lineHeight: 24,
    color: colors.blue['100'],
    alignSelf: 'flex-end',
  },
  spacer: {
    flex: 1,
  },
  bottomSheetStyle: {
    paddingHorizontal: 0,
    paddingBottom: 0,
  },
});

_LegacyDatePicker.displayName = '_LegacyDatePicker';
export {_LegacyDatePicker};
