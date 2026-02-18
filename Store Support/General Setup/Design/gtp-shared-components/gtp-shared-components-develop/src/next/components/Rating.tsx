import * as React from 'react';
import {StyleProp, StyleSheet, View, ViewProps, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Rating';
import {Icons} from '@walmart/gtp-shared-icons';

import {iconSizes} from '../utils';

// ---------------
// Props
// ---------------
export type RatingSize = 'small' | 'large';
export type RatingProps = ViewProps & {
  /**
   * The size for the rating.
   * Valid values: 'small' | 'large'
   * @default small
   */
  size?: RatingSize;
  /**
   * The value for the rating.
   * @default 0
   */
  value?: number;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * The number of ratings.
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  count?: number;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  onPress?: () => void;
};

/**
 * Ratings provide insight into how well a product or service has been received by those who have bought or used it previously.
 *
 * ## Usage
 * ```js
 * import {Rating} from '@walmart/gtp-shared-components`;
 *
 * <Rating value={3.5} size={'large'} />
 * ```
 */
const Rating: React.FC<RatingProps> = (props) => {
  const {value = 0, size = 'small', UNSAFE_style = {}, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------

  const starIcon = (index: number) => {
    if (value >= index) {
      return Icons.StarFillIcon;
    } else if (value > index - 1) {
      return Icons.StarHalfIcon;
    }
    return Icons.StarIcon;
  };

  const resolveIconSize = (_size: RatingSize) => {
    if (_size === 'small') {
      return token.componentRatingIconSizeSmallHeight;
    } else {
      // return token.componentRatingIconSizeLargeHeight;token is 21 which is not supported by Icons, using 24 instead
      return iconSizes.medium;
    }
  };

  const _renderRatingStar = (_size: RatingSize) => {
    return Array.of(1, 2, 3, 4, 5).map((index) => {
      const StarIcon: React.ElementType = starIcon(index);
      return (
        <StarIcon
          key={`rating_${index}`}
          size={resolveIconSize(_size)}
          color={token.componentRatingIconVariantFilledBackgroundColor}
        />
      );
    });
  };

  return (
    <View
      testID={Rating.displayName}
      style={[ss.container, UNSAFE_style]}
      {...rest}>
      {_renderRatingStar(size)}
    </View>
  );
};

// ---------------
// Styles
// ---------------

const ss = StyleSheet.create({
  container: {
    flexDirection: 'row',
  },
});

Rating.displayName = 'Rating';
export {Rating};
