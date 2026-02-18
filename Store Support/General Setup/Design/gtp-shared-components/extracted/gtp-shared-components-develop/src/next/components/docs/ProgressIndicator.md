### ProgressIndicator variant="error"

```js
import {StyleSheet} from 'react-native';
import {ProgressIndicator} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
});
<>
  <View style={styles.innerContainer}>
    <ProgressIndicator
      label={'Blocked by conveyor downtime'}
      value={25}
      valueLabel="25% loaded"
      variant="error"
    />
  </View>
</>
```

### ProgressIndicator variant="info"

```js
import {StyleSheet} from 'react-native';
import {ProgressIndicator} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;
const styles = StyleSheet.create({
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
});
<>
  <View style={styles.innerContainer}>
    <ProgressIndicator
      label={'Location'}
      value={50}
      valueLabel="50%"
      variant="info"
    />
  </View>
  <Spacer />
  <View style={styles.innerContainer}>
    <ProgressIndicator
      label={'Add $35 of items to your cart for free shipping'}
      value={75}
      valueLabel="$9 remaining"
      variant="info"
    />
  </View>
</>
```


### ProgressIndicator variant="success"

```js
import {StyleSheet} from 'react-native';
import {ProgressIndicator} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
});
<>
  <View style={styles.innerContainer}>
    <ProgressIndicator
      label={'Account setup is complete'}
      value={100}
      valueLabel="10 0f 10"
      variant="success"
    />
  </View>
</>
```

### ProgressIndicator variant="warning"

```js
import {StyleSheet} from 'react-native';
import {ProgressIndicator} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
});
<>
  <View style={styles.innerContainer}>
    <ProgressIndicator
      label={'Your membership will expire soon'}
      value={75}
      valueLabel="3 days left"
      variant="warning"
    />
  </View>
</>
```
### ProgressIndicator without labels

```js
import {StyleSheet} from 'react-native';
import {ProgressIndicator} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
});
<>
  <View style={styles.innerContainer}>
    <ProgressIndicator value={85} variant="warning" />
  </View>
  <View style={styles.innerContainer}>
    <ProgressIndicator value={75} variant="error" />
  </View>
  <View style={styles.innerContainer}>
    <ProgressIndicator value={65} variant="success" />
  </View>
  <View style={styles.innerContainer}>
    <ProgressIndicator value={55} variant="info" />
  </View>
</>
```
