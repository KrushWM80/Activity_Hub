import * as React from 'react';
import {LayoutChangeEvent, ScrollView, View, ViewStyle} from 'react-native';

import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import Tab, {TabExternalProps} from './tab';
import {composed as defaultTheme} from './theme';

export type TabsProps = {
  style: ViewStyle;
  /** This Tabs' tab select handler */
  onSelect: (index: number) => void;
  /** List of all tabs */
  tabs: Array<TabExternalProps>;
  /** Whether to size the tabs based on their content */
  proportional: boolean;
  /** Index of the selected tab */
  selectedIndex: number;
  /** Width of the tab selected indicator */
  selectedIndicatorWidth?: number;
  /** Children */
  children: React.ReactNode;
};

type TabsState = {
  totalWidth: number;
  availableWidth: number;
};

/**
 * @deprecated use TabNavigation instead
 */
export default class Tabs extends React.Component<TabsProps, TabsState> {
  static contextTypes = ThemeContext;
  state: TabsState = {
    totalWidth: 0,
    availableWidth: 0,
  };
  static defaultProps: Partial<TabsProps> = {
    proportional: false,
    selectedIndicatorWidth: 3,
    tabs: [],
  };
  _measurements: Array<number>;

  constructor(props: TabsProps) {
    super(props);
    this._measurements = Array.from(new Array(props.tabs.length)).map(() => 0);
  }

  componentDidUpdate(prevProps: TabsProps) {
    if (this.props.tabs !== prevProps.tabs) {
      this._measurements = Array.from(new Array(prevProps.tabs.length)).map(
        () => 0,
      );
      this.setState({totalWidth: 0});
    }
  }

  handlePress = (index: number) => {
    const {onSelect} = this.props;
    if (onSelect) {
      onSelect(index);
    }
  };

  handleTabsLayout = (event: LayoutChangeEvent) => {
    const {
      nativeEvent: {
        layout: {width},
      },
    } = event;
    this.setState({availableWidth: width});
  };

  handleTabLayout = (event: LayoutChangeEvent, index: number) => {
    if (!this._measurements[index]) {
      const {
        nativeEvent: {
          layout: {width},
        },
      } = event;
      this._measurements[index] = width;

      if (this._measurements.filter((value: number) => !value).length === 0) {
        this.setState({
          totalWidth: this._measurements.reduce(
            (a: number, b: number) => a + b,
            0,
          ),
        });
      }
    }
  };

  render() {
    /* eslint-disable react-native/no-inline-styles */
    const {
      children,
      style,
      tabs,
      proportional,
      selectedIndicatorWidth,
      onSelect,
      selectedIndex,
      ...rootProps
    } = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'navigation',
      'tabs',
    );
    const {totalWidth, availableWidth} = this.state;
    const calculated = !!totalWidth && !!availableWidth;
    const containerStyle = calculated &&
      totalWidth <= availableWidth && {flex: 1};
    return (
      <View
        accessibilityRole="tablist"
        style={[
          style,
          theme.part('static.container'),
          containerStyle,
          !calculated && {opacity: 0},
        ]}
        {...rootProps}
        onLayout={this.handleTabsLayout}>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          showsVerticalScrollIndicator={false}
          directionalLockEnabled
          bounces={false}
          scrollsToTop={false}
          scrollEnabled={calculated && totalWidth > availableWidth}
          contentContainerStyle={containerStyle}>
          <View style={[{flexDirection: 'row'}, containerStyle]}>
            {/* {tabs.map((tab, index) => {
              let calculatedStyle = {}
              if (calculated && totalWidth <= availableWidth) {
                calculatedStyle = proportional
                  ? { width: (this._measurements[index] / totalWidth) * availableWidth }
                  : { flex: 1 }
              }
              return React.cloneElement(tab, {
                style: mergeStyles(tab.props.style, calculatedStyle),
                onLayout: (event: LayoutChangeEvent) => this.handleTabLayout(event, index),
                onPress: () => this.handlePress(index),
                selected: index === this.props.selectedIndex,
                key: `Tab_${index}`,
                indicatorWidth: selectedIndicatorWidth,
              } as Partial<FullTabProps>)
            })} */}
            {tabs &&
              tabs.map((tab, i) => {
                const {style: tabStyle, ...rest} = tab;
                let calculatedStyle = {};
                if (calculated && totalWidth <= availableWidth) {
                  calculatedStyle = proportional
                    ? {
                        width:
                          (this._measurements[i] / totalWidth) * availableWidth,
                      }
                    : {flex: 1};
                }

                return (
                  <Tab
                    onLayout={(event: LayoutChangeEvent) => {
                      this.handleTabLayout(event, i);
                    }}
                    {...rest}
                    onPress={() => {
                      this.handlePress(i);
                    }}
                    selected={i === this.props.selectedIndex}
                    key={`Tab_${i}`}
                    style={[tabStyle, calculatedStyle]}
                    indicatorWidth={selectedIndicatorWidth}
                  />
                );
              })}
          </View>
        </ScrollView>
      </View>
    );
  }
}
