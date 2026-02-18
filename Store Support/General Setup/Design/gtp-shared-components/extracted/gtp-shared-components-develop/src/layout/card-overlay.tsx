import * as React from 'react';
import {
  Modal,
  ModalBaseProps,
  SafeAreaView,
  StyleProp,
  TouchableOpacity,
  ViewStyle,
} from 'react-native';

import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import SolidCard, {SolidCardExternalProps} from './solid-card';
import {composed as defaultTheme} from './theme';

export type CardOverlayProps = ModalBaseProps &
  Partial<Omit<SolidCardExternalProps, 'type'>> & {
    /** @deprecated, use cardStyle instead */
    style?: StyleProp<ViewStyle>;
    /** extra styling for the Card */
    cardStyle?: StyleProp<ViewStyle>;
    /** Whether to darken the background of the overlay */
    darken?: boolean;
  };

/**
 * @deprecated use Modal instead
 */
export default class CardOverlay extends React.Component<CardOverlayProps> {
  static contextTypes = ThemeContext;
  render() {
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      'cardOverlay',
      this.props.darken ? 'darken' : 'default',
    );
    const {
      children,
      style,
      cardStyle,
      color = 'white',
      elevation = 0,
      contentInset = 'normal',
      roundness = 'small',
      onRequestClose = () => {},
      ...rest
    } = this.props;
    return (
      <>
        <Modal {...rest} transparent>
          <SafeAreaView style={theme.part('container')}>
            <TouchableOpacity
              onPress={onRequestClose}
              style={theme.part('container')}>
              <SolidCard
                {...{color, elevation, contentInset, roundness}}
                style={[theme.part('content'), style, cardStyle]}>
                {/* ensure that a tap inside the Card does not trigger a dismiss */}
                <TouchableOpacity activeOpacity={1}>
                  {children}
                </TouchableOpacity>
              </SolidCard>
            </TouchableOpacity>
          </SafeAreaView>
        </Modal>
      </>
    );
  }
}
