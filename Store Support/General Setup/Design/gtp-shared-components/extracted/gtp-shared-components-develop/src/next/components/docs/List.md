### List

```js
import {List,ListItem,Icons,Button,IconButton} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

<List>
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
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor
        sit amet consectetur.
      </ListItem>
      <ListItem
        title="Box"
        leading={<Icons.BoxIcon size={24} />}
        trailing={
          <IconButton
            children={<Icons.ChevronRightIcon />}
            size="small"
            onPress={() => displayPopupAlert('Action', 'icon button pressed')}
          />
        }>
        Get it shipped to your door
      </ListItem>
      <ListItem title="Truck" leading={<Icons.TruckIcon />}>
        Lorem ipsum dolor sit amet,consectetur adipisicing elit,sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua
      </ListItem>
      <ListItem title="Truck">
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor
        sit amet consectetur.
      </ListItem>
      <ListItem>
        List Item with large text,French fries are delicious French fries are
        delicious.
      </ListItem>
      <ListItem>List with small text, French fries are delicious.</ListItem>
    </List>

```

### List With Items Array

```js
import {List,ListItem,Link,Icons,Button,IconButton} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;
const itemsArray = [
  {
    title: 'Truck',
    content:
      'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet consectetur.',
    leading: <Icons.InfoCircleIcon size={24} />,
    trailing: (
      <Link
        onPress={() => displayPopupAlert('Action', 'Action Link Pressed')}
        children={'Action1'}
      />
    ),
  },
  {
    title: 'Box',
    content: 'Get it shipped to your door',
    leading: <Icons.InfoCircleIcon size={24} />,
    trailing: (
      <IconButton
        children={<Icons.ChevronRightIcon />}
        size="small"
        onPress={() => displayPopupAlert('Action', 'icon button pressed')}
      />
    ),
  },
];

<List>
      {
        itemsArray.map((item,index) => {
        const {title, content, leading, trailing} = item;
        return (
          <ListItem
            title={title}
            leading={leading}
            trailing={trailing}
            key={index}>
                {content}
          </ListItem>
        );
      })
      }
</List>

```