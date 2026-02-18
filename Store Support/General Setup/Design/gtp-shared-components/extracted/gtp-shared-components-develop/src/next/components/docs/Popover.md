### Popovers with all position variants
```js
import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {DirectionView} from '../../../../example/src/components';

import {
  Checkbox,
  Link,
  Popover,
  useSimpleReducer,
} from '@walmart/gtp-shared-components';

const [state, setState] = useSimpleReducer({
  isPopoverOpen1: false,
  isPopoverOpen2: false,
  isPopoverOpen3: false,
  isPopoverOpen4: false,
  isPopoverOpen5: false,
  isPopoverOpen6: false,
  isPopoverOpen7: false,
  isPopoverOpen8: false,
});

const [hasNubbin, setHasNubbin] = React.useState(true);

const styles = StyleSheet.create({
  row: {
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
});

const content = () => {
  return (
    <View style={{width: 200}}>
      <Checkbox label="I must contain at least one focusable element." />
    </View>
  );
};

<>
  <View style={styles.row}>
    <Popover
      content={content()}
      isOpen={state.isPopoverOpen1}
      onClose={() =>
        setState('isPopoverOpen1', !(state.isPopoverOpen1))
      }
      hasNubbin={hasNubbin}
      position="bottomRight">
      <Link
        onPress={() =>
          setState('isPopoverOpen1', !(state.isPopoverOpen1))
        }>
        Bottom{'\n'}Right
      </Link>
    </Popover>
    <Popover
      content={
        <View style={{width: 300}}>
          <Checkbox label="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua" />
        </View>
      }
      isOpen={state.isPopoverOpen2}
      onClose={() =>
        setState('isPopoverOpen2', !(state.isPopoverOpen2))
      }
      hasNubbin={hasNubbin}
      position="bottomCenter">
      <Link
        onPress={() =>
          setState('isPopoverOpen2', !(state.isPopoverOpen2))
        }>
        Bottom{'\n'}Center
      </Link>
    </Popover>
    <Popover
      content={content()}
      isOpen={state.isPopoverOpen3}
      onClose={() =>
        setState('isPopoverOpen3', !(state.isPopoverOpen3))
      }
      hasNubbin={hasNubbin}
      position="bottomLeft">
      <Link
        onPress={() =>
          setState('isPopoverOpen3', !(state.isPopoverOpen3))
        }>
        Bottom{'\n'}Left
      </Link>
    </Popover>
  </View>
  <View style={styles.row}>
    <Popover
      content={content()}
      isOpen={state.isPopoverOpen4}
      onClose={() =>
        setState('isPopoverOpen4', !(state.isPopoverOpen4))
      }
      hasNubbin={hasNubbin}
      position="right">
      <Link
        onPress={() =>
          setState('isPopoverOpen4', !(state.isPopoverOpen4))
        }>
        Right
      </Link>
    </Popover>
    <Popover
      content={content()}
      isOpen={state.isPopoverOpen5}
      onClose={() =>
        setState('isPopoverOpen5', !(state.isPopoverOpen5))
      }
      hasNubbin={hasNubbin}
      position="left">
      <Link
        onPress={() =>
          setState('isPopoverOpen5', !(state.isPopoverOpen5))
        }>
        Left
      </Link>
    </Popover>
  </View>
  <View style={styles.row}>
    <Popover
      content={content()}
      isOpen={state.isPopoverOpen6}
      onClose={() =>
        setState('isPopoverOpen6', !(state.isPopoverOpen6))
      }
      hasNubbin={hasNubbin}
      position="topRight">
      <Link
        onPress={() =>
          setState('isPopoverOpen6', !(state.isPopoverOpen6))
        }>
        Top{'\n'}Right
      </Link>
    </Popover>
    <Popover
      content={content()}
      isOpen={state.isPopoverOpen7}
      onClose={() =>
        setState('isPopoverOpen7', !(state.isPopoverOpen7))
      }
      hasNubbin={hasNubbin}
      position="topCenter">
      <Link
        onPress={() =>
          setState('isPopoverOpen7', !(state.isPopoverOpen7))
        }>
        Top{'\n'}Center
      </Link>
    </Popover>
    <Popover
      content={content()}
      isOpen={state.isPopoverOpen8}
      onClose={() =>
        setState('isPopoverOpen8', !(state.isPopoverOpen8))
      }
      hasNubbin={hasNubbin}
      position="topLeft">
      <Link
        onPress={() =>
          setState('isPopoverOpen8', !(state.isPopoverOpen8))
        }>
        Top{'\n'}Left
      </Link>
    </Popover>
  </View>
  <Checkbox
    label="Show Nubbin"
    checked={hasNubbin}
    onPress={() => setHasNubbin(!hasNubbin)}
    UNSAFE_style={{marginTop: 10}}
  />
</>
```
