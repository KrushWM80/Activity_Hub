import * as React from 'react';
import {
  GestureResponderEvent,
  StyleSheet,
  TouchableOpacityProps,
  View,
  ViewProps,
} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import {LinkButton} from '../buttons';
import BaseButton, {ButtonTheme} from '../buttons/base/button';
import {Body} from '../next/components/Body';
import {colors} from '../next/utils';
import {getThemeFrom, ThemeContext, ThemeObject} from '../theme/theme-provider';

import {composed as defaultTheme} from './theme';

type SnackbarActionButtonProps = TouchableOpacityProps & {
  /** Button caption */
  caption: string;
  /** This Button's press event handler */
  onPress: (event: GestureResponderEvent) => void;
};

type SnackbarCloseButtonProps = TouchableOpacityProps & {
  onPress: (event: GestureResponderEvent) => void;
};

export type SnackbarProps = ViewProps & {
  children: string | React.ReactNode;

  /** Button to show on the Snackbar
   * @deprecated use actionButton instead
   */
  button?: SnackbarActionButtonProps;

  /** ActionButton to show on the Snackbar */
  actionButton?: SnackbarActionButtonProps;

  /** Close Button (transparent icon X) to show on the Snackbar */
  closeButton?: SnackbarCloseButtonProps;
};

/**
 * @deprecated use useSnackbar hook instead
 */
export default class Snackbar extends React.Component<SnackbarProps> {
  static contextTypes = ThemeContext;
  static displayName = 'Snackbar';

  renderActionButton(theme: ThemeObject) {
    if (this.props.button) {
      const {caption, disabled, ...rest} = this.props.button;
      return (
        <LinkButton
          disabled={!!disabled}
          white
          small
          {...rest}
          style={theme.part('static.button')}
          textProps={{numberOfLines: 1}}
          hitSlop={theme.part('static.hitSlop')}>
          {caption}
        </LinkButton>
      );
    }
    if (this.props.actionButton) {
      const {caption, disabled, ...rest} = this.props.actionButton;
      return (
        <LinkButton
          disabled={!!disabled}
          white
          small
          {...rest}
          style={theme.part('static.button')}
          textProps={{numberOfLines: 1}}
          hitSlop={theme.part('static.hitSlop')}>
          {caption}
        </LinkButton>
      );
    }
    return null;
  }

  renderCloseButton(theme: ThemeObject) {
    if (this.props.closeButton) {
      return (
        <BaseButton
          theme={theme as ButtonTheme}
          style={styles.closeButton}
          icon={<Icons.CloseIcon color={colors.white} />}
          onPress={this.props.closeButton.onPress}
        />
      );
    }
  }

  render() {
    const {children, style, button, ...rootProps} = this.props;

    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'messaging',
      'snackbar',
    );

    return (
      <View {...rootProps} style={[theme.part('static.container'), style]}>
        <Body UNSAFE_style={theme.part('static.text')}>{children}</Body>
        {this.renderActionButton(theme)}
        {this.renderCloseButton(theme)}
      </View>
    );
  }
}

const styles = StyleSheet.create({
  closeButton: {
    paddingRight: 4,
  },
});
