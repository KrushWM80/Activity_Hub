### TabNavigation
```js
import {StyleSheet} from 'react-native';
import { TabNavigation,TabNavigationItem,Icons,Badge} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
   badge: {
    marginLeft: 8,
  },
});
const [currentTab, setCurrentTab] = React.useState(1);
 <TabNavigation  >
    <TabNavigationItem
        leading={<Icons.CartIcon />}
        isCurrent={currentTab===0}
        onPress={() => setCurrentTab(0)}
        trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
        {"One"}
      </TabNavigationItem>
      <TabNavigationItem
        isCurrent={currentTab===1}
        leading={<Icons.CartIcon />}
        onPress={() => setCurrentTab(1)}
        trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
        {"Two"}
      </TabNavigationItem>
      <TabNavigationItem
        leading={<Icons.CartIcon />}
        isCurrent={currentTab===2}
        onPress={() => setCurrentTab(2)}
        trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
        {"Three"}
      </TabNavigationItem>
  </TabNavigation>
```
### TabNavigation with Scroll
```js
import {StyleSheet} from 'react-native';
import { TabNavigation,TabNavigationItem,Icons,Badge} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
   badge: {
    marginLeft: 8,
  },
});
const [currentTab, setCurrentTab] = React.useState(2);
 <TabNavigation>
    <TabNavigationItem
        leading={<Icons.CartIcon />}
        isCurrent={currentTab===0}
        onPress={() => setCurrentTab(0)}
        trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
        {"One"}
      </TabNavigationItem>
      <TabNavigationItem
        leading={<Icons.CartIcon />}
        isCurrent={currentTab===1}
        onPress={() => setCurrentTab(1)}
        trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
        {"Two"}
      </TabNavigationItem>
      <TabNavigationItem
        leading={<Icons.CartIcon />}
        isCurrent={currentTab===2}
        onPress={() => setCurrentTab(2)}
        trailing={<Badge color="gray" UNSAFE_style={styles.badge}>10</Badge>}>
        {"Three"}
      </TabNavigationItem>
      <TabNavigationItem
        leading={<Icons.CartIcon />}
        isCurrent={currentTab===3}
        onPress={() => setCurrentTab(3)}
        trailing={<Badge color="blue">10</Badge>}>
        {"Four"}
      </TabNavigationItem>
      <TabNavigationItem
        leading={<Icons.CartIcon />}
        isCurrent={currentTab===4}
        onPress={() => setCurrentTab(4)}
        trailing={<Badge color="green" UNSAFE_style={styles.badge}>10</Badge>}>
        {"Five"}
      </TabNavigationItem>
       <TabNavigationItem
        leading={<Icons.CartIcon />}
        isCurrent={currentTab===5}
        onPress={() => setCurrentTab(5)}
        trailing={<Badge color="blue" UNSAFE_style={styles.badge}>10</Badge>}>
        {"Six"}
      </TabNavigationItem>
  </TabNavigation>
```
