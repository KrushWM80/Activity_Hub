import * as React from 'react';
import {
  Modal,
  ModalBaseProps,
  SafeAreaView,
  TouchableOpacity,
  View,
} from 'react-native';

import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import {composed as defaultTheme} from './theme';

export type OverlayProps = ModalBaseProps & {
  /** Whether to darken the background of the overlay */
  darken?: boolean;
  /** Whether to darken the background as a modal*/
  isModal?: boolean;
  children?: React.ReactNode;
};

/**
 * @deprecated use Modal instead
 */
export default class Overlay extends React.Component<OverlayProps> {
  static contextTypes = ThemeContext;
  render() {
    let overlayType = 'default';
    if (this.props.darken) {
      overlayType = this.props.isModal ? 'darkenModal' : 'darken';
    }
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      'overlay',
      overlayType,
    );
    const {children, ...props} = this.props;
    return (
      <Modal {...props} transparent>
        <SafeAreaView style={theme.part('container')}>
          <TouchableOpacity
            activeOpacity={1}
            style={theme.part('closer')}
            onPress={this.props.onRequestClose}
          />
          <View style={theme.part('content')}>{children}</View>
        </SafeAreaView>
      </Modal>
    );
  }
}
