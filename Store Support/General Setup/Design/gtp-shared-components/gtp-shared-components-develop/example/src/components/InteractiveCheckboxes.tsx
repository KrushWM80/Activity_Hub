import * as React from 'react';
import {Checkbox} from '@walmart/gtp-shared-components';

const InteractiveCheckboxes = () => {
  const checkList = ['Lions', 'Tigers', 'And Bears', 'Oh My!'];
  const [checked, setChecked] = React.useState<string[]>([]);
  const [disabled, setDisabled] = React.useState(false);

  // Add/Remove checked item from list
  const handleCheck = (item: string) => {
    let updatedList = [...checked];
    if (checked.includes(item)) {
      updatedList = checked.filter(i => i !== item);
    } else {
      updatedList = [...checked, item];
    }
    setChecked(updatedList);
  };

  const renderList = checkList.map((item, index) => (
    <Checkbox
      key={index}
      label={item}
      checked={checked.includes(item)}
      disabled={disabled}
      onPress={() => handleCheck(item)}
    />
  ));

  return (
    <>
      {renderList}
      <Checkbox
        label="Disable All Above"
        checked={disabled}
        onPress={() => setDisabled(!disabled)}
      />
    </>
  );
};

export {InteractiveCheckboxes};
