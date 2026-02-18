### DataTableRow with headers

```js
import {DataTableRow,DataTableHeader} from '@walmart/gtp-shared-components';

<DataTableRow>
  <DataTableHeader alignment={'left'}>
      {"header Left"}
  </DataTableHeader>
  <DataTableHeader alignment={'right'}>
      {"header Right"}
  </DataTableHeader>
</DataTableRow>
```
### DataTableRow with Cell

```js
import {DataTableRow,DataTableCell} from '@walmart/gtp-shared-components';

<DataTableRow>
  <DataTableCell>
      {"Cell Left"}
  </DataTableCell>
  <DataTableCell variant="numeric">
      {"Cell Right"}
  </DataTableCell>
</DataTableRow>
```