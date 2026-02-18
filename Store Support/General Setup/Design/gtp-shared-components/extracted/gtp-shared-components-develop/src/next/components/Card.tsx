import * as React from 'react';
import {Platform, StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/Card';

import type {CommonViewProps} from '../types/ComponentTypes';
import {colors} from '../utils';

export type CardSize = 'large' | 'small';

const cardContext = {
  cardSize: 'small' as CardSize,
};

// ---------------
// Props
// ---------------
export type CardProps = CommonViewProps & {
  /**
   * The content for the card.
   */
  children: React.ReactNode;
  /**
   * This is the description for prop size
   * @default small
   */
  size?: CardSize;
  /**
   * If provided, the `style` to provide to the root element.
   * @note This property is prefixed with `UNSAFE` as its use often
   * results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Cards organize and present similar content that users can scan
 * quickly and interact with. They always show relevant content and
 * actionable information. They contain text, images, icons and buttons
 * placed with hierarchy, and may be placed as a series or feed of similar content.
 *
 * ## Usage
 * ```js
 * import * as React from 'react';
 * import {Image, Text} from 'react-native';
 * import {Heading, Icons, Card, CardHeader, CardMedia, CardContent, CardActions, Button, ButtonGroup} from '@walmart/gtp-shared-components';
 * const Spacer = () => <View style={{height: 8}} />;
 *
 * <>
 *   {['small', 'large'].map(size => {
 *     return (
 *       <React.Fragment key={size}>
 *           <Heading size="large">{`Card size="${size}"`}</Heading>
 *           <Spacer />
 *           <Card size={size}>
 *             <CardMedia>
 *               <Image
 *                 source={{
 *                   uri: 'https://placekitten.com/g/200/200',
 *                   height: 300,
 *                   width: '100%',
 *                 }}
 *               />
 *             </CardMedia>
 *             <CardHeader
 *               leadingIcon={<Icons.SparkIcon size={32} />}
 *               title="Welcome"
 *               trailing={
 *                 <Button
 *                   variant="tertiary"
 *                   onPress={() => {}}>
 *                   Start Here
 *                 </Button>
 *               }
 *             />
 *             <CardContent>
 *               <Text>Lorem ipsum dolor sit amet.</Text>
 *             </CardContent>
 *             <CardActions>
 *               <ButtonGroup>
 *                 <Button
 *                   variant="tertiary"
 *                   onPress={() => {}}>
 *                   Action1
 *                 </Button>
 *                 <Button
 *                   variant="primary"
 *                   onPress={() => {}}>
 *                   Action2
 *                 </Button>
 *               </ButtonGroup>
 *             </CardActions>
 *           </Card>
 *           <Spacer />
 *       </React.Fragment>
 *     );
 *   })}
 *
 * </>;
 *
 * ```
 */
const Card: React.FC<CardProps> = (props) => {
  const {children, size = 'small', UNSAFE_style = {}} = props;

  // ---------------
  // Rendering
  // ---------------
  return (
    <CardContext.Provider value={{cardSize: size}}>
      <View testID={Card.displayName} style={[ss().container, UNSAFE_style]}>
        {children}
      </View>
    </CardContext.Provider>
  );
};

// ---------------
// Styles
// ---------------
const ss = () => {
  const blurRadius = parseInt(
    token.componentCardContainerElevation[0].blurRadius, // 2px
    10,
  );
  const offsetY = parseInt(
    token.componentCardContainerElevation[0].offsetY, // 1px
    10,
  );
  const offsetX = parseInt(
    `${token.componentCardContainerElevation[0].offsetX}`,
    10,
  ); // 0

  return StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: token.componentCardContainerBackgroundColor,
      borderRadius: token.componentCardContainerBorderRadius,
      ...Platform.select({
        android: {
          elevation: blurRadius,
        },
        ios: {
          shadowColor: colors.black,
          shadowOpacity: 0.15,
          shadowRadius: blurRadius,
          shadowOffset: {
            height: offsetY,
            width: offsetX,
          },
        },
      }),
    },
  });
};
Card.displayName = 'Card';

const CardContext = React.createContext<typeof cardContext>(cardContext);
CardContext.displayName = 'CardContext';

export {Card, CardContext};
