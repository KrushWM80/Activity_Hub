import * as React from 'react';
import {
  FlexAlignType,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
} from 'react-native';

import * as token from '@livingdesign/tokens/dist/react-native/light/regular/components/List';

import type {CommonViewProps} from '../types/ComponentTypes';

import {
  _LeadingTrailing as _Leading,
  _LeadingTrailing as _Trailing,
} from './_LeadingTrailing';
import {Body, BodySize, BodyWeight} from './Body';

// ---------------
// Props
// ---------------

export type ListItemProps = CommonViewProps & {
  /**
   * The text label for the list item.
   */
  children: React.ReactNode;
  /**
   * The leading content for the list item.
   * Typically an icon.
   */
  leading?: React.ReactNode;
  /**
   * The title for the list item.
   */
  title?: React.ReactNode;
  /**
   * The trailing content for the list item.
   * Typically an IconButton or Button
   */
  trailing?: React.ReactElement;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  content?: React.ReactElement;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  leadingAlign?: FlexAlignType;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  trailingAlign?: FlexAlignType;
  /**
   * @deprecated it has no effect. Provided just for API backwards compatibility.
   */
  onPress?: () => void;
};

/**
 * ListItem's are composed of items containing text, icons, spot icons or images, and
 * they should contain at least one action.
 *
 * ## Usage
 * ```js
 * import {ListItem} from '@walmart/gtp-shared-components`;
 *
 * <ListItem>List Item</ListItem>
 * <ListItem leading={<Icon name="icon-name" />}>List Item with Icon</ListItem>
 * <ListItem title="Title">List Item with Title</ListItem>
 * <ListItem title="Title" leading={<Icon name="icon-name" />}>
 *  List Item with Title and Icon
 * </ListItem>
 * ```
 */
const ListItem: React.FC<ListItemProps> = (props) => {
  const {
    children,
    leading,
    title,
    trailing,
    UNSAFE_style = {},
    ...rest
  } = props;

  // ---------------
  // Rendering
  // ---------------
  const renderLeading = (node: React.ReactNode) => (
    <_Leading
      node={node}
      iconProps={{
        UNSAFE_style: ss.leadingContainer,
        testID: ListItem.displayName + '-leading',
      }}
    />
  );

  const renderTitle = () => {
    return title ? (
      <Body
        testID={ListItem.displayName + '-title'}
        size={token.componentListItemTitleAliasOptionsSize as BodySize}
        weight={
          `${token.componentListItemTitleAliasOptionsWeight}` as BodyWeight
        }>
        {title}
      </Body>
    ) : null;
  };

  const renderTrailing = (node: React.ReactNode) => (
    <View
      style={ss.trailingContainer}
      testID={ListItem.displayName + '-trailing'}>
      <_Trailing
        node={node}
        iconProps={{
          UNSAFE_style: ss.trailingContent,
          testID: ListItem.displayName + '-trailing-content',
        }}
      />
    </View>
  );

  const renderChildren = () => {
    return typeof children === 'string' ? (
      <Body
        testID={ListItem.displayName + '-content'}
        size={token.componentListItemTextLabelAliasOptionsSize as BodySize}>
        {children}
      </Body>
    ) : (
      <>{children}</>
    );
  };

  return (
    <View
      testID={ListItem.displayName}
      style={[ss.container, UNSAFE_style]}
      {...rest}>
      {leading ? renderLeading(leading) : null}
      <View style={ss.contentContainer}>
        {renderTitle()}
        {renderChildren()}
      </View>
      {trailing ? renderTrailing(trailing) : null}
    </View>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: token.componentListItemContainerBackgroundColor,
    paddingHorizontal: token.componentListSeparatorPaddingHorizontal,
    paddingVertical: token.componentListSeparatorPaddingVertical,
  },
  leadingContainer: {
    marginRight: token.componentListItemLeadingMarginEnd,
  },
  contentContainer: {
    flex: 1,
  },
  trailingContainer: {
    justifyContent: 'center',
    alignItems: 'flex-end',
    marginLeft: token.componentListItemTrailingMarginStart,
  },
  trailingContent: {
    maxWidth: 100,
  },
});

ListItem.displayName = 'ListItem';
export {ListItem};
