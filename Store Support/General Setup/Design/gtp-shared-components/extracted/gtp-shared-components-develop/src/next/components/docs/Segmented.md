```js
import {Segmented, Segment} from '@walmart/gtp-shared-components';

const [selectedSegment1, setSelectedSegment1] = React.useState(0);

<Segmented
  size='small'
  selectedIndex={selectedSegment1}
  onChange={index => setSelectedSegment1(index)}>
  <Segment>First</Segment>
  <Segment>Second</Segment>
  <Segment>Third</Segment>
</Segmented>
```

### Use the size property to show a `large` variant. Default - `small`

```js
import {Segmented, Segment} from '@walmart/gtp-shared-components';

const [selectedSegment2, setSelectedSegment2] = React.useState(0);

<Segmented
  size='large'
  selectedIndex={selectedSegment2}
  onChange={index => setSelectedSegment2(index)}>
  <Segment>First</Segment>
  <Segment>Second</Segment>
  <Segment>Third</Segment>
</Segmented>
```

### Disable the Component using `disabled` property

 ```js
import {Segmented, Segment} from '@walmart/gtp-shared-components';

const [selectedSegment3, setSelectedSegment3] = React.useState(0);

<Segmented
  size='large'
  selectedIndex={selectedSegment3}
  onChange={index => setSelectedSegment3(index)}
  disabled={true}>
  <Segment>First</Segment>
  <Segment>Second</Segment>
  <Segment>Third</Segment>
</Segmented>
```
