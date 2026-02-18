### FormGroup Checkbox

```js
import {Checkbox,Radio,FormGroup,} from '@walmart/gtp-shared-components';
const itemsArray = [
  {
    id:1,
    label:'Labels that are long should wrap to the additional lines. This applies to all anatomy elements include Group Label, Helper Text, Error Text, and Checkboxes or Radios'
  },{
    id:2,
    label:'Apple'
  },{
    id:3,
    label:'Cookie'
  }
];
 const [selectedIds, setSelectedIds] = React.useState([]);
<FormGroup
      label="Labels that are long should wrap to the additional lines. This applies to all anatomy elements include Group Label, Helper Text, Error Text, and Checkboxes or Radios?"
      helperText={'write helperText'}>
      {itemsArray.map((item, index) => (
        <Checkbox
          label={item.label}
          checked={selectedIds.includes(item.id)}
          onPress={() => {
            if (selectedIds.includes(item.id)) {
              setSelectedIds(selectedIds.filter(i => i !== item.id));
            } else {
              setSelectedIds([...selectedIds, item.id]);
            }
          }}
        />
      ))}
    </FormGroup>;

```
### FormGroup Radio

```js
import {Radio,FormGroup,} from '@walmart/gtp-shared-components';
const itemsArray = [
      {
        id: 1,
        label:
          'Labels that are long should wrap to the additional lines. This applies to all anatomy elements include Group Label, Helper Text, Error Text, and Checkboxes or Radios',
      },
      {
        id: 2,
        label: 'Apple',
      },
      {
        id: 3,
        label: 'Cookie',
      },
    ];
    const [selectedId, setSelectedId] = React.useState(0);
    <FormGroup
      label="Labels that are long should wrap to the additional lines. This applies to all anatomy elements include Group Label, Helper Text, Error Text, and Checkboxes or Radios?"
      error={'write errorText '}>
      {itemsArray.map(item => (
        <Radio
          label={item.label}
          checked={selectedId === item.id}
          onPress={() => setSelectedId(item.id)}
        />
      ))}
    </FormGroup>;
```