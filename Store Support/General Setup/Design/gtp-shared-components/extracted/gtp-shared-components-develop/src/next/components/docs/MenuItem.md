### MenuItem
```js
import {Icons, MenuItem} from '@walmart/gtp-shared-components';
<MenuItem
  onPress={() => {
        displayPopupAlert('Edit', 'Edit MenuItemPressed');
      }}>
      Edit
</MenuItem>;
```
### MenuItem with Leading
```js
import {Icons, MenuItem} from '@walmart/gtp-shared-components';
<MenuItem
  leading={<Icons.PencilIcon />}
  onPress={() => {
        displayPopupAlert('Edit', 'Edit MenuItemPressed');
      }}>
      Edit
</MenuItem>;
```