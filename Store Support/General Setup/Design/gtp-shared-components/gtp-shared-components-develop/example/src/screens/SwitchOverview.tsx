import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {colors, List, ListItem, Switch} from '@walmart/gtp-shared-components';
import {
  Header,
  InteractiveSwitches,
  Page,
  Section,
  SubHeader,
} from '../components';

const SwitchOverview: React.FC = () => {
  return (
    <Page>
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
    </Page>
  );
};

const ss = StyleSheet.create({
  section: {
    paddingVertical: 12,
    paddingHorizontal: 16,
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
});

export {SwitchOverview};
