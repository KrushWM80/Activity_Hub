import * as React from 'react';
import {
  Controller,
  Header,
  InteractiveCheckboxes,
  InteractiveRadios,
  InteractiveSwitches,
  Page,
  Section,
  SubHeader,
} from '../components';
import {StyleSheet, View} from 'react-native';
import {sizesObjects} from './screensFixtures';
import {
  colors,
  Checkbox,
  CheckboxItem,
  DateDropdown,
  RadioItemGroup,
  List,
  ListItem,
  Radio,
  RadioItem,
  Switch,
  ToggleItem,
} from '@walmart/gtp-shared-components';

type FormsScreenState = {
  date: Date | undefined;
  selectedSizeId: string | undefined;
};

const FormsOverview: React.FC<FormsScreenState> = () => {
  const [date, setDate] = React.useState<Date | undefined>(undefined);
  const [selectedSizeId, setSelectedSizeId] = React.useState<
    string | undefined
  >(undefined);

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
      <Header>Switches</Header>
      <Section space={false} inset={false} color={colors.gray['5']}>
        <View style={ss.switches}>
          <Switch label="Off" />
          <Switch label="On" isOn />
          <Switch label="Off (disabled)" disabled />
          <Switch label="On (dlsabled)" isOn disabled />
        </View>
        <SubHeader>No labels</SubHeader>
        <View style={ss.noLabels}>
          <Switch />
          <Switch isOn />
          <Switch disabled />
          <Switch isOn disabled />
        </View>
        <SubHeader>Interactive</SubHeader>
        <Section
          horizontal={false}
          space={false}
          inset={false}
          style={ss.section}>
          <InteractiveSwitches />
        </Section>
        <SubHeader>List with Switches</SubHeader>
        <List>
          <ListItem
            title="Order Updates"
            trailing={<Switch />}
            UNSAFE_style={ss.listItem}>
            Get an alert for your pickup and delivery orders
          </ListItem>
          <ListItem
            title="Accounts & Receipts"
            trailing={<Switch />}
            UNSAFE_style={ss.listItem}>
            Get updates on your account, view store receipts, track gift cards
            and more
          </ListItem>
          <ListItem
            title="Events & Specials"
            trailing={<Switch />}
            UNSAFE_style={ss.listItem}>
            Mobile promotions and more
          </ListItem>
        </List>
      </Section>
      <Header>Toggles (Legacy Support)</Header>
      <Section space={false} inset={false} color={colors.gray['5']}>
        <Controller setValueProp="onValueChange">
          <ToggleItem>Untoggled</ToggleItem>
        </Controller>
        <Controller initialValue setValueProp="onValueChange">
          <ToggleItem>Toggled</ToggleItem>
        </Controller>
        <Controller setValueProp="onValueChange">
          <ToggleItem>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua
          </ToggleItem>
        </Controller>
        <SubHeader>Small Variant</SubHeader>
        <Controller setValueProp="onValueChange">
          <ToggleItem small>Untoggled</ToggleItem>
        </Controller>
        <Controller initialValue setValueProp="onValueChange">
          <ToggleItem small>Toggled</ToggleItem>
        </Controller>
        <Section
          horizontal
          space={false}
          inset={false}
          style={ss.sectionVerticalZero}>
          <Controller setValueProp="onValueChange">
            <ToggleItem small>Untoggled</ToggleItem>
          </Controller>
          <Controller initialValue setValueProp="onValueChange">
            <ToggleItem small>Toggled</ToggleItem>
          </Controller>
        </Section>
        <Controller setValueProp="onValueChange">
          <ToggleItem small>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do
            eiusmod tempor incididunt ut labore et dolore magna aliqua
          </ToggleItem>
        </Controller>
      </Section>
      <Header>Date Selector</Header>
      <Section inset={false}>
        <Controller setValueProp="onSelect">
          <DateDropdown
            value={date}
            onSelect={dt => {
              if (dt) {
                setDate(dt);
              }
            }}
            label="Date"
            helperText="Select one of these dates!"
            UNSAFE_style={ss.innerElement}
          />
        </Controller>
      </Section>
      <Header>Date Selector - with Success State</Header>
      <Section inset={false}>
        <Controller setValueProp="onSelect">
          <DateDropdown
            value={date}
            label="Date"
            helperText="Select one of these dates!"
            onSelect={dt => {
              if (dt) {
                setDate(dt);
              }
            }}
            UNSAFE_style={ss.innerElement}
          />
        </Controller>
      </Section>
      <Header>Date Selector - with Error State</Header>
      <Section inset={false}>
        <Controller setValueProp="onSelect">
          <DateDropdown
            value={date}
            error={date ? '' : 'this field is required'}
            label="Date"
            helperText="Select one of these dates!"
            onSelect={dt => {
              if (dt) {
                setDate(dt);
              }
            }}
            UNSAFE_style={ss.innerElement}
          />
        </Controller>
      </Section>
    </Page>
  );
};

const ss = StyleSheet.create({
  innerElement: {
    marginHorizontal: 16,
  },
  section: {
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  sectionVerticalZero: {
    paddingVertical: 0,
  },
  listItem: {
    backgroundColor: 'transparent',
  },
  switches: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    alignItems: 'flex-start',
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

export {FormsOverview};
