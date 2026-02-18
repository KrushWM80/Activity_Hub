import * as React from 'react';
import {
  FlatList,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
  ViewToken,
} from 'react-native';

import flattenChildren from 'react-keyed-flatten-children';

import type {CommonViewProps} from '../../next/types/ComponentTypes';
import {usePrevious} from '../../next/utils';
import {colors} from '../../next/utils/colors';

// ---------------
// Props
// ---------------
export type FilterGroupProps = CommonViewProps & {
  /**
   * The children to render within the filter group.  These are typically `FilterToggle`, `FilterTriggerSingle`,
   * `FilterTriggerAll`, or `FilterTag` components.
   */
  children?: React.ReactNode;
  /**
   * If the filter group should wrap its children or show inline and scroll horizontally.
   * @default false
   */
  wrapping?: boolean;
  /**
   * If provided, the `style` to provide to the root element. @note This property is prefixed with
   * `UNSAFE` as its use often results in unintended side effects.
   */
  UNSAFE_style?: StyleProp<ViewStyle>;
};

/**
 * These are used in conjunction with other components, designers and engineers should use these over atoms,
 * unless a variant needs to be created for a specific purpose.
 *
 * ## Usage
 * ```js
 * import {FilterGroup, FilterTriggerAll, FilterTriggerSingle, FilterToggle, FilterTag} from '@walmart/gtp-shared-components/ax`;
 *
 * <FilterGroup>
 *   <FilterTriggerAll />
 *   <FilterTriggerSingle>Trigger Single</FilterTriggerSingle>
 *   <FilterToggle>Toggle</FilterToggle>
 *   <FilterTag>Tag</FilterTag>
 * </FilterGroup>
 * ```
 */
const FilterGroup: React.FC<FilterGroupProps> = (props) => {
  const {children, wrapping = false, UNSAFE_style} = props;
  const kids = flattenChildren(children);
  const flatListRef = React.useRef<FlatList>(null);
  const previousKidsLength = usePrevious(kids.length);
  const filterRefs = React.useRef<Array<View | null>>([]);
  const [viewableFilters, setViewableFilters] = React.useState<
    Array<ViewToken>
  >([]);
  const viewPortWidth = React.useRef<number>(0);

  // If the filter group is not wrapping and a filter is pressed while not fully visible, scroll to it
  // Or else call the original onPress
  const onFilterPress = (index: number, originalOnPress: any) => {
    // Is the filter in viewableFilters and fully visible?
    const viewItem = viewableFilters.find((item) => item.index === index);
    // If it is, call the original onPress
    if (viewItem) {
      if (originalOnPress) {
        originalOnPress?.();
      }
    } else {
      // Get the index of the first item in viewItems
      const lowerBoundIndex = viewableFilters[0]?.index;
      if (lowerBoundIndex && index < lowerBoundIndex) {
        // Scroll to the left
        flatListRef?.current?.scrollToIndex({
          index: index,
          viewPosition: 0.02, // Give a little buffer (0.02) so the filter is fully visible
        });
      } else {
        // Scroll to the right
        flatListRef?.current?.scrollToIndex({
          index: index,
          viewPosition: 0.98, // Give a little buffer (0.02) so the filter is fully visible
        });
      }
    }
  };

  // renderFilterItem is called for each child of the filter group
  const renderFilterItem = ({
    item,
    index,
  }: {
    item: React.ReactNode;
    index: number;
  }) => {
    return (
      <View
        ref={(ref) => (filterRefs.current[index] = ref)}
        style={[ss.filterContainer]}>
        {
          // @ts-ignore
          React.cloneElement(item, {
            // @ts-ignore
            onPress: () => onFilterPress(index, item?.props?.onPress),
          })
        }
      </View>
    );
  };

  // Scroll to end if in wrapping mode and the number of children has increased
  const scrollToEnd = () => {
    if (
      !wrapping &&
      flatListRef.current &&
      previousKidsLength &&
      kids.length > previousKidsLength
    ) {
      // Wait for the new filter to render animation before scrolling
      setTimeout(() => flatListRef?.current?.scrollToEnd(), 250);
    }
  };

  // An item is considered viewable if 95% of it is visible
  const viewabilityConfig = {
    itemVisiblePercentThreshold: 95,
  };

  // When the viewable items change, update the viewableFilters state
  const onViewableItemsChanged = ({
    viewableItems,
  }: {
    viewableItems: ViewToken[];
  }) => {
    setViewableFilters(viewableItems);
  };

  // Fixes "Changing onViewableItemsChanged on the fly is not supported" error when hot reloading
  // by using a ref to store the viewabilityConfig and onViewableItemsChanged:
  // https://github.com/facebook/react-native/issues/30171#issuecomment-820833606
  const handleViewableItemsChanged = React.useRef([
    {viewabilityConfig, onViewableItemsChanged},
  ]);

  // ---------------
  // Rendering
  // ---------------
  return wrapping ? (
    <View
      testID={FilterGroup.displayName}
      style={[ss.wrapContainer, UNSAFE_style]}>
      {React.Children.map(kids, (kid: React.ReactNode) => (
        <View style={[ss.filterContainer]}>
          {
            // @ts-ignore
            React.cloneElement(kid)
          }
        </View>
      ))}
    </View>
  ) : (
    <FlatList
      testID={FilterGroup.displayName}
      ref={flatListRef}
      horizontal
      data={kids}
      onLayout={(e) => {
        viewPortWidth.current = e.nativeEvent.layout.width;
      }}
      onContentSizeChange={scrollToEnd}
      viewabilityConfigCallbackPairs={handleViewableItemsChanged.current}
      showsHorizontalScrollIndicator={false}
      style={[ss.listContainer, UNSAFE_style]}
      contentContainerStyle={[ss.contentContainer]}
      renderItem={renderFilterItem}
      ListFooterComponent={<View style={ss.listFooter} />}
    />
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  wrapContainer: {
    width: '100%',
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'flex-start',
    alignItems: 'flex-start',
    backgroundColor: colors.white,
    borderBottomWidth: 1,
    borderColor: colors.gray['20'], // '#E3E4E5',
    padding: 16,
    columnGap: 12, // Gap is supported in React Native 0.71+
  },
  listContainer: {
    width: '100%',
    backgroundColor: colors.white,
    height: 65,
    flexGrow: 0,
    flexShrink: 0,
    borderBottomWidth: 1,
    borderColor: colors.gray['20'], // '#E3E4E5',
  },
  contentContainer: {
    alignItems: 'center',
    paddingLeft: 16,
    columnGap: 12, // Gap is supported in React Native 0.71+
  },
  listFooter: {
    // Use an empty list footer for RN bug workaround: "FlatList scrollToEnd ignores contentContainerStyle bottom padding"
    // https://github.com/facebook/react-native/issues/26246#issuecomment-526098893
    width: 8,
  },
  filterContainer: {
    overflow: 'hidden', // so slide-in animations don't overlap with each other
  },
});

FilterGroup.displayName = 'FilterGroup';
export {FilterGroup};
