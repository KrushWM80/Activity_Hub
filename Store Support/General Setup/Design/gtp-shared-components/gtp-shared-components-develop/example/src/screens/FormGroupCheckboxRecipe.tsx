import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Page, Section, Header} from '../components';
import {Checkbox, FormGroup, colors} from '@walmart/gtp-shared-components';
import {formGroupCheckbox} from './screensFixtures';

const FormGroupCheckboxRecipe = () => {
  const [selectedIds, setSelectedIds] = React.useState<Array<number>>([]);
  return (
    <Page>
      <Section color="white">
        <Header>Form Group with Radio</Header>
        <View style={ss.outerContainer}>
          <FormGroup label="Bread ?" helperText={'choose bread type'}>
            {formGroupCheckbox.map((item, index) => (
              <Checkbox
                key={index}
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
          </FormGroup>
        </View>
      </Section>
    </Page>
  );
};

const ss = StyleSheet.create({
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    padding: 5,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
});

export {FormGroupCheckboxRecipe};
