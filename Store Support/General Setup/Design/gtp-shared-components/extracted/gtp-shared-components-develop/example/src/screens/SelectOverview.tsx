import * as React from 'react';
import {Platform, StyleSheet} from 'react-native';
import {Page, Header, VariantText, Section} from '../components';
import {
  Select,
  SelectOptions,
  Selected,
  Icons,
  Card,
  _KeyboardAvoidingView,
  OSBasedComponentType,
} from '@walmart/gtp-shared-components';

const SelectOverview: React.FC = () => {
  const selectOptions: SelectOptions = [
    {text: 'Mug'},
    {text: 'Shirt'},
    {
      text: 'Sticker',
    },
    {text: 'Hat - not available', disabled: true},
    {text: 'Hoodie'},
  ];

  const componentType: OSBasedComponentType = {
    ios: 'BottomSheet',
    android: 'Modal',
  };

  const handleOnChange = (selected: Array<Selected>) => {
    console.log('---- Picked:', selected);
  };

  const SelectDefault = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>
            size="large (default)" componentType="InlineView (default)"
          </VariantText>
        </Header>
        <Section>
          <Select
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            onChange={handleOnChange}
          />
        </Section>
      </>
    );
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
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            onChange={handleOnChange}
          />
        </Section>
      </>
    );
  };
  const SelectWithSingle = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>
            size="large (default)" componentType="InlineView (default)
            selectionType="single""
          </VariantText>
        </Header>
        <Section>
          <Select
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            selectionType="single"
            helperText="Helper text"
            onChange={handleOnChange}
          />
        </Section>
      </>
    );
  };
  const SelectWithMulti = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>
            size="large (default)" componentType="InlineView (default)
            selectionType="multi""
          </VariantText>
        </Header>
        <Section>
          <Select
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            selectionType="multi"
            helperText="Helper text"
            onChange={handleOnChange}
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
            onChange={handleOnChange}
            placeholder="Select your swag..."
            label="Swag"
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
            onChange={handleOnChange}
            placeholder="Select your swag..."
            label="Swag"
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
            modalProps={{
              animationInTiming: 1,
              animationOutTiming: 1,
              backdropTransitionInTiming: 1,
              backdropTransitionOutTiming: 1,
            }}
            bottomSheetProps={{
              animationInTiming: 1,
              animationOutTiming: 1,
              backdropTransitionInTiming: 1,
              backdropTransitionOutTiming: 1,
            }}
            onChange={selected => {
              handleOnChange(selected);
            }}
            placeholder="Select your swag..."
            label="Swag"
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
            onChange={handleOnChange}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
          />
        </Section>
      </>
    );
  };
  const SelectDefaultWithCardOverlay = () => {
    return (
      <>
        <Header>
          Select Inside Card{'\n  '}
          <VariantText>{'Overlay selectionType="default"'}</VariantText>
        </Header>
        <Section>
          <Card UNSAFE_style={ss.cardContent}>
            <Select
              componentType={{ios: 'Overlay', android: 'Overlay'}}
              selectionType="default"
              doneButtonTitle="Done"
              UNSAFE_style={{width: '100%'}}
              cancelButtonTitle="Cancel"
              selectOptions={selectOptions}
              onChange={handleOnChange}
              placeholder="Select your swag..."
              label="Swag"
              helperText="Helper text"
            />
          </Card>
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
            onChange={handleOnChange}
            placeholder="Select your swag..."
            label="Swag"
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
            onChange={handleOnChange}
            placeholder="Select your swag..."
            label="Swag"
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
            placeholder="Select your swag..."
            label="Swag"
            error={errorText}
            onChange={selected => handleOnChangeWithError(selected)}
          />
        </Section>
      </>
    );
  };

  const SelectDisabled = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>disabled</VariantText>
        </Header>
        <Section>
          <Select
            disabled
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            leading={<Icons.EmailIcon />}
            onChange={handleOnChange}
          />
        </Section>
      </>
    );
  };

  const SelectWithLeading = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>with leading</VariantText>
        </Header>
        <Section>
          <Select
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            leading={<Icons.HomeIcon />}
            onChange={handleOnChange}
          />
        </Section>
      </>
    );
  };

  const SelectWithLeadingSmall = () => {
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>with leading small</VariantText>
        </Header>
        <Section>
          <Select
            size="small"
            selectOptions={selectOptions}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            leading={<Icons.HomeIcon />}
            onChange={handleOnChange}
          />
        </Section>
      </>
    );
  };

  const SelectDefaultWithPreselect = () => {
    // create local copy of selectOptions
    let localCopy = [...selectOptions];

    // preselect Shirt
    localCopy[1] = {text: 'Shirt', selected: true};

    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>
            size="large" (default) with preselected value
          </VariantText>
        </Header>
        <Section>
          <Select
            selectOptions={localCopy}
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            onChange={handleOnChange}
          />
        </Section>
      </>
    );
  };

  const SelectDefaultWithLongOption = () => {
    // create local copy of selectOptions
    let localCopy = [...selectOptions];

    // replace 'Shirt' with a long string
    localCopy[1] = {
      text: 'Shirt and many many many other things here going on and on forever',
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
            placeholder="Select your swag..."
            label="Swag"
            helperText="Helper text"
            onChange={handleOnChange}
          />
        </Section>
      </>
    );
  };

  return (
    <_KeyboardAvoidingView>
      <Page>
        <SelectDefault />
        <SelectSmall />
        <SelectWithSingle />
        <SelectWithMulti />
        <SelectDefaultWithOverlay />
        <SelectDefaultWithCardOverlay />
        <SelectSingleWithOverlay />
        <SelectMultiWithOverlay />
        <SelectBottomSheetWithDefaultOption />
        <SelectBottomSheetWithSingleOption />
        <SelectBottomSheetWithMultiOption />
        <SelectWithError />
        <SelectDisabled />
        <SelectWithLeading />
        <SelectWithLeadingSmall />
        <SelectDefaultWithLongOption />
        <SelectDefaultWithPreselect />
      </Page>
    </_KeyboardAvoidingView>
  );
};
const ss = StyleSheet.create({
  cardContent: {
    borderRadius: 10,
    marginBottom: 16,
    paddingHorizontal: 16,
    paddingBottom: 16,
  },
});
SelectOverview.displayName = 'SelectOverview';
export {SelectOverview};
