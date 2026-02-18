import * as React from 'react';
import {StyleSheet} from 'react-native';
import {
  colors,
  List,
  ListItem,
  Switch,
  useSimpleReducer,
} from '@walmart/gtp-shared-components';
import {Header, Page, Section} from '../components';

type SwitchState = {
  orderSwitch: boolean | undefined;
  accountSwitch: boolean | undefined;
  eventSwitch: boolean | undefined;
};
const initialState = {
  orderSwitch: false,
  accountSwitch: false,
  eventSwitch: false,
};

const SwitchRecipes: React.FC = () => {
  const [state, setState] = useSimpleReducer<SwitchState>(initialState);

  const switchHandler = (type: string) => {
    setState(type, !state[type]);
  };

  return (
    <Page>
      <Header>Switches</Header>
      <Section space={false} inset={false} color={colors.gray['5']}>
        <List>
          <ListItem
            title="Order Updates"
            trailing={
              <Switch
                isOn={state['orderSwitch'] as boolean}
                onValueChange={() => switchHandler('orderSwitch')}
              />
            }
            UNSAFE_style={ss.listItem}>
            Get an alert for your pickup and delivery orders
          </ListItem>
          <ListItem
            title="Accounts & Receipts"
            trailing={
              <Switch
                isOn={state['accountSwitch'] as boolean}
                onValueChange={() => switchHandler('accountSwitch')}
              />
            }
            UNSAFE_style={ss.listItem}>
            Get updates on your account, view store receipts, track gift cards
            and more
          </ListItem>
          <ListItem
            title="Events & Specials"
            trailing={
              <Switch
                isOn={state['eventSwitch'] as boolean}
                onValueChange={() => switchHandler('eventSwitch')}
              />
            }
            UNSAFE_style={ss.listItem}>
            Mobile promotions and more
          </ListItem>
        </List>
      </Section>
    </Page>
  );
};

const ss = StyleSheet.create({
  listItem: {
    backgroundColor: 'transparent',
  },
});

export {SwitchRecipes};
