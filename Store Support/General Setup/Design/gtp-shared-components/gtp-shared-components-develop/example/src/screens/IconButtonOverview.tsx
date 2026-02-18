import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Header, Page} from '../components';
import {colors, Icons, IconButton} from '@walmart/gtp-shared-components';
import {displayPopupAlert} from './screensFixtures';

const IconButtonOverview: React.FC = () => {
  return (
    <Page>
      <Header>Icon Button (small, medium, large)</Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <IconButton
            children={<Icons.PlusIcon />}
            size="small"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            children={<Icons.PlusIcon />}
            disabled
            size="small"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>

        <View style={ss.innerContainer}>
          <IconButton
            children={<Icons.PlusIcon />}
            size="medium"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            children={<Icons.PlusIcon />}
            disabled
            size="medium"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>

        <View style={ss.innerContainer}>
          <IconButton
            children={<Icons.PlusIcon />}
            size="large"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            children={<Icons.PlusIcon />}
            disabled
            size="large"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>

        <View style={ss.innerContainer}>
          <IconButton
            children={<Icons.CheckIcon />}
            size="small"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            children={<Icons.CheckIcon />}
            disabled
            size="small"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>

        <View style={ss.innerContainer}>
          <IconButton
            children={<Icons.CheckIcon />}
            size="medium"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            children={<Icons.CheckIcon />}
            disabled
            size="medium"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>

        <View style={ss.innerContainer}>
          <IconButton
            children={<Icons.CheckIcon />}
            size="large"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            children={<Icons.CheckIcon />}
            disabled
            size="large"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>

        <View style={ss.innerContainer}>
          <IconButton
            children={<Icons.HomeIcon />}
            size="small"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            children={<Icons.HomeIcon />}
            disabled
            size="small"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>
        <View style={ss.innerContainer}>
          <IconButton
            children={<Icons.HomeIcon />}
            size="medium"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            children={<Icons.HomeIcon />}
            disabled
            size="medium"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>
        <View style={ss.innerContainer}>
          <IconButton
            children={<Icons.HomeIcon />}
            size="large"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            children={<Icons.HomeIcon />}
            disabled
            size="large"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>

        {/* Showcase undocumented feature: ability to change the icon color
         * (this is not in LD3, but having it just in case, it seems like
         * a reasonable thing to request)
         */}
        {/*<View style={s.innerContainer}>
            <IconButton
              children={<Icons.HomeIcon />}
              size="large"
              color={colors.blue['100']}
              disabledColor={colors.blue['60']}
              onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
            />
            <IconButton
              children={<Icons.HomeIcon />}
              disabled
              color={colors.blue['100']}
              disabledColor={colors.blue['60']}
              size="large"
              onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
            /> *
          </View> */}
      </View>
      <Header>Icon Button (legacy support)</Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <IconButton
            icon={<Icons.PlusIcon />}
            size="small"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            icon={<Icons.PlusIcon />}
            disabled
            size="small"
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>
        <View style={ss.innerContainer}>
          <IconButton
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
          <IconButton
            disabled
            onPress={() => displayPopupAlert('Action', 'Icon button pressed')}
          />
        </View>
      </View>
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

export {IconButtonOverview};
