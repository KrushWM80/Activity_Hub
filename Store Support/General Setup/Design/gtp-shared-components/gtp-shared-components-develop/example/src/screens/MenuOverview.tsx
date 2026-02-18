import * as React from 'react';
import {StyleSheet, SafeAreaView, View} from 'react-native';
import {
  Icons,
  IconButton,
  colors,
  Menu,
  MenuItem,
  MenuPosition,
  useSimpleReducer,
} from '@walmart/gtp-shared-components';
import {Header, VariantText, Section, Page} from '../components';
import {displayPopupAlert, menus} from './screensFixtures';

type MenuOpenState = {
  isTopLeftMenuOpen: boolean;
  isTopRightMenuOpen: boolean;
  isBottomLeftMenuOpen: boolean;
  isBottomRightMenuOpen: boolean;
};
const initialState = {
  isTopLeftMenuOpen: false,
  isTopRightMenuOpen: false,
  isBottomLeftMenuOpen: false,
  isBottomRightMenuOpen: false,
};

const MenuOverview = () => {
  const [state, setState] = useSimpleReducer<MenuOpenState>(initialState);

  const isMenuOpen = (menuPosition: string): boolean => {
    switch (menuPosition) {
      case 'bottomLeft':
        return state.isBottomLeftMenuOpen as boolean;
      case 'bottomRight':
        return state.isBottomRightMenuOpen as boolean;
      case 'topLeft':
        return state.isTopLeftMenuOpen as boolean;
      case 'topRight':
        return state.isTopRightMenuOpen as boolean;
      default:
        return false;
    }
  };

  const setMenuOpen = (menuPosition: string) => {
    switch (menuPosition) {
      case 'bottomLeft':
        setState('isBottomLeftMenuOpen', !state.isBottomLeftMenuOpen);
        return;
      case 'bottomRight':
        setState('isBottomRightMenuOpen', !state.isBottomRightMenuOpen);
        return;
      case 'topLeft':
        setState('isTopLeftMenuOpen', !state.isTopLeftMenuOpen);
        return;
      case 'topRight':
        setState('isTopRightMenuOpen', !state.isTopRightMenuOpen);
        return;
      default:
        return;
    }
  };

  const renderMenuItem = (
    menuPosition: MenuPosition,
    item: {
      id: number;
      leading: React.JSX.Element;
      label: string;
    },
  ) => {
    return (
      <MenuItem
        key={item.id}
        leading={item.leading}
        onPress={() => {
          setMenuOpen(menuPosition);
          displayPopupAlert(item.label, `${item.label} MenuItemPressed`);
        }}>
        {item.label}
      </MenuItem>
    );
  };
  const renderMenu = (
    menuPosition: string,
    menuItems: {id: number; leading: React.JSX.Element; label: string}[],
  ) => {
    return (
      <Page key={menuPosition}>
        <Header>
          Menu {'\n  '}
          <VariantText>{`position:${menuPosition}`} </VariantText>
        </Header>
        <Section>
          <View style={styles.content}>
            <Menu
              isOpen={isMenuOpen(menuPosition)}
              position={menuPosition as MenuPosition}
              onClose={() => setMenuOpen(menuPosition)}
              trigger={
                <IconButton
                  a11yLabel="More actions"
                  onPress={() => setMenuOpen(menuPosition)}>
                  <Icons.MoreIcon />
                </IconButton>
              }>
              {menuItems.map(item =>
                renderMenuItem(menuPosition as MenuPosition, item),
              )}
            </Menu>
          </View>
        </Section>
      </Page>
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {renderMenu('bottomRight', menus.bottomRight)}
        {renderMenu('bottomLeft', menus.bottomLeft)}
      </View>
      <View style={styles.content}>
        {renderMenu('topRight', menus.topRight)}
        {renderMenu('topLeft', menus.topLeft)}
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.gray[20],
  },
  content: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

export {MenuOverview};
