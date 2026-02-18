import * as React from 'react';
import {View, StyleSheet, Text, TextStyle} from 'react-native';
import {
  List,
  ListItem,
  Icons,
  Button,
  Checkbox,
  colors,
  TextField,
  getFont,
} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';
import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

const ListPlayground = () => {
  type Traits = {
    title?: React.ReactNode;
    children: React.ReactNode;
    leading?: boolean;
    trailing?: boolean;
    titleFlag?: boolean;
  };

  const [traits, setTraits] = React.useState<Traits>({
    children: 'French fries are delicious.',
    title: 'Potato!',
    leading: true,
    trailing: true,
    titleFlag: true,
  });

  const trailingElement = () => {
    return (
      <Button
        variant="tertiary"
        onPress={() => displayPopupAlert('Action', 'Action button pressed')}>
        Action
      </Button>
    );
  };

  React.useEffect(() => {
    if (traits.titleFlag) {
      setTraits({
        ...traits,
        title: 'Potato!',
      });
    } else {
      setTraits({
        ...traits,
        title: '',
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [traits.titleFlag]);

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <List>
          <ListItem
            title={traits.title}
            leading={traits.leading ? <Icons.BoxIcon /> : <></>}
            trailing={traits.trailing ? trailingElement() : <></>}>
            {traits.children}
          </ListItem>
        </List>
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>ListItem traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Checkbox
            label="leading"
            checked={!!traits.leading}
            onPress={() =>
              setTraits({
                ...traits,
                leading: !traits.leading,
              })
            }
          />
          <Spacer />
          <Checkbox
            label="trailing"
            checked={!!traits.trailing}
            onPress={() =>
              setTraits({
                ...traits,
                trailing: !traits.trailing,
              })
            }
          />

          <Spacer />
          <Text style={ss.radioHeaderText}>children</Text>
          <TextField
            label="(as text)"
            value={traits.children as string}
            onChangeText={_text => {
              setTraits({
                ...traits,
                children: _text as React.ReactNode,
              });
            }}
          />

          <Spacer />
          <Checkbox
            label={<Text style={ss.radioHeaderText}>title</Text>}
            checked={traits.titleFlag}
            onPress={() =>
              setTraits({
                ...traits,
                titleFlag: !traits.titleFlag,
              })
            }
          />
          <TextField
            disabled={!traits.titleFlag}
            label="(as text)"
            size="small"
            value={traits.title as string}
            onChangeText={_text => {
              setTraits({
                ...traits,
                title: _text as React.ReactNode,
              });
            }}
          />
        </View>
      </Page>
    </View>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  buttonContainer: {
    minHeight: 80,
    marginHorizontal: 16,
    borderRadius: 12,
    paddingVertical: 10,
    borderColor: colors.blue['90'],
    paddingHorizontal: 8,
    borderWidth: 0.5,
    backgroundColor: colors.gray['10'],
  },
  innerContainer: {
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.blue['90'],
    borderTopColor: colors.blue['90'],
    borderBottomColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingHorizontal: 8,
    paddingBottom: 8,
    borderWidth: 1,
  },
  spacer: {
    height: 8,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
    borderTopColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingRight: 16,
    paddingVertical: 8,
    marginTop: 8,
  },
  headerText: {
    fontSize: 20,
    fontWeight: '500',
    color: colors.blue['90'],
    textAlign: 'left',
    paddingVertical: 4,
    marginLeft: 12,
  },
  radioHeaderText: {
    ...getFont('500'),
    fontSize: 20,
    color: colors.blue['90'],
  } as TextStyle,
});

export {ListPlayground};
