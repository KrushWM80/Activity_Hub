import * as React from 'react';

import {Icons} from '@walmart/gtp-shared-icons';
import moment from 'moment';

import ThemedTextField, {
  ThemedTextFieldExternalProps,
} from '../text-fields/base/themed-textfield';

import DatePicker from './date-picker';

type DateDropdownState = {
  expanded: boolean;
  value?: Date;
};

export type DateDropdownProps = Omit<
  ThemedTextFieldExternalProps,
  | 'trailingIcon'
  | 'trailingLink'
  | 'onTrailingIconPress'
  | 'onLinkPress'
  | 'value'
  | 'leadingIcon'
  | 'editable'
  | 'onFocus'
  | 'onBlur'
  | 'onChange'
> & {
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
};

/**
 * @deprecated: DateDropdown is refactored to current coding standards and moved to the next folder
 */
export default class DateDropdown extends React.Component<
  DateDropdownProps,
  DateDropdownState
> {
  state: DateDropdownState = {
    expanded: false,
  };

  private toggleExpanded = () => {
    this.setState({expanded: !this.state.expanded});
  };

  private onSelect = (value?: Date) => {
    this.toggleExpanded();
    this.props.onSelect(value);
  };

  render() {
    const {value, minimumDate, maximumDate, dateFormat, ...props} = this.props;
    return (
      <>
        <ThemedTextField
          {...props}
          value={
            value ? moment(value).format(dateFormat ?? 'MM / DD / YYYY') : ''
          }
          editable={false}
          active={this.state.expanded}
          type="textField"
          leadingIcon={<Icons.CalendarIcon />}
          trailingIcon={
            this.state.expanded ? (
              <Icons.CaretUpIcon />
            ) : (
              <Icons.CaretDownIcon />
            )
          }
          onPress={this.toggleExpanded}
          onTrailingIconPress={this.toggleExpanded}
        />
        <DatePicker
          {...{value, minimumDate, maximumDate}}
          visible={this.state.expanded}
          onSelect={this.onSelect}
          onCancel={this.toggleExpanded}
        />
      </>
    );
  }
}
