import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {colors, Checkbox, CheckboxItem} from '@walmart/gtp-shared-components';

import {
  Controller,
  Header,
  InteractiveCheckboxes,
  Page,
  Section,
  SubHeader,
} from '../components';

const CheckboxOverview: React.FC = () => {
  return (
    <Page>
      <Header>Checkboxes</Header>
      <Section space={false} inset={false} color={colors.gray['5']}>
        <Section
          horizontal={false}
          space={false}
          inset={false}
          style={ss.section}>
          <Checkbox label="Unchecked" />
          <Checkbox label="Checked" checked />
          <Checkbox label="Indeterminate" indeterminate />
          <Checkbox label="Checked and Indeterminate" checked indeterminate />
        </Section>
        <Section
          horizontal={false}
          space={false}
          inset={false}
          style={ss.section}>
          <Checkbox label="Unchecked (disabled)" disabled />
          <Checkbox label="Checked (disabled)" checked disabled />
          <Checkbox label="Indeterminate (disabled)" indeterminate disabled />
          <Checkbox
            label="Checked and Indeterminate (disabled)"
            checked
            indeterminate
            disabled
          />
        </Section>
        <SubHeader>No labels</SubHeader>
        <View style={ss.noLabels}>
          <Checkbox />
          <Checkbox checked />
          <Checkbox indeterminate />
          <Checkbox checked indeterminate />
          <Checkbox disabled />
          <Checkbox checked disabled />
          <Checkbox indeterminate disabled />
          <Checkbox checked indeterminate disabled />
        </View>
        <SubHeader>Long label</SubHeader>
        <Section
          horizontal={false}
          space={false}
          inset={false}
          style={ss.section}>
          <Checkbox label="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua" />
        </Section>
        <SubHeader>Interactive</SubHeader>
        <Section
          horizontal={false}
          space={false}
          inset={false}
          style={ss.section}>
          <InteractiveCheckboxes />
        </Section>
      </Section>
      <Header>Checkboxes (Legacy Support)</Header>
      <Section space={false} inset={false} color={colors.gray['5']}>
        <Section
          horizontal
          space={false}
          inset={false}
          style={ss.sectionVerticalZero}>
          <Controller>
            <CheckboxItem label="Unchecked" />
          </Controller>
          <Controller initialValue>
            <CheckboxItem label="Checked" />
          </Controller>
          <Controller initialValue>
            <CheckboxItem label="Ind." indeterminate />
          </Controller>
        </Section>
        <Section
          horizontal
          space={false}
          inset={false}
          style={ss.sectionVerticalZero}>
          <Controller>
            <CheckboxItem label="Unchecked" disabled />
          </Controller>
          <Controller initialValue>
            <CheckboxItem label="Checked" disabled />
          </Controller>
          <Controller initialValue>
            <CheckboxItem label="Ind." indeterminate disabled />
          </Controller>
        </Section>
        <Controller>
          <CheckboxItem label="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua" />
        </Controller>
      </Section>
    </Page>
  );
};

const ss = StyleSheet.create({
  section: {
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  sectionVerticalZero: {
    paddingVertical: 0,
  },
  noLabels: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
});

export {CheckboxOverview};
