### ListItem

```js
import {ListItem,Icons,Button,IconButton} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;
<>
  <ListItem>
   List Item with large text,French fries are delicious French fries
   are delicious.
 </ListItem>
</>
```
### ListItem with Title

```js
import {List,ListItem} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;
<>
  <ListItem
    title="Truck">
   Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet consectetur.
  </ListItem>
</>
```
### ListItem with Title & Leading

```js
import {List,ListItem,Icons} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

  <>
    <ListItem
     title="Truck"
     leading={<Icons.TruckIcon />}
    >
     Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet consectetur.
    </ListItem>
  </>

```
### ListItem with Leading & Trailing

```js
import {List,ListItem,Icons,Button,IconButton} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

  <>
    <ListItem
      title="Truck"
      leading={<Icons.TruckIcon size={24} />}
      trailing={
                <Button
                  variant={'tertiary'}
                  onPress={() =>
                    displayPopupAlert('Action', 'Action1 button pressed')
                  }>
                    Action1
                </Button>
            }>
       Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet consectetur.
    </ListItem>
  </>

```
### ListItem with Trailing

```js
import {List,ListItem,Icons,Button,IconButton} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

  <>
    <ListItem
      title="Box"
      trailing={
                <IconButton
                  children={<Icons.ChevronRightIcon />}
                  size="small"
                  onPress={() =>
                    displayPopupAlert('Action', 'icon button pressed')
                 }
                />
                }
      >
      Get it shipped to your door
    </ListItem>
  </>

```