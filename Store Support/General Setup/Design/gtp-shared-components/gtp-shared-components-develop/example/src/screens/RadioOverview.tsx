import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {sizesObjects} from './screensFixtures';
import {
  colors,
  Radio,
  RadioItem,
  RadioItemGroup,
} from '@walmart/gtp-shared-components';
import {
  Controller,
  Header,
  InteractiveRadios,
  Page,
  Section,
  SubHeader,
} from '../components';

type FormsScreenState = {
  selectedSizeId: string | undefined;
};

const RadioOverview: React.FC<FormsScreenState> = () => {
  const [selectedSizeId, setSelectedSizeId] = React.useState<
    string | undefined
  >(undefined);

  return (
    <Page>
      <Header>Radios</Header>
      <Section space={false} inset={false} color={colors.gray['5']}>
        <View style={ss.radios}>
          <Radio label="Unselected" />
          <Radio label="Selected" checked />
          <Radio label="Unselected (disabled)" disabled />
          <Radio label="Selected (disabled)" checked disabled />
        </View>
        <SubHeader>No labels</SubHeader>
        <View style={ss.noLabels}>
          <Radio />
          <Radio checked />
          <Radio disabled />
          <Radio checked disabled />
        </View>
        <SubHeader>Long label</SubHeader>
        <Section
          horizontal={false}
          space={false}
          inset={false}
          style={ss.section}>
          <Radio label="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua" />
        </Section>
        <SubHeader>Interactive</SubHeader>
        <Section
          horizontal={false}
          space={false}
          inset={false}
          style={ss.section}>
          <InteractiveRadios />
        </Section>
      </Section>
      <Header>Radios (Legacy Support)</Header>
      <Section space={false} inset={false} color={colors.gray['5']}>
        <Section
          horizontal
          space={false}
          inset={false}
          style={ss.sectionVerticalZero}>
          <Controller>
            <RadioItem label="Unselected" />
          </Controller>
          <Controller initialValue>
            <RadioItem label="Selected" />
          </Controller>
        </Section>
        <Section
          horizontal
          space={false}
          inset={false}
          style={ss.sectionVerticalZero}>
          <Controller>
            <RadioItem label="Unselected" disabled />
          </Controller>
          <Controller initialValue>
            <RadioItem label="Selected" disabled />
          </Controller>
        </Section>
        <Controller>
          <RadioItem label="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua" />
        </Controller>
      </Section>
      <Header>RadioItemGroup (Legacy Support)</Header>
      <Section space={false} inset={false} color={colors.gray['5']}>
        <RadioItemGroup
          items={sizesObjects}
          selectedId={selectedSizeId}
          onSelect={val => {
            if (val) {
              setSelectedSizeId(val);
            }
          }}
        />
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
  radios: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    alignItems: 'flex-start',
  },
});

export {RadioOverview};
