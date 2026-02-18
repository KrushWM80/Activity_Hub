```js
import {Chips} from '@walmart/gtp-shared-components';

<Chips
  selected="All"
  chips={[
    {id: 'All', title: 'All'},
    {id: 'Last7Days', title: 'Last 7 Days', disabled: true},
    {id: 'LastMonth', title: 'Last Month'},
    {id: 'Last6Months', title: 'Last 6 Months'},
    {id: '2020', title: '2020'},
  ]}
  onPress={(id) => console.log('Chip Selected: ', id)}
/>;
```

Use the `multiple` property to enable the multiple-select interface.

```js
<Chips
  multiple
  selected={['All', '2020']}
  chips={[
    {id: 'All', title: 'All'},
    {id: 'Last7Days', title: 'Last 7 Days', disabled: true},
    {id: 'LastMonth', title: 'Last Month'},
    {id: 'Last6Months', title: 'Last 6 Months'},
    {id: '2020', title: '2020'},
  ]}
  onPress={(id) => console.log('Chip Selected: ', id)}
/>
```
