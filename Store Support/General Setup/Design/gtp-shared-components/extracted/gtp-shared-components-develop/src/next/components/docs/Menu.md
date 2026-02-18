### Menu bottomLeft
```js
import {StyleSheet} from 'react-native';
import {
  Icons,
  IconButton,
  colors,
  Menu,
  MenuItem,
} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
  content: {
    width:300,
    height:300,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
 const bottomLeft = [
      {
      id: 1,
      leading: <Icons.PencilIcon />,
      label: 'Edit',
    },
    {
      id: 2,
      leading: <Icons.CloudDownloadIcon />,
      label: 'Download',
    },
    {
      id: 3,
      leading: <Icons.TrashCanIcon />,
      label: 'Delete',
    },
    ];
    const [isMenuOpen, setMenuOpen] = React.useState(false);
    <View style={styles.content}>
    <Menu
      isOpen={isMenuOpen}
      position={'bottomLeft'}
      onClose={() => setMenuOpen(!isMenuOpen)}
      trigger={
        <IconButton
          a11yLabel="More actions"
          onPress={() => setMenuOpen(!isMenuOpen)}>
          <Icons.MoreIcon />
        </IconButton>
      }>
      {bottomLeft.map(item => (
        <MenuItem
          leading={item.leading}
          onPress={() => {
            displayPopupAlert(item.label, `${item.label} MenuItemPressed`);
          }}>
          {item.label}
        </MenuItem>
      ))}
    </Menu>
  </View>
```
### Menu bottomRight
```js
import {StyleSheet} from 'react-native';
import {
  Icons,
  IconButton,
  colors,
  Menu,
  MenuItem,
} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
  content: {
    width:300,
    height:300,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
 const bottomRight = [
      {
      id: 1,
      leading: <Icons.PencilIcon />,
      label: 'Edit',
    },
    {
      id: 2,
      leading: <Icons.CloudDownloadIcon />,
      label: 'Download',
    },
    {
      id: 3,
      leading: <Icons.TrashCanIcon />,
      label: 'Delete',
    },
    ];
    const [isMenuOpen, setMenuOpen] = React.useState(false);
   <View style={styles.content}>
   <Menu
      isOpen={isMenuOpen}
      position={'bottomRight'}
      onClose={() => setMenuOpen(!isMenuOpen)}
      trigger={
        <IconButton
          a11yLabel="More actions"
          onPress={() => setMenuOpen(!isMenuOpen)}>
          <Icons.MoreIcon />
        </IconButton>
      }>
      {bottomRight.map(item => (
        <MenuItem
          leading={item.leading}
          onPress={() => {
            displayPopupAlert(item.label, `${item.label} MenuItemPressed`);
          }}>
          {item.label}
        </MenuItem>
      ))}
    </Menu>
  </View>
```
### Menu topLeft
```js
import {StyleSheet} from 'react-native';
import {
  Icons,
  IconButton,
  colors,
  Menu,
  MenuItem,
} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
  content: {
    width:300,
    height:300,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
 const topLeft = [
      {
      id: 1,
      leading: <Icons.PencilIcon />,
      label: 'Edit',
    },
    {
      id: 2,
      leading: <Icons.CloudDownloadIcon />,
      label: 'Download',
    },
    {
      id: 3,
      leading: <Icons.TrashCanIcon />,
      label: 'Delete',
    },
    ];
    const [isMenuOpen, setMenuOpen] = React.useState(false);
    <View style={styles.content}>
    <Menu
      isOpen={isMenuOpen}
      position={'topLeft'}
      onClose={() => setMenuOpen(!isMenuOpen)}
      trigger={
        <IconButton
          a11yLabel="More actions"
          onPress={() => setMenuOpen(!isMenuOpen)}>
          <Icons.MoreIcon />
        </IconButton>
      }>
      {topLeft.map(item => (
        <MenuItem
          leading={item.leading}
          onPress={() => {
            displayPopupAlert(item.label, `${item.label} MenuItemPressed`);
          }}>
          {item.label}
        </MenuItem>
      ))}
    </Menu>
  </View>
```
### Menu topRight
```js
import {StyleSheet} from 'react-native';
import {
  Icons,
  IconButton,
  colors,
  Menu,
  MenuItem,
} from '@walmart/gtp-shared-components';
const styles = StyleSheet.create({
  content: {
    width:300,
    height:300,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
 const topRight = [
      {
      id: 1,
      leading: <Icons.PencilIcon />,
      label: 'Edit',
    },
    {
      id: 2,
      leading: <Icons.CloudDownloadIcon />,
      label: 'Download',
    },
    {
      id: 3,
      leading: <Icons.TrashCanIcon />,
      label: 'Delete',
    },
    ];
    const [isMenuOpen, setMenuOpen] = React.useState(false);
   <View style={styles.content}>
   <Menu
      isOpen={isMenuOpen}
      position={'topRight'}
      onClose={() => setMenuOpen(!isMenuOpen)}
      trigger={
        <IconButton
          a11yLabel="More actions"
          onPress={() => setMenuOpen(!isMenuOpen)}>
          <Icons.MoreIcon />
        </IconButton>
      }>
      {topRight.map(item => (
        <MenuItem
          leading={item.leading}
          onPress={() => {
            displayPopupAlert(item.label, `${item.label} MenuItemPressed`);
          }}>
          {item.label}
        </MenuItem>
      ))}
    </Menu>
  </View>
```