import * as React from 'react';
import {StyleSheet} from 'react-native';

import {Checkbox, Radio} from '@walmart/gtp-shared-components';

const InteractiveRadios = () => {
  const list = ['Lions', 'Tigers', 'Or Bears', 'Oh My!'];
  const [selected, setSelected] = React.useState('');
  const [disabled, setDisabled] = React.useState(false);

  const renderList = list.map((item, index) => (
    <Radio
      key={index}
      label={item}
      checked={item === selected}
      disabled={disabled}
      onPress={() => setSelected(item)}
    />
  ));

  return (
    <>
      {renderList}
      <Checkbox
        label="Disable All Above"
        checked={disabled}
        onPress={() => setDisabled(!disabled)}
        UNSAFE_style={styles.checkbox}
      />
    </>
  );
};

export {InteractiveRadios};

const styles = StyleSheet.create({
  checkbox: {
    paddingTop: 5,
  },
});
