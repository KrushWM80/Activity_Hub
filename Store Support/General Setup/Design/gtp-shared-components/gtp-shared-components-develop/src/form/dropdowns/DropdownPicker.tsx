import * as React from 'react';
import {
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import {Platform} from 'react-native';

import {PickerIOS} from '@react-native-picker/picker';
import {Icons} from '@walmart/gtp-shared-icons';

import Overlay from '../../layout/overlay';
import {colors} from '../../next/utils';
import RadioItemGroup, {
  RadioItemGroupItemProps,
} from '../toggleable/radio-item-group';

type Option = string | number;
type PickerState = {
  value: Option;
  selectedId: string | undefined;
};

export type PickerSize = number | 'small' | 'medium' | 'large';

export type PickerProps = {
  values: Array<Option>;
  value?: Option;
  onSelect: (value?: Option) => void;
  onChange?: (value: Option) => void;
  onCancel: () => void;
  visible: boolean;
  size?: PickerSize;
};

/**
 * @internal
 */
class DropdownPicker extends React.Component<PickerProps, PickerState> {
  static getDerivedStateFromProps = (
    props: PickerProps,
    state: PickerState,
  ) => ({
    value: props.visible
      ? state.value ?? props.value ?? props.values[0]
      : props.value ?? props.values[0],
  });

  state: PickerState = {
    value: this.props.value ?? this.props.values[0],
    selectedId: this.props.value?.toString() ?? undefined,
  };

  private handleClose = () => {
    this.props.onSelect(this.state.value);
  };
  private handleChange = (
    value: Option,
    close?: boolean,
    selectedId?: string,
  ) => {
    this.setState({value, selectedId}, () => {
      this.props.onChange?.(value);
      if (close) {
        this.props.onSelect(this.state.value);
      }
    });
  };
  private selectNext = () => {
    const {values} = this.props;
    const index = values.findIndex((v) => v === this.state.value);
    this.setState({value: values[Math.min(index + 1, values.length - 1)]});
  };
  private selectPrevious = () => {
    const {values} = this.props;
    const index = values.findIndex((v) => v === this.state.value);
    this.setState({value: values[Math.max(index - 1, 0)]});
  };

  private getSize = () => {
    const {size} = this.props;
    if (!size) {
      return undefined;
    }
    if (typeof size === 'number') {
      return size;
    }
    const sizes = {
      small: 400,
      medium: 600,
      large: 800,
    };
    return sizes[size];
  };

  private valuesObjectsList = (inArr: Array<Option>) => {
    return inArr.map((item, idx) => {
      return {
        label: item.toString(),
        id: idx.toString(),
      } as RadioItemGroupItemProps;
    });
  };

  private getValueById = (
    objList: Array<RadioItemGroupItemProps>,
    id: string,
  ) => {
    const obj = objList.filter(
      (item) => item.id === id,
    )[0] as RadioItemGroupItemProps;
    return obj.label;
  };

  render() {
    const {values, onCancel} = this.props;

    const valuesObjList = this.valuesObjectsList(values);
    return Platform.OS === 'android' ? (
      <Overlay
        darken
        isModal
        onRequestClose={onCancel}
        visible={this.props.visible}>
        <View style={styles.container} pointerEvents="box-none">
          <View
            style={[styles.actionBar, {maxWidth: this.getSize()}]}
            accessibilityRole="radiogroup">
            <ScrollView
              bounces={false}
              scrollsToTop={false}
              style={styles.scroll}
              contentContainerStyle={styles.content}>
              <RadioItemGroup
                selectedId={this.state.selectedId}
                items={valuesObjList}
                onSelect={(id: string) =>
                  this.handleChange(
                    this.getValueById(valuesObjList, id),
                    true,
                    id,
                  )
                }
              />
            </ScrollView>
          </View>
        </View>
      </Overlay>
    ) : (
      <Overlay
        darken
        isModal
        onRequestClose={onCancel}
        visible={this.props.visible}>
        <View style={styles.container} pointerEvents="auto">
          <View style={styles.actionBar}>
            <TouchableOpacity
              activeOpacity={0.5}
              style={styles.action}
              onPress={this.selectPrevious}>
              <Icons.ChevronLeftIcon
                UNSAFE_style={styles.actionIcon}
                size={24}
              />
            </TouchableOpacity>
            <TouchableOpacity
              activeOpacity={0.5}
              style={styles.action}
              onPress={this.selectNext}>
              <Icons.ChevronRightIcon
                UNSAFE_style={styles.actionIcon}
                size={24}
              />
            </TouchableOpacity>
            <View style={styles.spacer} />
            <TouchableOpacity
              activeOpacity={0.5}
              style={styles.action}
              onPress={this.handleClose}>
              <Text style={styles.actionText}>Done</Text>
            </TouchableOpacity>
          </View>
          <PickerIOS
            selectedValue={this.state.value}
            onValueChange={(value) => this.handleChange(value, false)}>
            {values.map((value) => (
              <PickerIOS.Item
                key={value}
                label={value.toString()}
                value={value}
              />
            ))}
          </PickerIOS>
        </View>
      </Overlay>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      android: {
        flex: 1,
        backgroundColor: 'transparent',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'row',
      },
      ios: {
        backgroundColor: colors.white,
        marginBottom: -100,
        paddingBottom: 100,
      },
    }),
  },
  actionBar: {
    ...Platform.select({
      android: {
        flexGrow: 1,
        marginHorizontal: 50,
        marginVertical: 100,
        backgroundColor: colors.white,
        paddingVertical: 10,
        borderRadius: 2,
        elevation: 10,
      },
      ios: {
        paddingHorizontal: 16,
        borderColor: '#e1e0e0',
        borderWidth: 0,
        borderTopWidth: 1,
        borderBottomWidth: 1,
        borderStyle: 'solid',
        backgroundColor: '#fafaf8',
        alignItems: 'center',
        flexDirection: 'row',
      },
    }),
  },
  content: {
    flex: 0,
  },
  scroll: {
    flexGrow: 0,
  },
  action: {
    paddingVertical: 9,
    marginRight: 8,
  },
  actionIcon: {
    tintColor: '#007aff',
  },
  actionText: {
    fontSize: 15,
    lineHeight: 24,
    color: '#007aff',
    alignSelf: 'flex-end',
  },
  spacer: {
    flex: 1,
  },
});

export {DropdownPicker};
