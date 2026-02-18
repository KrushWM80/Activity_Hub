import * as React from 'react';
import {Platform, Text, TouchableOpacity, View} from 'react-native';

import DateTimePicker from '@react-native-community/datetimepicker';
import {Icons} from '@walmart/gtp-shared-icons';
import moment from 'moment';

import Overlay from '../../layout/overlay';
import {getThemeFrom, ThemeContext} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

type DatePickerState = {
  value: Date;
};

export type DatePickerProps = {
  value?: Date;
  minimumDate?: Date;
  maximumDate?: Date;
  onSelect: (value?: Date) => void;
  onChange?: (value: Date) => void;
  onCancel: () => void;
  visible: boolean;
};

/**
 * @deprecated: DatePicker is refactored to current coding standards and moved to the next folder
 */

export default class DatePicker extends React.Component<
  DatePickerProps,
  DatePickerState
> {
  static contextTypes = ThemeContext;

  static getDerivedStateFromProps = (
    props: DatePickerProps,
    state: DatePickerState,
  ) => ({
    value: props.visible
      ? state.value ?? props.value ?? new Date()
      : props.value ?? new Date(),
  });

  state: DatePickerState = {
    value: this.props.value ?? new Date(),
  };
  private handleClose = () => {
    this.props.onSelect(this.state.value);
  };
  private handleChange = (_event: any, value?: Date) => {
    if (Platform.OS === 'android') {
      if (value) {
        this.props.onSelect(value);
      } else {
        this.props.onCancel();
      }
    } else {
      if (value) {
        this.setState({value}, () => this.props.onChange?.(value));
      }
    }
  };
  private selectNext = () => {
    this.setState({value: moment(this.state.value).add(1, 'day').toDate()});
  };
  private selectPrevious = () => {
    this.setState({value: moment(this.state.value).add(-1, 'day').toDate()});
  };
  render() {
    const {minimumDate, maximumDate, onCancel} = this.props;
    const theme = getThemeFrom(this.context, defaultTheme, 'form', 'picker');
    return Platform.OS === 'android' ? (
      this.props.visible ? (
        <DateTimePicker
          mode="date"
          value={this.state.value}
          {...{minimumDate, maximumDate}}
          onChange={this.handleChange}
        />
      ) : null
    ) : (
      <Overlay darken onRequestClose={onCancel} visible={this.props.visible}>
        <View style={theme.part('static.container')} pointerEvents="auto">
          <View style={theme.part('static.actionBar')}>
            <TouchableOpacity
              activeOpacity={0.5}
              style={theme.part('static.action')}
              onPress={this.selectPrevious}>
              <Icons.ChevronLeftIcon
                UNSAFE_style={theme.part('static.actionIcon')}
                size={24}
              />
            </TouchableOpacity>
            <TouchableOpacity
              activeOpacity={0.5}
              style={theme.part('static.action')}
              onPress={this.selectNext}>
              <Icons.ChevronRightIcon
                UNSAFE_style={theme.part('static.actionIcon')}
                size={24}
              />
            </TouchableOpacity>
            <View style={theme.part('static.spacer')} />
            <TouchableOpacity
              activeOpacity={0.5}
              style={theme.part('static.action')}
              onPress={this.handleClose}>
              <Text style={theme.part('static.actionText')}>Done</Text>
            </TouchableOpacity>
          </View>
          <DateTimePicker
            mode="date"
            display="spinner"
            textColor={'#000000'}
            style={theme.part('static.picker')}
            value={this.state.value}
            {...{minimumDate, maximumDate}}
            onChange={this.handleChange}
          />
        </View>
      </Overlay>
    );
  }
}
