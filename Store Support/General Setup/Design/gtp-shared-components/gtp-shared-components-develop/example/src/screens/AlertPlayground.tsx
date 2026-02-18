import * as React from 'react';
import {StyleSheet, Text, View, TextStyle} from 'react-native';
import {
  colors,
  getFont,
  Radio,
  TextField,
  Alert,
  AlertVariant,
  Checkbox,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';
import {displayPopupAlert} from './screensFixtures';

const Spacer = () => <View style={ss.spacer} />;

const alertVariant = ['info', 'error', 'success', 'warning'];

const AlertPlayground: React.FC = () => {
  type Traits = {
    variant?: AlertVariant;
    children: React.ReactNode;
    actionButton: boolean;
  };

  const [tfText, setTfText] = React.useState('Reservation about to expire');
  const [traits, setTraits] = React.useState<Traits>({
    variant: 'info',
    children: tfText,
    actionButton: false,
  });

  const variantHandler = (sel: AlertVariant): void => {
    setTraits({
      ...traits,
      variant: sel,
    });
  };

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <Alert
          variant={traits.variant}
          children={traits.children}
          actionButtonProps={{
            children: traits.actionButton && 'Reserve now',
            onPress: () =>
              traits.actionButton
                ? displayPopupAlert('Action', 'Reserve now pressed')
                : {},
          }}
        />
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Alert traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Checkbox
            label="actionButtonProps"
            checked={!!traits.actionButton}
            onPress={() =>
              setTraits({
                ...traits,
                actionButton: !traits.actionButton,
              })
            }
          />
          <Spacer />
          <Text style={ss.radioHeaderText}>variant</Text>
          {alertVariant.map((v, i) => (
            <Radio
              key={i}
              label={v}
              checked={v === traits.variant}
              onPress={() => variantHandler(v as AlertVariant)}
            />
          ))}

          <Spacer />
          <Text style={ss.radioHeaderText}>children</Text>

          <TextField
            label="(as text)"
            size="small"
            value={tfText}
            onChangeText={_text => {
              setTraits({
                ...traits,
                children: _text as string,
              });
              setTfText(_text);
            }}
          />

          <Spacer />
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
    alignItems: 'center',
    justifyContent: 'center',
  },
  spacer: {
    height: 8,
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
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  } as TextStyle,
});

export {AlertPlayground};
