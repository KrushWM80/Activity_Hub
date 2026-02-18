import * as React from 'react';
import {View} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import ThemedTextField, {
  ThemedTextFieldExternalProps,
} from '../text-fields/base/themed-textfield';

import {DropdownPicker, PickerSize} from './DropdownPicker';

type Option = string | number;
type DropdownState = {
  expanded: boolean;
  value?: Option;
};

export type DropdownProps = Omit<
  ThemedTextFieldExternalProps,
  | 'trailingIcon'
  | 'trailingLink'
  | 'onTrailingIconPress'
  | 'onLinkPress'
  | 'value'
  | 'editable'
  | 'onFocus'
  | 'onBlur'
  | 'onChange'
> & {
  /**
   * The list of all available values.
   */
  values: Array<Option>;
  /**
   * The selected value.
   */
  value?: Option;
  /**
   * This Dropdown's select handler.
   */
  onSelect: (value?: Option) => void;
  /**
   * Android Only: The size of the picker modal.
   */
  pickerSize?: PickerSize;
  /**
   * Button accessibility text.
   * If not provided, it defaults to this English string:
   * "Select an item from the available options"
   */
  buttonAccessibilityText?: string;
};

/**
 * @deprecated use <strong>Select</strong> instead
 */
export default class Dropdown extends React.Component<
  DropdownProps,
  DropdownState
> {
  state: DropdownState = {
    expanded: false,
  };

  private toggleExpanded = () => {
    this.setState({expanded: !this.state.expanded});
  };

  private onSelect = (value?: Option) => {
    this.props.onSelect(value);
    this.toggleExpanded();
  };

  resolveA11yLabel = (value: {toString: () => any}, label: string) => {
    const {
      buttonAccessibilityText:
        a11yText = 'Select an item from available options',
    } = this.props;
    if (value) {
      return `${label} ${value.toString()}. ${a11yText}.`;
    }
    if (label) {
      return `${label}. ${a11yText}. ${this.props.helperText}`;
    }
  };

  render() {
    const {onSelect, value, values, pickerSize, ...rest} = this.props;
    return (
      <View
        accessible
        accessibilityRole="button"
        accessibilityLabel={this.resolveA11yLabel(value ?? '', rest.label)}>
        <ThemedTextField
          {...rest}
          importantForAccessibility="no"
          helperTextImportantForA11y="no"
          value={(value ?? '').toString()}
          editable={false}
          active={this.state.expanded}
          type="textField"
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
        <DropdownPicker
          {...{value, values, size: pickerSize}}
          visible={this.state.expanded}
          onSelect={this.onSelect}
          onCancel={this.toggleExpanded}
        />
      </View>
    );
  }
}
