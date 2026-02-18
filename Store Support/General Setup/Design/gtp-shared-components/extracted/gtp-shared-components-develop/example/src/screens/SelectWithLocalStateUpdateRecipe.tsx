import * as React from 'react';
import {Page, Header, VariantText, Section} from '../components';
import {
  Select,
  SelectOptions,
  Selected,
  _KeyboardAvoidingView,
} from '@walmart/gtp-shared-components';

const SelectWithLocalStateUpdateRecipe = () => {
  const selectOptions: SelectOptions = [
    {text: 'Mug'},
    {text: 'Shirt'},
    {
      text: 'Sticker',
    },
    {text: 'Hat - not available', disabled: true},
    {text: 'Hoodie'},
  ];

  const [count, setCount] = React.useState(0);
  const [multiCount, setMultiCount] = React.useState(0);
  const handleSingleChange = (selected: Array<Selected>) => {
    setCount(count + 1);
    console.log('---- count:', count);
    console.log('---- Picked:', selected);
  };
  const handleMultiChange = (selected: Array<Selected>) => {
    setMultiCount(multiCount + 1);
    console.log('---- count:', multiCount);
    console.log('---- Picked:', selected);
  };

  return (
    <_KeyboardAvoidingView>
      <Page>
        <>
          <Header>
            Select {'\n  '}
            <VariantText>local state update onSelection</VariantText>
          </Header>
          <Section>
            <Select
              selectOptions={selectOptions}
              placeholder="Select your swag..."
              label="Swag"
              helperText="Helper text"
              onChange={handleSingleChange}
            />
            <VariantText>{`number Of selection: ${count}`}</VariantText>
          </Section>
        </>
        <>
          <Header>
            Select {'\n  '}
            <VariantText>{'local state update on Multi Selection'}</VariantText>
          </Header>
          <Section>
            <Select
              componentType={{ios: 'BottomSheet', android: 'Modal'}}
              selectionType="multi"
              doneButtonTitle="Done"
              cancelButtonTitle="Cancel"
              selectOptions={selectOptions}
              onChange={handleMultiChange}
              placeholder="Select your swag..."
              label="Swag"
              helperText="Helper text"
            />
            <VariantText>{`number Of selection: ${multiCount}`}</VariantText>
          </Section>
        </>
      </Page>
    </_KeyboardAvoidingView>
  );
};

export {SelectWithLocalStateUpdateRecipe};
