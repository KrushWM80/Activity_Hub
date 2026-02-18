import * as React from 'react';
import {Text, AccessibilityInfo, findNodeHandle} from 'react-native';
import {Page, Header, VariantText, Section} from '../components';
import {
  Select,
  SelectOptions,
  Selected,
  _KeyboardAvoidingView,
} from '@walmart/gtp-shared-components';

const SelectWithCustomTextRecipe: React.FC = () => {
  const selectOptions: SelectOptions = [
    {text: 'Mug'},
    {text: 'Shirt'},
    {
      text: 'Sticker',
    },
    {text: 'Hat - not available', disabled: true},
    {text: 'Hoodie'},
  ];
  const [selectedOptions, setSelectedOptions] = React.useState(selectOptions);
  const handleOnChange = (_selected: Array<Selected>) => {
    console.log('---- Picked:', _selected);
    setSelectedOptions(
      selectedOptions.map(item => {
        return {...item, selected: item.text === _selected[0].text};
      }),
    );
  };

  const SelectDefault = () => {
    const errorRef = React.useRef(null);
    React.useEffect(() => {
      if (errorRef && errorRef.current) {
        const reactTag = findNodeHandle(errorRef.current);
        if (reactTag) {
          setTimeout(() => {
            // Due to screen lifecycle, we need to put a minor delay.
            AccessibilityInfo.setAccessibilityFocus(reactTag);
          }, 300);
        }
      }
    }, [errorRef]);
    return (
      <>
        <Header>
          Select {'\n  '}
          <VariantText>with custom label and helperText</VariantText>
        </Header>
        <Section>
          <Select
            selectOptions={selectedOptions}
            placeholder="Select your swag..."
            label={<Text>Swag</Text>}
            helperText={<Text>Helper text</Text>}
            error={
              selectedOptions[4]?.selected && (
                <Text ref={errorRef}>Error text ReactNode</Text>
              )
            }
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
      </Page>
    </_KeyboardAvoidingView>
  );
};

SelectWithCustomTextRecipe.displayName = 'SelectWithCustomTextRecipe';
export {SelectWithCustomTextRecipe};
