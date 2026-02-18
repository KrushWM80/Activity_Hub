import * as React from 'react';
import {Platform} from 'react-native';
import {Header, Section, VariantText, Page} from '../components';
import {
  OSBasedComponentType,
  Select,
  Selected,
  SelectOptions,
  TextField,
} from '@walmart/gtp-shared-components';

const ExtraContent: React.FC = () => {
  const [extraContentValue, setExtraContentValue] =
    React.useState('Hello ExtraContent');
  const handleOnSubmitEditing = (event: {nativeEvent: {text: string}}) => {
    console.log(
      'TextField value captured:',
      parseInt(event.nativeEvent.text, 10),
    );
  };
  return (
    <TextField
      label=""
      placeholder="Enter quantity"
      value={extraContentValue}
      onChangeText={txt => setExtraContentValue(txt)}
      onSubmitEditing={handleOnSubmitEditing}
    />
  );
};

const handleOnChange = (selected: Array<Selected>) => {
  console.log('---- Picked :', selected);
};

const componentType = {ios: 'BottomSheet', android: 'Modal'};

const SelectWithExtraContentRecipe = () => {
  const SelectMultiWithExtraContentAfterLastOption = () => {
    const selectOptions: SelectOptions = [
      {text: 'Mug'},
      {text: 'Shirt'},
      {text: 'Sticker'},
      {text: 'Hat - not available', disabled: true},
      {text: 'Hoodie'},
      {text: 'Pins', extraContent: <ExtraContent />},
    ];

    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>{`${
            componentType[Platform.OS as 'ios' | 'android']
          } selectionType="multi" with extraContent below last option`}</VariantText>
        </Header>
        <Section>
          <Select
            componentType={componentType as OSBasedComponentType}
            selectionType="multi"
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            onChange={selected => handleOnChange(selected)}
          />
        </Section>
      </>
    );
  };

  const SelectMultiWithExtraContentAfterMiddleOption = () => {
    const selectOptions: SelectOptions = [
      {text: 'Mug'},
      {text: 'Shirt', extraContent: <ExtraContent />},
      {text: 'Sticker'},
      {text: 'Hat - not available', disabled: true},
      {text: 'Hoodie'},
      {text: 'Pins'},
    ];
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>{`${
            componentType[Platform.OS as 'ios' | 'android']
          } selectionType="multi" with extraContent below last option`}</VariantText>
        </Header>
        <Section>
          <Select
            componentType={componentType as OSBasedComponentType}
            selectionType="multi"
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            onChange={selected => handleOnChange(selected)}
          />
        </Section>
      </>
    );
  };
  const SelectOverlayMultiWithExtraContentAfterMiddleOption = () => {
    const selectOptions: SelectOptions = [
      {text: 'Mug'},
      {text: 'Shirt', extraContent: <ExtraContent />},
      {text: 'Sticker'},
      {text: 'Hat - not available', disabled: true},
      {text: 'Hoodie'},
      {text: 'Pins'},
    ];
    const overlayComponent = {ios: 'Overlay', android: 'Overlay'};
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>{`${
            overlayComponent[Platform.OS as 'ios' | 'android']
          } selectionType="multi" with extraContent below middle option`}</VariantText>
        </Header>
        <Section>
          <Select
            componentType={overlayComponent as OSBasedComponentType}
            selectionType="multi"
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            onChange={selected => handleOnChange(selected)}
          />
        </Section>
      </>
    );
  };

  const SelectOverlaySingleWithExtraContentAfterMiddleOption = () => {
    const selectOptions: SelectOptions = [
      {text: 'Mug'},
      {text: 'Shirt', extraContent: <ExtraContent />},
      {text: 'Sticker'},
      {text: 'Hat - not available', disabled: true},
      {text: 'Hoodie'},
      {text: 'Pins'},
    ];

    const overlayComponent = {ios: 'InlineView', android: 'Overlay'};
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>{`${
            overlayComponent[Platform.OS as 'ios' | 'android']
          } selectionType="Single" with extraContent below middle option`}</VariantText>
        </Header>
        <Section>
          <Select
            componentType={overlayComponent as OSBasedComponentType}
            selectionType="single"
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            onChange={selected => handleOnChange(selected)}
          />
        </Section>
      </>
    );
  };

  return (
    <Page>
      <SelectOverlaySingleWithExtraContentAfterMiddleOption />
      <SelectMultiWithExtraContentAfterLastOption />
      <SelectOverlayMultiWithExtraContentAfterMiddleOption />
      <SelectMultiWithExtraContentAfterMiddleOption />
    </Page>
  );
};

export {SelectWithExtraContentRecipe};
