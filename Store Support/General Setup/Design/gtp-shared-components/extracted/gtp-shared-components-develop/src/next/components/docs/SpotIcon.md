### Spot Icon

```js
import {StyleSheet} from 'react-native';
import {SpotIcon,Icons} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;
const styles = StyleSheet.create({
  firstContainer: { flexDirection: 'row', justifyContent: 'space-around'},
  secondContainer: {
    flexDirection: 'row',
    marginTop: 10,
    justifyContent: 'space-around',
  },
});

<>
  <View style={styles.firstContainer}>
    <SpotIcon>
      <Icons.CheckIcon />
    </SpotIcon>
    <SpotIcon color="white">
      <Icons.CheckIcon />
    </SpotIcon>
  </View>
  <View style={styles.secondContainer}>
    <SpotIcon size="large">
      <Icons.CheckIcon />
    </SpotIcon>
    <SpotIcon color="white" size="large">
      <Icons.CheckIcon />
    </SpotIcon>
  </View>
</>
```