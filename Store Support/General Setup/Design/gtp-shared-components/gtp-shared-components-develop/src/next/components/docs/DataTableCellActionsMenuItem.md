### DataTableCellActionsMenuItem

```js
import {
  DataTableCellActionsMenuItem,
  Icons,
} from '@walmart/gtp-shared-components';
<DataTableCellActionsMenuItem
  onPress={() => console.log("itemPressed")}>
Email
</DataTableCellActionsMenuItem>
```
### DataTableCellActionsMenuItem with icon
```js
import {
  DataTableCellActionsMenuItem,
  Icons,
} from '@walmart/gtp-shared-components';
<DataTableCellActionsMenuItem
  onPress={() => console.log("itemPressed")}
  leading={<Icons.PencilIcon />}
  >
Edit
</DataTableCellActionsMenuItem>
```