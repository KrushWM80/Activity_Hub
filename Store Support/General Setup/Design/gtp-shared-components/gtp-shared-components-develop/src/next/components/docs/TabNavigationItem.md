### TabNavigationItem Selected
```js
import { TabNavigationItem,Icons} from '@walmart/gtp-shared-components';
const [currentTab, setCurrentTab] = React.useState(true);
<TabNavigationItem
 isCurrent={currentTab}
 onPress={() => setCurrentTab(!currentTab)}
  >
  {"One"}
</TabNavigationItem>
```
### TabNavigationItem With leading
```js
import { TabNavigationItem,Icons} from '@walmart/gtp-shared-components';
const [currentTab, setCurrentTab] = React.useState(false);
<TabNavigationItem
  leading={<Icons.CartIcon />}
  onPress={() => setCurrentTab(!currentTab)}
  isCurrent={currentTab}
  >
  {"One"}
</TabNavigationItem>
```
### TabNavigationItem Trailing
```js
import {StyleSheet} from 'react-native';
import { TabNavigationItem,Icons,Badge} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
   badge: {
    marginLeft: 8,
  },
});
const [currentTab, setCurrentTab] = React.useState(false);
<TabNavigationItem
  onPress={() => setCurrentTab(!currentTab)}
  isCurrent={currentTab}
  trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
  {"One"}
</TabNavigationItem>
```
### TabNavigationItem Leading and Trailing
```js
import {StyleSheet} from 'react-native';
import { TabNavigationItem,Icons,Badge} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
   badge: {
    marginLeft: 8,
  },
});
const [currentTab, setCurrentTab] = React.useState(false);
<TabNavigationItem
  leading={<Icons.CartIcon />}
  onPress={() => setCurrentTab(!currentTab)}
  isCurrent={currentTab}
  trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
  {"One"}
</TabNavigationItem>
```