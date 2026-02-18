import * as React from 'react';
import {StyleSheet, View} from 'react-native';

import {Radio} from '@walmart/gtp-shared-components';

export type Category = Partial<
  | 'size'
  | 'body'
  | 'variant'
  | 'position'
  | 'keyboardType'
  | 'selectionType'
  | 'selectionInputType'
  | 'leadingType'
  | 'trailingType'
  | 'ListItemType'
  | 'flagPosition'
  | 'actionPosition'
  | 'title'
  | 'color'
  | 'origin'
  | 'fillDirection'
  | 'value'
  | 'minimumDate'
  | 'maximumDate'
  | 'dateFormat'
  | 'disabled'
>;

type RadioButtonGroupProps = {
  category: Category;
  list: Array<string>;
  disabled?: Array<string>;
  selected: string;
  onChange: (cat: any, sel: any) => void;
  orientation?: 'horizontal' | 'vertical';
};

const RadioGroup: React.FC<RadioButtonGroupProps> = props => {
  const [selected, setSelected] = React.useState({
    cat: props.category,
    sel: props.selected,
  });

  const handleOnPress = (cat: Category, sel: string) => {
    setSelected({...selected, cat, sel});
    props.onChange(cat, sel);
  };

  const containerStyle =
    props?.orientation === 'horizontal' ? ss.horizontalStyle : {};
  const itemStyle = props?.orientation === 'horizontal' ? ss.rbGroup : {};
  return (
    <View style={[ss.rbGroup, containerStyle]}>
      {props.list.map(item => {
        return (
          <Radio
            key={item}
            label={item}
            disabled={props.disabled?.includes(item)}
            UNSAFE_style={itemStyle}
            checked={item === selected.sel}
            onPress={() => handleOnPress(props.category, item)}
          />
        );
      })}
    </View>
  );
};

const ss = StyleSheet.create({
  rbGroup: {
    marginLeft: 16,
  },
  horizontalStyle: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
});

export {RadioGroup};
