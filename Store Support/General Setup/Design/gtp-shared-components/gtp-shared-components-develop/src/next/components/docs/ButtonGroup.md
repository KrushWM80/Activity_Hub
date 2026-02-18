### ButtonGroup

```js
import {StyleSheet, Text} from 'react-native';
import {ButtonGroup, Button, colors} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 16}} />;

const ss = StyleSheet.create({
  variantInBody: {
    alignSelf: 'center',
    marginVertical: 12,
    paddingHorizontal: 12,
    marginLeft: 20,
    fontSize: 15,
    lineHeight: 20,
    color: colors.blue['90'],
    borderColor: colors.blue['90'],
    borderWidth: 0.5,
  },
});

<>
  <Spacer />
  <View>
    <ButtonGroup>
      <Button
        variant="secondary"
        onPress={() =>
          displayPopupAlert('Action', 'Secondary button pressed')
        }>
        Secondary
      </Button>
      <Button
        variant="primary"
        onPress={() =>
          displayPopupAlert('Action', 'Primary button pressed')
        }>
        Primary
      </Button>
    </ButtonGroup>
  </View>
  <Spacer />
  <View>
    <ButtonGroup UNSAFE_style={{marginVertical: 16}}>
      <Button
        variant="tertiary"
        onPress={() =>
          displayPopupAlert('Action', 'Button "One" pressed')
        }>
        One
      </Button>
      <Button
        variant="secondary"
        onPress={() =>
          displayPopupAlert('Action', 'Button "Two" pressed')
        }>
        Two
      </Button>
      <Button
        variant="primary"
        onPress={() =>
          displayPopupAlert('Action', 'Button "Three" pressed')
        }>
        Three
      </Button>
    </ButtonGroup>
      <Text style={ss.variantInBody}>{'isFullWidth={true}'}</Text>
        <ButtonGroup isFullWidth>
          <Button
            variant="secondary"
            onPress={() =>
              displayPopupAlert('Action', 'Secondary button pressed')
            }>
            Secondary
          </Button>
          <Button
            variant="primary"
            onPress={() =>
              displayPopupAlert('Action', 'Primary button pressed')
            }>
            Primary
          </Button>
      </ButtonGroup>
  </View>
</>;
```
