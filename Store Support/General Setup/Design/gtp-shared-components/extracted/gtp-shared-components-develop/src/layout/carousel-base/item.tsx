import * as React from 'react';
import {
  GestureResponderEvent,
  TouchableOpacity,
  View,
  ViewProps,
} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import LinkButton, {LinkProps} from '../../buttons/link-button';
import {AvailabilityBadge, MediaBadge} from '../../flags';
import Ratings, {RatingsProps} from '../../indicators/ratings';
import {Body} from '../../next/components/Body';
import {Caption} from '../../next/components/Caption';
import {IconButton} from '../../next/components/IconButton';
import {colors} from '../../next/utils';
import {getThemeFrom, ThemeContext} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

import ProductImage from './image';

export type CarouselItemExternalProps = ViewProps & {
  /** Unique ID for this item */
  id: string | number;
  /** Flag component to show on this item */
  flag?: React.ReactNode;
  /** Product image URI */
  imageSource: string;
  /** Product price */
  price: number;
  /** Product was price.  Not displayed on the `small` variant. */
  wasPrice?: number;
  /** Product each price.  Not displayed on the `small` variant. */
  eachPrice?: number;
  /** Product each price label.  Not displayed on the `small` variant. */
  weightLabel?: boolean;
  /** Product name */
  name: string;
  /** Whether this product is out of stock */
  outOfStock?: boolean;
  /** Product ratings information */
  ratings?: RatingsProps;
  /** Media badge text to show on this item */
  mediaBadge?: string;
  /** Availability badge text to show on this item */
  availabilityBadge?: string;
} & LinkProps;

export type CarouselItemProps = CarouselItemExternalProps & {
  small?: boolean;
  showFlagArea?: boolean;
  showWeightLabel?: boolean;
  onAddPress?: (event: GestureResponderEvent) => void;
  onItemPress: (event: GestureResponderEvent) => void;
};

export default class CarouselItem extends React.Component<CarouselItemProps> {
  static contextTypes = ThemeContext;

  render() {
    const {
      small,
      flag,
      showFlagArea,
      imageSource,
      onAddPress,
      onItemPress,
      price,
      wasPrice,
      eachPrice,
      weightLabel,
      name,
      outOfStock,
      ratings,
      mediaBadge,
      availabilityBadge,
      link,
      onLinkPress,
      style,
      ...rootProps
    } = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      'carouselItem',
      small ? 'small' : 'default',
    );

    return (
      <TouchableOpacity
        {...rootProps}
        style={[theme.part('container'), style]}
        activeOpacity={1}
        onPress={onItemPress}>
        {!small && showFlagArea && (
          <View style={theme.part('flag')}>{flag ? flag : null}</View>
        )}
        <View style={theme.part('imageContainer')}>
          <ProductImage
            source={imageSource}
            style={theme.part('image')}
            size={theme.part('imageSize')}
          />
          {onAddPress && (
            <IconButton
              children={<Icons.PlusIcon />}
              onPress={onAddPress}
              UNSAFE_style={[
                theme.part('addButton'),
                {backgroundColor: colors.blue['100']},
              ]}
              size="small"
              color={colors.white}
            />
          )}
        </View>
        <Body>
          <Body UNSAFE_style={theme.part('price')}>${price.toFixed(2)}</Body>
          {!small && wasPrice && (
            <>
              {' '}
              <Caption UNSAFE_style={theme.part('wasPrice')}>
                ${wasPrice.toFixed(2)}
              </Caption>
            </>
          )}
          {!small && eachPrice && (
            <>
              {' '}
              <Caption UNSAFE_style={theme.part('eachPrice')}>
                ${eachPrice.toFixed(2)}
              </Caption>
            </>
          )}
        </Body>
        {!small && weightLabel && (
          <Caption UNSAFE_style={theme.part('weightLabel')}>
            Final cost by weight
          </Caption>
        )}
        <Body UNSAFE_style={theme.part('name')} numberOfLines={2}>
          {name}
        </Body>
        {!small && ratings && (
          <Ratings style={theme.part('ratings')} {...ratings} />
        )}
        {!small && outOfStock && (
          <Caption UNSAFE_style={theme.part('stock')}>Out of stock</Caption>
        )}
        {!small && availabilityBadge && (
          <AvailabilityBadge style={theme.part('badge')}>
            {availabilityBadge}
          </AvailabilityBadge>
        )}
        {!small && mediaBadge && (
          <MediaBadge style={theme.part('badge')}>{mediaBadge}</MediaBadge>
        )}
        {!small && link && onLinkPress && (
          <LinkButton
            small
            onPress={onLinkPress}
            style={theme.part('linkContainer')}>
            <Body
              UNSAFE_style={theme.part('link')}
              numberOfLines={1}
              inheritColor>
              {link}
            </Body>
          </LinkButton>
        )}
      </TouchableOpacity>
    );
  }
}
