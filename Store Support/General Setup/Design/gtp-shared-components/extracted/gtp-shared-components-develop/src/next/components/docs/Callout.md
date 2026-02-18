### Callouts with all position variants
```js
import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {DirectionView} from '../../../../example/src/components';

import {
  Callout,
  Checkbox,
  Link,
  useSimpleReducer,
} from '@walmart/gtp-shared-components';

const [state, setState] = useSimpleReducer({
  isCalloutOpen1: false,
  isCalloutOpen2: false,
  isCalloutOpen3: false,
  isCalloutOpen4: false,
  isCalloutOpen5: false,
  isCalloutOpen6: false,
  isCalloutOpen7: false,
  isCalloutOpen8: false,
});

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
    <Callout
      content={'Example Callout content.'}
      isOpen={state.isCalloutOpen1}
      onClose={() =>
        setState('isCalloutOpen1', !(state.isCalloutOpen1))
      }
      position="bottomRight">
      <Link
        onPress={() =>
          setState('isCalloutOpen1', !(state.isCalloutOpen1))
        }>
        Bottom{'\n'}Right
      </Link>
    </Callout>
    <Callout
      content={
        <View style={{width: 300, paddingHorizontal: 16}}>
          <Text style={{color: 'white'}}>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed
            do eiusmod tempor incididunt ut labore et dolore magna aliqua
          </Text>
        </View>
      }
      isOpen={state.isCalloutOpen2}
      onClose={() =>
        setState('isCalloutOpen2', !(state.isCalloutOpen2))
      }
      position="bottomCenter">
      <Link
        onPress={() =>
          setState('isCalloutOpen2', !(state.isCalloutOpen2))
        }>
        Bottom{'\n'}Center
      </Link>
    </Callout>
    <Callout
      content={'Example Callout content.'}
      isOpen={state.isCalloutOpen3}
      onClose={() =>
        setState('isCalloutOpen3', !(state.isCalloutOpen3))
      }
      position="bottomLeft">
      <Link
        onPress={() =>
          setState('isCalloutOpen3', !(state.isCalloutOpen3))
        }>
        Bottom{'\n'}Left
      </Link>
    </Callout>
  </View>
  <View style={styles.row}>
    <Callout
      content={'Example Callout content.'}
      isOpen={state.isCalloutOpen4}
      onClose={() =>
        setState('isCalloutOpen4', !(state.isCalloutOpen4))
      }
      position="right">
      <Link
        onPress={() =>
          setState('isCalloutOpen4', !(state.isCalloutOpen4))
        }>
        Right
      </Link>
    </Callout>
    <Callout
      content={'Example Callout content.'}
      isOpen={state.isCalloutOpen5}
      onClose={() =>
        setState('isCalloutOpen5', !(state.isCalloutOpen5))
      }
      position="left">
      <Link
        onPress={() =>
          setState('isCalloutOpen5', !(state.isCalloutOpen5))
        }>
        Left
      </Link>
    </Callout>
  </View>
  <View style={styles.row}>
    <Callout
      content={'Example Callout content.'}
      isOpen={state.isCalloutOpen6}
      onClose={() =>
        setState('isCalloutOpen6', !(state.isCalloutOpen6))
      }
      position="topRight">
      <Link
        onPress={() =>
          setState('isCalloutOpen6', !(state.isCalloutOpen6))
        }>
        Top{'\n'}Right
      </Link>
    </Callout>
    <Callout
      content={'Example Callout content.'}
      isOpen={state.isCalloutOpen7}
      onClose={() =>
        setState('isCalloutOpen7', !(state.isCalloutOpen7))
      }
      position="topCenter">
      <Link
        onPress={() =>
          setState('isCalloutOpen7', !(state.isCalloutOpen7))
        }>
        Top{'\n'}Center
      </Link>
    </Callout>
    <Callout
      content={'Example Callout content.'}
      isOpen={state.isCalloutOpen8}
      onClose={() =>
        setState('isCalloutOpen8', !(state.isCalloutOpen8))
      }
      position="topLeft">
      <Link
        onPress={() =>
          setState('isCalloutOpen8', !(state.isCalloutOpen8))
        }>
        Top{'\n'}Left
      </Link>
    </Callout>
  </View>
</>
```
