import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Page, Section, Header} from '../components';
import {formGroupRadio} from './screensFixtures';
import {Radio, FormGroup, colors} from '@walmart/gtp-shared-components';

const FormGroupRadioRecipe = () => {
  const [selectedId, setSelectedId] = React.useState(0);
  return (
    <Page>
      <Section color="white">
        <Header>Form Group with Radio</Header>
        <View style={ss.outerContainer}>
          <FormGroup label="Milkshake ?" error={'Please Choose a Milkshake'}>
            {formGroupRadio.map((item, index) => (
              <Radio
                key={index}
                label={item.label}
                checked={selectedId === item.id}
                onPress={() => {
                  setSelectedId(item.id);
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
export {FormGroupRadioRecipe};
