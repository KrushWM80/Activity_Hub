import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Page, Section, Header} from '../components';
import {ListWithCheckbox} from '../components/ListWithCheckbox';
import {colors} from '@walmart/gtp-shared-components';

const ToggleablesRecipe = () => {
  const [selectedIds, setSelectedIds] = React.useState<Array<number>>([]);

  return (
    <Page>
      <Section color="white">
        <Header>List with Checkbox's</Header>
        <View style={ss.outerContainer}>
          <ListWithCheckbox
            selectedIds={selectedIds}
            onSelect={(ids: Array<number>) => {
              setSelectedIds(ids);
              console.log('ids : ', ids);
            }}
          />
        </View>
      </Section>
    </Page>
  );
};

const ss = StyleSheet.create({
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
});

export {ToggleablesRecipe};
