import * as React from 'react';
import {
  Modal,
  ModalBaseProps,
  SafeAreaView,
  StyleProp,
  View,
  ViewStyle,
} from 'react-native';

import {Spinner, SpinnerColor} from '../next/components/Spinner';
import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import {composed as defaultTheme} from './theme';

export type SpinnerOverlayProps = ModalBaseProps & {
  style?: StyleProp<ViewStyle>;
  /**
   * Color for the foreground of the spinner
   * Valid values are 'white'|'gray'
   */
  spinnerColor?: SpinnerColor;
  /** Whether to darken the background of the overlay */
  darken?: boolean;
  children?: React.ReactNode;
};

/**
 * @deprecated not in the LD3 specs
 */
export default class SpinnerOverlay extends React.Component<SpinnerOverlayProps> {
  static contextTypes = ThemeContext;
  render() {
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      'spinnerOverlay',
      this.props.darken ? 'darken' : 'default',
    );
    const {children, style, spinnerColor, ...props} = this.props;
    return (
      <Modal {...props} transparent>
        <SafeAreaView style={[theme.part('container'), style]}>
          <View style={theme.part('content')}>
            <Spinner color={spinnerColor} />
            {children}
          </View>
        </SafeAreaView>
      </Modal>
    );
  }
}
