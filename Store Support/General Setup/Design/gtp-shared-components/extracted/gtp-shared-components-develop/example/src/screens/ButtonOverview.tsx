import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, Page, VariantText} from '../components';
import {colors, Icons, Button} from '@walmart/gtp-shared-components';
import ButtonTable from '../components/ButtonTable';
import {displayPopupAlert} from './screensFixtures';

const ButtonOverview: React.FC = () => {
  const otherProps = {
    isLoading: true,
    leading: <Icons.PlusIcon size={24} />,
    trailing: <Icons.PlusIcon size={24} />,
  };

  return (
    <Page>
      <Header>
        Button{'\n  '}
        <VariantText>variant="primary"</VariantText>
      </Header>
      <ButtonTable
        button={
          <Button
            variant="primary"
            onPress={() =>
              displayPopupAlert('Action', 'Primary button pressed')
            }
          />
        }
        {...otherProps}
      />
      <Header>
        Button{'\n  '}
        <VariantText>variant="secondary"</VariantText>
      </Header>
      <ButtonTable
        button={
          <Button
            variant="secondary"
            onPress={() =>
              displayPopupAlert('Action', 'Secondary button pressed')
            }
          />
        }
        {...otherProps}
      />
      <Header>
        Button{'\n  '}
        <VariantText>variant="tertiary"</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Button
            variant="tertiary"
            children="Small"
            onPress={() =>
              displayPopupAlert('Action', 'Tertiary button pressed')
            }
          />
          <Button
            variant="tertiary"
            size="small"
            children="Small"
            disabled
            onPress={() =>
              displayPopupAlert('Action', 'Tertiary button pressed')
            }
          />
        </View>
        <View style={ss.innerContainer}>
          <Button
            variant="tertiary"
            size="medium"
            children="Medium"
            onPress={() =>
              displayPopupAlert('Action', 'Tertiary button pressed')
            }
          />
          <Button
            variant="tertiary"
            size="medium"
            children="Medium"
            disabled
            onPress={() =>
              displayPopupAlert('Action', 'Tertiary button pressed')
            }
          />
        </View>
        <View style={ss.innerContainer}>
          <Button
            variant="tertiary"
            size="large"
            children="Large"
            onPress={() =>
              displayPopupAlert('Action', 'Tertiary button pressed')
            }
          />
          <Button
            variant="tertiary"
            size="large"
            children="Large"
            disabled
            onPress={() =>
              displayPopupAlert('Action', 'Tertiary button pressed')
            }
          />
        </View>
      </View>
      <Header>
        Button{'\n  '}
        <VariantText>variant="destructive"</VariantText>
      </Header>
      <ButtonTable
        button={
          <Button
            variant="destructive"
            onPress={() =>
              displayPopupAlert('Action', 'Destructive button pressed')
            }
          />
        }
        {...otherProps}
      />
    </Page>
  );
};

const ss = StyleSheet.create({
  variantText: {
    fontSize: 15,
  },
  buttonGroup: {
    marginVertical: 16,
  },
  linkContainer: {
    color: 'white',
  },
  innerContainer: {
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
    padding: 10,
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  linkTextColor: {
    color: 'white',
  },
  variantInBody: {
    alignSelf: 'center',
    marginVertical: 12,
    paddingHorizontal: 12,
    marginLeft: 20,
    fontSize: 15,
    lineHeight: 20,
    color: colors.blue['90'],
    borderColor: colors.blue['90'],
    borderWidth: 0.5,
  },
  spacer: {
    height: 16,
  },
});

export {ButtonOverview};
