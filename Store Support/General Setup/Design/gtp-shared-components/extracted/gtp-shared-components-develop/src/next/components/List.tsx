import * as React from 'react';
import {ScrollView, StyleProp, ViewStyle} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/List';

import {CommonScrollViewProps} from '../types/ComponentTypes';

import {_Gap} from './_Gap';

// ---------------
// Props
// ---------------
export type ListProps = CommonScrollViewProps & {
  /**
   * The content for the list.
   * It is marked as optional for backwards compatibility only
   */
  children?: React.ReactNode;
  /**
   * 	If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * Whether to show the separator
   * between rows
   * @default true
   */
  separator?: boolean;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  items?: Array<any>;
};

/**
 * Lists are a continuous, vertical group of related information.
 *
 * ## Usage
 * ```js
 * import {List, ListItem} from '@walmart/gtp-shared-components`;
 *
 * <List>
 *   <ListItem>Item 1</ListItem>
 *   <ListItem>Item 2</ListItem>
 * </List>
 * ```
 */
const List: React.FC<ListProps> = (props) => {
  const {children, UNSAFE_style, separator = true, ...rest} = props;

  // ---------------
  // Rendering
  // ---------------
  return (
    <ScrollView
      testID={List.displayName}
      showsVerticalScrollIndicator={false}
      style={UNSAFE_style}
      {...rest}>
      <_Gap
        gap={token.componentListSeparatorPaddingVertical}
        direction={'vertical'}
        showSeparator={separator}>
        {children}
      </_Gap>
    </ScrollView>
  );
};

List.displayName = 'List';
export {List};
