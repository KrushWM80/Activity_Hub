import * as React from 'react';
import {GestureResponderEvent, ScrollView, View, ViewProps} from 'react-native';

import LinkButton, {LinkProps} from '../../buttons/link-button';
import {Body} from '../../next/components/Body';
import {Caption} from '../../next/components/Caption';
import {
  getThemeFrom,
  ThemeContext,
  ThemeObject,
} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

import CarouselItem, {CarouselItemExternalProps} from './item';

type HeaderProps = {
  /** Header title text */
  title: string;
  /** Header link text */
  link?: string;
  /** Header subtitle text */
  subtitle?: string;
} & LinkProps;

type FooterProps = {
  /** Footer total */
  total?: number;
  /** Footer button */
  button: React.ReactNode;
} & LinkProps;

export type CarouselProps = ViewProps & {
  /** This Carousel's add button press event handler.  If set, will display an add button on each item. */
  onAddPress?: (event: {
    id: string | number;
    index: number;
    event: GestureResponderEvent;
  }) => void;
  /** This Carousel's item press event handler */
  onItemPress: (event: {
    id: string | number;
    index: number;
    event: GestureResponderEvent;
  }) => void;
  /** Whether to use the `small` variant */
  small?: boolean;
  /** Header information */
  header?: HeaderProps;
  /** Footer information */
  footer?: FooterProps;
  /** List of all items in the carousel */
  items: Array<CarouselItemExternalProps>;
};

const Header = ({
  title,
  link,
  onLinkPress,
  subtitle,
  theme,
}: HeaderProps & {theme: ThemeObject}) => (
  <View style={theme.part('header')}>
    <View style={theme.part('headerTitleContainer')}>
      <Body UNSAFE_style={theme.part('headerTitle')}>{title}</Body>
      {subtitle && (
        <Caption UNSAFE_style={theme.part('headerSubtitle')}>
          {subtitle}
        </Caption>
      )}
    </View>
    {link && onLinkPress && (
      <LinkButton small onPress={onLinkPress}>
        <Body
          UNSAFE_style={theme.part('headerLink')}
          numberOfLines={1}
          inheritColor>
          {link}
        </Body>
      </LinkButton>
    )}
  </View>
);

const Footer = ({
  total,
  link,
  onLinkPress,
  button,
  theme,
}: FooterProps & {theme: ThemeObject}) => (
  <View style={theme.part('footer')}>
    {total && (
      <>
        <Body UNSAFE_style={theme.part('footerCaption')}>Total</Body>
        <Body UNSAFE_style={theme.part('footerTotal')}>
          ${total.toFixed(2)}
        </Body>
      </>
    )}
    {link && onLinkPress && (
      <LinkButton small onPress={onLinkPress}>
        <Body
          UNSAFE_style={theme.part('footerLink')}
          numberOfLines={1}
          inheritColor>
          {link}
        </Body>
      </LinkButton>
    )}
    <View style={theme.part('footerButton')}>{button}</View>
  </View>
);

/**
 * @deprecated This not in the LD specs and will be removed in a future release
 */
export default class Carousel extends React.Component<CarouselProps> {
  static contextTypes = ThemeContext;
  render() {
    const {
      small,
      header,
      footer,
      items,
      onAddPress,
      onItemPress,
      style,
      ...rootProps
    } = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      'carousel',
      small ? 'small' : 'default',
    );

    const showFlag = items.some((item) => item.flag);
    const showWeightLabel = items.some((item) => item.weightLabel);

    return (
      <View {...rootProps} style={[theme.part('container'), style]}>
        {header && <Header {...header} theme={theme} />}
        <ScrollView horizontal contentContainerStyle={theme.part('items')}>
          {items.map((item, index) => (
            <CarouselItem
              key={item.id}
              small={small}
              showWeightLabel={showWeightLabel}
              showFlagArea={showFlag}
              {...item}
              onItemPress={(event) => onItemPress({id: item.id, index, event})}
              onAddPress={
                onAddPress
                  ? (event) => onAddPress({id: item.id, index, event})
                  : undefined
              }
            />
          ))}
        </ScrollView>
        {footer && <Footer {...footer} theme={theme} />}
      </View>
    );
  }
}
