### DataTableCellSelect

```js
import {DataTableHeaderSelect} from '@walmart/gtp-shared-components';

const [simpleCellChecked, setSimpleCellChecked] = React.useState(false);

<DataTableHeaderSelect
    name={'Options'}
    numberOfColumns ={1}
    alignment={'right'}
    onChange={()=>setSimpleCellChecked(!simpleCellChecked)}
    checked={simpleCellChecked}
/>
```
### DataTableCellSelect indeterminate

```js
import {DataTableHeaderSelect} from '@walmart/gtp-shared-components';

const [simpleCellChecked, setSimpleCellChecked] = React.useState(true);

<DataTableHeaderSelect
    name={'Options'}
    alignment={'right'}
    onChange={()=>setSimpleCellChecked(!simpleCellChecked)}
    indeterminate={simpleCellChecked}
    numberOfColumns ={1}
/>
```