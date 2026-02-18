import * as React from 'react';
import {Platform} from 'react-native';
import {Page, Header, VariantText, Section} from '../components';
import {
  Select,
  SelectOptions,
  Selected,
  _KeyboardAvoidingView,
  OSBasedComponentType,
} from '@walmart/gtp-shared-components';

const SelectWithLongListRecipe: React.FC = () => {
  const selectOptions: SelectOptions = [
    {text: 'Welcome'},
    {text: 'Back'},
    {text: 'My'},
    {text: 'Friends'},
    {text: 'To'},
    {text: 'The'},
    {text: 'Show'},
    {text: 'That'},
    {text: 'Never'},
    {text: 'Ends'},
    {text: 'Were'},
    {text: 'So'},
    {text: 'Glad'},
    {text: 'You'},
    {text: 'Could'},
    {text: 'Attend'},
    {text: 'Come'},
    {text: 'Inside'},
    {text: 'Comein'},
    {text: 'Side'},
    {text: 'There'},
    {text: 'Behind'},
    {text: 'Aglass'},
    {text: 'Stands'},
    {text: 'Areal'},
    {text: 'Blade'},
    {text: 'Ofgrass'},
    {text: 'Becareful'},
    {text: 'Asyou'},
    {text: 'Pass'},
    {text: 'Move'},
    {text: 'Along'},
    {text: 'Movealong'},
  ];

  const placeholder = 'Select your favorite...';
  const label = 'Karn Evil 9';

  const componentType: OSBasedComponentType = {
    ios: 'BottomSheet',
    android: 'Modal',
  };

  const handleOnChange = (selected: Array<Selected>) => {
    console.log('---- Picked:', selected);
  };

  const SelectSmall = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>size="small" componentType="InlineView"</VariantText>
        </Header>
        <Section>
          <Select
            size="small"
            selectOptions={selectOptions}
            placeholder={placeholder}
            label={label}
            helperText="Helper text"
            onChange={selected => handleOnChange(selected)}
          />
        </Section>
      </>
    );
  };

  const SelectBottomSheetWithDefaultOption = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>{`${
            componentType[Platform.OS as 'ios' | 'android']
          } selectionType="default"`}</VariantText>
        </Header>
        <Section>
          <Select
            componentType={componentType}
            selectionType="default"
            selectOptions={selectOptions}
            onChange={selected => handleOnChange(selected)}
            placeholder={placeholder}
            label={label}
            helperText="Helper text"
          />
        </Section>
      </>
    );
  };

  const SelectBottomSheetWithSingleOption = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>{`${
            componentType[Platform.OS as 'ios' | 'android']
          } selectionType="single"`}</VariantText>
        </Header>
        <Section>
          <Select
            componentType={componentType}
            selectionType="single"
            selectOptions={selectOptions}
            onChange={selected => handleOnChange(selected)}
            placeholder={placeholder}
            label={label}
            helperText="Helper text"
          />
        </Section>
      </>
    );
  };

  const SelectBottomSheetWithMultiOption = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>{`${
            componentType[Platform.OS as 'ios' | 'android']
          } selectionType="multi"`}</VariantText>
        </Header>
        <Section>
          <Select
            componentType={{ios: 'BottomSheet', android: 'Modal'}}
            selectionType="multi"
            doneButtonTitle="Done"
            cancelButtonTitle="Cancel"
            selectOptions={selectOptions}
            onChange={selected => handleOnChange(selected)}
            placeholder={placeholder}
            label={label}
            helperText="Helper text"
          />
        </Section>
      </>
    );
  };
  const SelectMultiWithOverlay = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>{'Overlay selectionType="multi"'}</VariantText>
        </Header>
        <Section>
          <Select
            componentType={{ios: 'Overlay', android: 'Overlay'}}
            selectionType="multi"
            doneButtonTitle="Done"
            cancelButtonTitle="Cancel"
            selectOptions={selectOptions}
            onChange={selected => handleOnChange(selected)}
            placeholder={placeholder}
            label={label}
            helperText="Helper text"
          />
        </Section>
      </>
    );
  };
  const SelectSingleWithOverlay = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>{'Overlay selectionType="single"'}</VariantText>
        </Header>
        <Section>
          <Select
            componentType={{ios: 'Overlay', android: 'Overlay'}}
            selectionType="single"
            doneButtonTitle="Done"
            cancelButtonTitle="Cancel"
            selectOptions={selectOptions}
            onChange={selected => handleOnChange(selected)}
            placeholder={placeholder}
            label={label}
            helperText="Helper text"
          />
        </Section>
      </>
    );
  };
  const SelectDefaultWithOverlay = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>{'Overlay selectionType="default"'}</VariantText>
        </Header>
        <Section>
          <Select
            componentType={{ios: 'Overlay', android: 'Overlay'}}
            selectionType="default"
            doneButtonTitle="Done"
            cancelButtonTitle="Cancel"
            selectOptions={selectOptions}
            onChange={selected => handleOnChange(selected)}
            placeholder={placeholder}
            label={label}
            helperText="Helper text"
          />
        </Section>
      </>
    );
  };
  const SelectWithError = () => {
    const [errorText, setErrorText] = React.useState<string>('');

    const handleOnChangeWithError = (selected: Array<Selected>) => {
      if (selected[0].index === 2) {
        setErrorText(
          'You have selected this in a previous screen. Please select another item.',
        );
      } else {
        setErrorText('');
      }
      console.log('---- Picked:', selected);
    };
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>with error</VariantText>
        </Header>
        <Section>
          <Select
            selectOptions={selectOptions}
            placeholder={placeholder}
            label={label}
            error={errorText}
            onChange={selected => handleOnChangeWithError(selected)}
          />
        </Section>
      </>
    );
  };

  const SelectDefaultWithLongOption = () => {
    // create local copy of selectOptions
    let localCopy = [...selectOptions];

    // replace one option with a ridiculously long string
    localCopy[1] = {
      text: "Soon the Gypsy Queen In a glaze of Vaseline Will perform on guillotine What a scene! What a scene Next upon the stand Will you please extend a hand To Alexander's Ragtime Band Dixieland, Dixieland",
    };

    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>size="large" with long option text"</VariantText>
        </Header>
        <Section>
          <Select
            selectOptions={localCopy}
            placeholder={placeholder}
            label={label}
            helperText="Helper text"
            onChange={selected => handleOnChange(selected)}
          />
        </Section>
      </>
    );
  };

  return (
    <_KeyboardAvoidingView>
      <Page>
        <SelectSmall />
        <SelectDefaultWithOverlay />
        <SelectSingleWithOverlay />
        <SelectMultiWithOverlay />
        <SelectBottomSheetWithDefaultOption />
        <SelectBottomSheetWithSingleOption />
        <SelectBottomSheetWithMultiOption />
        <SelectWithError />
        <SelectDefaultWithLongOption />
      </Page>
    </_KeyboardAvoidingView>
  );
};

SelectWithLongListRecipe.displayName = 'SelectWithLongListRecipe';
export {SelectWithLongListRecipe};
