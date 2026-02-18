import * as React from 'react';
import {ScrollView, StyleProp, StyleSheet, View, ViewStyle} from 'react-native';

import flattenChildren from 'react-keyed-flatten-children';

import type {CommonViewProps} from '../types/ComponentTypes';

// ---------------
// Props
// ---------------

export type DataTableProps = CommonViewProps & {
  /**
   * The content for the data table.
   */
  children: React.ReactNode;
  /**
   * Horizontal scroll for the Data Table.
   * @default false
   */
  horizontalScroll?: boolean;
  /**
   * If provided, the <strong>style</strong> to provide to the container.
   * This property is prefixed with <strong>UNSAFE</strong> as its use
   * often results in <strong>unintended side effects</strong>.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * Data Table displays a set of related information in rows and columns.
 *
 * ## Usage
 * ```js
 * import {Body, DataTable} from '@walmart/gtp-shared-components`;
 *
 * <DataTable>
 *   <DataTableHead>
 *     <DataTableRow>
 *       <DataTableHeader>ID</DataTableHeader>
 *       <DataTableHeader>Name</DataTableHeader>
 *     </DataTableRow>
 *   </DataTableHead>
 *   <DataTableBody>
 *     <Body>Lorem ipsum</Body>
 *   </DataTableBody>
 * </DataTable>
 * ```
 */
const DataTable: React.FC<DataTableProps> = (props: DataTableProps) => {
  const {children, UNSAFE_style, horizontalScroll = false, ...rest} = props;
  const [allowHorizontalScroll, setAllowHorizontalScroll] =
    React.useState(false);
  const kids = flattenChildren(children);

  React.useEffect(() => {
    const DTHeader = (kids[0] as React.ReactElement).props.children;
    const DTHeadersCount = React.Children.count(DTHeader.props.children);
    if (DTHeadersCount > 5) {
      setAllowHorizontalScroll(true);
    }
  }, [kids]);

  // ---------------
  // Rendering
  // ---------------
  const renderDataTable = () => {
    return (
      <View style={styles.innerContainer}>
        {kids.map((child, index) =>
          index === 0 ? (
            // index === 0 means putting DataTable Headers in non scrollable view, so that data body only can be scrollable
            <View {...rest} key={index}>
              {child}
            </View>
          ) : (
            <ScrollView
              key={index}
              bounces={false}
              accessibilityRole="tablist"
              scrollsToTop={false}
              nestedScrollEnabled={true}
              showsVerticalScrollIndicator={false}
              testID={DataTable.displayName}
              style={[styles.container, UNSAFE_style]}
              contentContainerStyle={styles.contentContainer}
              {...rest}>
              {child}
            </ScrollView>
          ),
        )}
      </View>
    );
  };

  return (
    <>
      {horizontalScroll || allowHorizontalScroll ? (
        <ScrollView
          horizontal
          stickyHeaderIndices={[0]}
          style={styles.container}
          showsHorizontalScrollIndicator={false}>
          {renderDataTable()}
        </ScrollView>
      ) : (
        renderDataTable()
      )}
    </>
  );
};

// ---------------
// StyleSheet
// ---------------
const styles = StyleSheet.create({
  container: {
    width: '100%',
  },
  contentContainer: {
    flexGrow: 1,
  },
  innerContainer: {
    flex: 1,
  },
});

DataTable.displayName = 'DataTable';
export {DataTable};
