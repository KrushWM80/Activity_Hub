import * as React from 'react';
import {Appearance, StyleSheet, Text, useColorScheme, View} from 'react-native';
import {
  DarkTheme,
  DefaultTheme,
  NavigationContainer,
} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';

import {IconButton, LivingDesignProvider} from '@walmart/gtp-shared-components';

import {
  HomeScreen,

  // Foundation screens
  ColorsOverview,
  IconsOverview,
  TypographyOverview,

  // Component screens
  AlertOverview,
  BadgeOverview,
  BottomSheetOverview,
  ButtonGroupOverview,
  ButtonOverview,
  CardOverview,
  CalloutOverview,
  CheckboxOverview,
  ChipGroupOverview,
  ChipOverview,
  CircularProgressIndicatorOverview,
  CollapseOverview,
  DateDropdownOverview,
  DividerOverview,
  ErrorMessageOverview,
  FilterOverview,
  FilterGroupOverview,
  FormGroupOverview,
  FormsOverview,
  IconButtonOverview,
  IndicatorOverview,
  LayoutOverview,
  LinkOverview,
  ListOverview,
  MenuOverview,
  MessagingOverview,
  MetricOverview,
  ModalOverview,
  OverlayOverview,
  PopoverOverview,
  ProgressIndicatorOverview,
  ProgressTrackerOverview,
  RadioOverview,
  SeeDetailsOverview,
  SegmentedOverview,
  SelectOverview,
  SkeletonOverview,
  SnackbarOverview,
  SpinnerOverview,
  SpotIconOverview,
  StyledTextOverview,
  SwitchOverview,
  TabNavigationOverview,
  TagOverview,
  TextAreaOverview,
  TextFieldOverview,
  WizardFooterOverview,
  VariantsOverview,

  // Playground screens
  AlertPlayground,
  BadgePlayground,
  ButtonPlayground,
  CardPlayground,
  CheckboxPlayground,
  ChipGroupPlayground,
  ChipPlayground,
  CircularProgressIndicatorPlayground,
  CollapsePlayground,
  DateDropdownPlayground,
  DividerPlayground,
  FilterPlayground,
  FilterGroupPlayground,
  IconButtonPlayground,
  LinkPlayground,
  ListPlayground,
  MetricPlayground,
  ModalPlayground,
  ProgressIndicatorPlayground,
  ProgressTrackerPlayground,
  RadioPlayground,
  SeeDetailsPlayground,
  SkeletonPlayground,
  SpotIconPlayground,
  StyledTextPlayground,
  SwitchPlayground,
  TagPlayground,
  VariantsPlayground,

  // Recipe screens
  ModalRecipes,
  AlertRecipe,
  AlertTalkBackRecipe,
  BadgeRecipes,
  BottomSheetMultiTextInputsRecipe,
  BottomSheetTextInputKeyboardRecipe,
  BottomSheetWithScrollableContentRecipe,
  BottomSheetWithFlatListContentRecipe,
  BottomSheetWithCustomHeightContentRecipe,
  BottomSheetWithCustomActionsRecipe,
  BottomSheetWithExposedPropsRecipe,
  BottomSheetWithoutRNModalPropsRecipe,
  ButtonRecipes,
  CalloutRecipes,
  CardRecipes,
  CheckboxRecipes,
  ChipGroupRecipes,
  ChipRecipes,
  DataTableBulkActionsRecipe,
  DataTableCellActionsMenuRecipe,
  DataTableCellActionsRecipe,
  DataTableCheckboxRecipe,
  DataTableScrollRecipe,
  DataTableSortRecipe,
  DataTableStatusRecipe,
  DividerRecipes,
  ErrorMessageRecipes,
  FilterGroupRecipes,
  FormGroupCheckboxRecipe,
  FormGroupRadioRecipe,
  IconTintColorRecipe,
  ListRecipes,
  MetricRecipes,
  MetricGroupRecipes,
  PopoverRecipes,
  ProgressIndicatorRecipes,
  ProgressTrackerRecipes,
  SeeDetailsRecipes,
  SelectWithCustomTextRecipe,
  SelectWithExtraContentRecipe,
  SelectWithLocalStateUpdateRecipe,
  SelectWithLongListRecipe,
  SkeletonRecipes,
  SpinnerRecipes,
  SpotIconRecipes,
  StyledTextRecipes,
  SwitchRecipes,
  TabNavigationRecipes,
  TagRecipes,
  TextFieldAccessibilityRecipe,
  TextFieldRecipe,
  ToggleablesRecipe,
  VariantsRecipes,

  // Navigation drivers (these drive navigation to individual recipes)
  AlertRecipes,
  BottomSheetRecipes,
  DataTableRecipes,
  FormGroupRecipes,
  SelectRecipes,
  TextFieldRecipes,

  // Utility screens
  AccessibilityHelper,
} from './screens';
import {BottomSheetDepartmentModalRecipe} from './screens/BottomSheetDepartmentModalRecipe';

type Screen = {
  name: string;
  component: React.ComponentType<any>;
  headerTitle?: string;
};

const screens: Screen[] = [
  {
    name: 'ModalRecipes',
    component: ModalRecipes,
  },
  {
    name: 'CircularProgressIndicatorPlayground',
    component: CircularProgressIndicatorPlayground,
    headerTitle: 'CircularProgressIndicator',
  },
  {
    name: 'CircularProgressIndicatorOverview',
    component: CircularProgressIndicatorOverview,
    headerTitle: 'CircularProgressIndicator',
  },
  {
    name: 'DateDropdownOverview',
    component: DateDropdownOverview,
    headerTitle: 'DateDropdown',
  },
  {
    name: 'DateDropdownPlayground',
    component: DateDropdownPlayground,
    headerTitle: 'DateDropdown',
  },
  {
    name: 'SeeDetailsOverview',
    component: SeeDetailsOverview,
    headerTitle: 'SeeDetails',
  },
  {
    name: 'SeeDetailsRecipes',
    component: SeeDetailsRecipes,
    headerTitle: 'SeeDetails',
  },
  {
    name: 'SeeDetailsPlayground',
    component: SeeDetailsPlayground,
    headerTitle: 'SeeDetails',
  },
  {
    name: 'CollapseOverview',
    component: CollapseOverview,
    headerTitle: 'Collapse',
  },
  {
    name: 'CollapsePlayground',
    component: CollapsePlayground,
    headerTitle: 'Collapse',
  },
  // Foundation screens
  {name: 'ColorsOverview', component: ColorsOverview, headerTitle: 'Colors'},
  {name: 'IconsOverview', component: IconsOverview, headerTitle: 'Icons'},
  {
    name: 'TypographyOverview',
    component: TypographyOverview,
    headerTitle: 'Typography',
  },

  // Component screens

  {
    name: 'AlertOverview',
    component: AlertOverview,
    headerTitle: 'Alert',
  },
  {
    name: 'BadgeOverview',
    component: BadgeOverview,
    headerTitle: 'Badge',
  },
  {
    name: 'BottomSheetOverview',
    component: BottomSheetOverview,
    headerTitle: 'BottomSheet',
  },
  {name: 'ButtonOverview', component: ButtonOverview, headerTitle: 'Button'},
  {
    name: 'ButtonGroupOverview',
    component: ButtonGroupOverview,
    headerTitle: 'ButtonGroup',
  },
  {
    name: 'CalloutOverview',
    component: CalloutOverview,
    headerTitle: 'Callout',
  },
  {
    name: 'CardOverview',
    component: CardOverview,
    headerTitle: 'Card',
  },
  {
    name: 'CheckboxOverview',
    component: CheckboxOverview,
    headerTitle: 'Checkbox',
  },
  {
    name: 'ChipGroupOverview',
    component: ChipGroupOverview,
    headerTitle: 'Chip Group',
  },
  {name: 'ChipOverview', component: ChipOverview, headerTitle: 'Chip'},
  {name: 'DividerOverview', component: DividerOverview, headerTitle: 'Divider'},
  {
    name: 'ErrorMessageOverview',
    component: ErrorMessageOverview,
    headerTitle: 'ErrorMessage',
  },
  {
    name: 'FormGroupOverview',
    component: FormGroupOverview,
    headerTitle: 'FormGroup',
  },
  {
    name: 'FilterOverview',
    component: FilterOverview,
    headerTitle: 'Filter',
  },
  {
    name: 'FilterGroupOverview',
    component: FilterGroupOverview,
    headerTitle: 'FilterGroup',
  },
  {name: 'FormsOverview', component: FormsOverview, headerTitle: 'Forms'},
  {
    name: 'IconButtonOverview',
    component: IconButtonOverview,
    headerTitle: 'IconButton',
  },
  {
    name: 'IndicatorOverview',
    component: IndicatorOverview,
    headerTitle: 'Indicator',
  },
  {name: 'LayoutOverview', component: LayoutOverview, headerTitle: 'Layout'},
  {name: 'LinkOverview', component: LinkOverview, headerTitle: 'Link'},
  {name: 'ListOverview', component: ListOverview, headerTitle: 'List'},
  {name: 'MenuOverview', component: MenuOverview, headerTitle: 'Menu'},
  {
    name: 'MessagingOverview',
    component: MessagingOverview,
    headerTitle: 'Messaging',
  },
  {name: 'MetricOverview', component: MetricOverview, headerTitle: 'Metric'},
  {name: 'ModalOverview', component: ModalOverview, headerTitle: 'Modal'},
  {name: 'OverlayOverview', component: OverlayOverview, headerTitle: 'Overlay'},
  {name: 'PopoverOverview', component: PopoverOverview, headerTitle: 'Popover'},
  {
    name: 'ProgressIndicatorOverview',
    component: ProgressIndicatorOverview,
    headerTitle: 'ProgressIndicator',
  },
  {
    name: 'ProgressTrackerOverview',
    component: ProgressTrackerOverview,
    headerTitle: 'Progress Tracker',
  },
  {name: 'RadioOverview', component: RadioOverview, headerTitle: 'Radio'},
  {
    name: 'SegmentedOverview',
    component: SegmentedOverview,
    headerTitle: 'Segmented',
  },
  {name: 'SelectOverview', component: SelectOverview, headerTitle: 'Select'},
  {
    name: 'SkeletonOverview',
    component: SkeletonOverview,
    headerTitle: 'Skeleton',
  },
  {
    name: 'SnackbarOverview',
    component: SnackbarOverview,
    headerTitle: 'Snackbar',
  },
  {
    name: 'SpinnerOverview',
    component: SpinnerOverview,
    headerTitle: 'Spinner',
  },
  {
    name: 'SpotIconOverview',
    component: SpotIconOverview,
    headerTitle: 'SpotIcon',
  },
  {
    name: 'StyledTextOverview',
    component: StyledTextOverview,
    headerTitle: 'StyledText',
  },
  {
    name: 'SwitchOverview',
    component: SwitchOverview,
    headerTitle: 'Switch',
  },
  {
    name: 'TabNavigationOverview',
    component: TabNavigationOverview,
    headerTitle: 'TabNavigation',
  },
  {name: 'TagOverview', component: TagOverview, headerTitle: 'Tags'},
  {
    name: 'TextAreaOverview',
    component: TextAreaOverview,
    headerTitle: 'TextArea',
  },
  {
    name: 'TextFieldOverview',
    component: TextFieldOverview,
    headerTitle: 'TextField',
  },
  {
    name: 'WizardFooterOverview',
    component: WizardFooterOverview,
    headerTitle: 'WizardFooter',
  },
  {
    name: 'VariantsOverview',
    component: VariantsOverview,
    headerTitle: 'Variants',
  },

  // Playground screens
  {
    name: 'AlertPlayground',
    component: AlertPlayground,
    headerTitle: 'Alert',
  },
  {
    name: 'BadgePlayground',
    component: BadgePlayground,
    headerTitle: 'Badge',
  },
  {
    name: 'ButtonPlayground',
    component: ButtonPlayground,
    headerTitle: 'Button',
  },
  {
    name: 'CardPlayground',
    component: CardPlayground,
    headerTitle: 'Card',
  },
  {
    name: 'CheckboxPlayground',
    component: CheckboxPlayground,
    headerTitle: 'Checkbox',
  },
  {
    name: 'ChipGroupPlayground',
    component: ChipGroupPlayground,
    headerTitle: 'Chip Group',
  },
  {
    name: 'ChipPlayground',
    component: ChipPlayground,
    headerTitle: 'Chip',
  },
  {
    name: 'DividerPlayground',
    component: DividerPlayground,
    headerTitle: 'Divider Playground',
  },
  {
    name: 'FilterPlayground',
    component: FilterPlayground,
    headerTitle: 'Filter Playground',
  },
  {
    name: 'FilterGroupPlayground',
    component: FilterGroupPlayground,
    headerTitle: 'FilterGroup Playground',
  },
  {
    name: 'IconButtonPlayground',
    component: IconButtonPlayground,
    headerTitle: 'IconButton',
  },
  {name: 'LinkPlayground', component: LinkPlayground, headerTitle: 'Link'},
  {name: 'ListPlayground', component: ListPlayground, headerTitle: 'List'},
  {
    name: 'MetricPlayground',
    component: MetricPlayground,
    headerTitle: 'Metric',
  },
  {name: 'ModalPlayground', component: ModalPlayground, headerTitle: 'Modal'},
  {
    name: 'ProgressIndicatorPlayground',
    component: ProgressIndicatorPlayground,
    headerTitle: 'ProgressIndicator',
  },
  {
    name: 'ProgressTrackerPlayground',
    component: ProgressTrackerPlayground,
    headerTitle: 'Progress Tracker',
  },
  {name: 'RadioPlayground', component: RadioPlayground, headerTitle: 'Radio'},
  {
    name: 'SkeletonPlayground',
    component: SkeletonPlayground,
    headerTitle: 'Skeleton',
  },
  {
    name: 'SpotIconPlayground',
    component: SpotIconPlayground,
    headerTitle: 'SpotIcon',
  },
  {
    name: 'StyledTextPlayground',
    component: StyledTextPlayground,
    headerTitle: 'StyledText',
  },
  {
    name: 'SwitchPlayground',
    component: SwitchPlayground,
    headerTitle: 'Switch',
  },
  {
    name: 'TagPlayground',
    component: TagPlayground,
    headerTitle: 'Tag',
  },
  {
    name: 'VariantsPlayground',
    component: VariantsPlayground,
    headerTitle: 'Variants',
  },

  // Recipe screens
  {name: 'AlertRecipe', component: AlertRecipe},
  {
    name: 'AlertTalkBackRecipe',
    component: AlertTalkBackRecipe,
    headerTitle: 'Alert TalkBack',
  },
  {
    name: 'BadgeRecipes',
    component: BadgeRecipes,
    headerTitle: 'Badge',
  },
  {
    name: 'BottomSheetDepartmentModalRecipe',
    component: BottomSheetDepartmentModalRecipe,
    headerTitle: 'DepartmentModal',
  },
  {
    name: 'BottomSheetKeyboardRecipe',
    component: BottomSheetTextInputKeyboardRecipe,
    headerTitle: 'Keyboard',
  },
  {
    name: 'BottomSheetMultiTextInputsRecipe',
    component: BottomSheetMultiTextInputsRecipe,
    headerTitle: 'With TextFields',
  },
  {
    name: 'BottomSheetWithScrollableContentRecipe',
    component: BottomSheetWithScrollableContentRecipe,
    headerTitle: 'With Scrollable Content',
  },
  {
    name: 'BottomSheetWithFlatListContentRecipe',
    component: BottomSheetWithFlatListContentRecipe,
    headerTitle: 'With FlatList Content',
  },
  {
    name: 'BottomSheetWithCustomHeightContentRecipe',
    component: BottomSheetWithCustomHeightContentRecipe,
    headerTitle: 'With Custom Height Content',
  },
  {
    name: 'BottomSheetWithCustomActionsRecipe',
    component: BottomSheetWithCustomActionsRecipe,
    headerTitle: 'With Custom Actions',
  },
  {
    name: 'BottomSheetWithExposedPropsRecipe',
    component: BottomSheetWithExposedPropsRecipe,
    headerTitle: 'With exposed Props',
  },
  {
    name: 'BottomSheetWithoutRNModalPropsRecipe',
    component: BottomSheetWithoutRNModalPropsRecipe,
    headerTitle: 'withRNModal=false Props',
  },
  {
    name: 'ButtonRecipes',
    component: ButtonRecipes,
    headerTitle: 'Buttons Recipes',
  },
  {
    name: 'CalloutRecipes',
    component: CalloutRecipes,
    headerTitle: 'Callout w/Custom position',
  },
  {
    name: 'CardRecipes',
    component: CardRecipes,
    headerTitle: 'Card Recipes',
  },
  {
    name: 'CheckboxRecipes',
    component: CheckboxRecipes,
    headerTitle: 'Checkbox Recipes',
  },
  {
    name: 'ChipGroupRecipes',
    component: ChipGroupRecipes,
    headerTitle: 'ChipGroup Recipes',
  },
  {
    name: 'ChipRecipes',
    component: ChipRecipes,
    headerTitle: 'Chip Recipes',
  },
  {
    name: 'DataTableBulkActionsRecipe',
    component: DataTableBulkActionsRecipe,
    headerTitle: 'BulkActions',
  },
  {
    name: 'DataTableCellActionsRecipe',
    component: DataTableCellActionsRecipe,
    headerTitle: 'Cell Actions',
  },
  {
    name: 'DataTableCellActionsMenuRecipe',
    component: DataTableCellActionsMenuRecipe,
    headerTitle: 'Cell Actions Menu',
  },
  {
    name: 'DataTableCheckboxRecipe',
    component: DataTableCheckboxRecipe,
    headerTitle: 'Checkbox',
  },
  {
    name: 'DataTableScrollRecipe',
    component: DataTableScrollRecipe,
    headerTitle: 'Scroll',
  },
  {
    name: 'DataTableSortRecipe',
    component: DataTableSortRecipe,
    headerTitle: 'Sort',
  },
  {
    name: 'DataTableStatusRecipe',
    component: DataTableStatusRecipe,
    headerTitle: 'Status',
  },
  {
    name: 'ErrorMessageRecipes',
    component: ErrorMessageRecipes,
    headerTitle: 'ErrorMessage',
  },
  {
    name: 'FilterGroupRecipes',
    component: FilterGroupRecipes,
    headerTitle: 'FilterGroup Recipes',
  },
  {
    name: 'FormGroupCheckboxRecipe',
    component: FormGroupCheckboxRecipe,
    headerTitle: 'FormGroup Checkbox',
  },
  {
    name: 'FormGroupRadioRecipe',
    component: FormGroupRadioRecipe,
    headerTitle: 'FormGroup Radio',
  },
  {
    name: 'IconTintColorRecipe',
    component: IconTintColorRecipe,
    headerTitle: 'Icon tintColor',
  },
  {
    name: 'ListRecipes',
    component: ListRecipes,
    headerTitle: 'List Recipe',
  },
  {
    name: 'MetricRecipes',
    component: MetricRecipes,
    headerTitle: 'Metric Recipe',
  },
  {
    name: 'MetricGroupRecipes',
    component: MetricGroupRecipes,
    headerTitle: 'MetricGroup Recipe',
  },
  {
    name: 'PopoverRecipes',
    component: PopoverRecipes,
    headerTitle: 'Popover Recipe',
  },
  {
    name: 'ProgressIndicatorRecipes',
    component: ProgressIndicatorRecipes,
    headerTitle: 'ProgressIndicator Recipe',
  },
  {
    name: 'ProgressTrackerRecipes',
    component: ProgressTrackerRecipes,
    headerTitle: 'Progress Tracker',
  },
  {
    name: 'SelectWithCustomTextRecipe',
    component: SelectWithCustomTextRecipe,
    headerTitle: 'Select w/Custom Text',
  },
  {
    name: 'SelectWithExtraContentRecipe',
    component: SelectWithExtraContentRecipe,
    headerTitle: 'Select w/Custom Content',
  },
  {
    name: 'SelectWithLocalStateUpdateRecipe',
    component: SelectWithLocalStateUpdateRecipe,
    headerTitle: 'Select Local state Update Recipe',
  },
  {
    name: 'SelectWithLongListRecipe',
    component: SelectWithLongListRecipe,
    headerTitle: 'Select w/Long List',
  },
  {
    name: 'SkeletonRecipes',
    component: SkeletonRecipes,
    headerTitle: 'Skeleton Recipe',
  },
  {
    name: 'SpinnerRecipes',
    component: SpinnerRecipes,
    headerTitle: 'Spinner Recipes',
  },
  {
    name: 'SpotIconRecipes',
    component: SpotIconRecipes,
    headerTitle: 'SpotIcon Recipes',
  },
  {
    name: 'StyledTextRecipes',
    component: StyledTextRecipes,
    headerTitle: 'StyledText Recipe',
  },
  {
    name: 'SwitchRecipes',
    component: SwitchRecipes,
    headerTitle: 'Switch Recipe',
  },
  {
    name: 'TabNavigationRecipes',
    component: TabNavigationRecipes,
    headerTitle: 'Tab Navigation',
  },
  {
    name: 'TagRecipes',
    component: TagRecipes,
    headerTitle: 'Tag Recipes',
  },
  {
    name: 'TextFieldAccessibilityRecipe',
    component: TextFieldAccessibilityRecipe,
    headerTitle: 'TextFieldAccessibility Recipe',
  },
  {
    name: 'TextFieldRecipe',
    component: TextFieldRecipe,
    headerTitle: 'TextFields Recipe',
  },
  {
    name: 'ToggleablesRecipe',
    component: ToggleablesRecipe,
    headerTitle: 'Toggleables Recipe',
  },
  {
    name: 'VariantsRecipes',
    component: VariantsRecipes,
    headerTitle: 'Variants Recipe',
  },

  // Navigation drivers (these drive navigation to individual recipes)
  {name: 'AlertRecipes', component: AlertRecipes, headerTitle: 'Alert'},
  {
    name: 'BottomSheetRecipes',
    component: BottomSheetRecipes,
    headerTitle: 'BottomSheet',
  },
  {
    name: 'DataTableRecipes',
    component: DataTableRecipes,
    headerTitle: 'DataTable',
  },
  {
    name: 'DividerRecipes',
    component: DividerRecipes,
    headerTitle: 'Divider',
  },
  {
    name: 'FormGroupRecipes',
    component: FormGroupRecipes,
    headerTitle: 'FormGroup',
  },
  {
    name: 'SelectRecipes',
    component: SelectRecipes,
    headerTitle: 'Select',
  },
  {
    name: 'TextFieldRecipes',
    component: TextFieldRecipes,
    headerTitle: 'TextField',
  },

  // Utility screens
  {
    name: 'AccessibilityHelper',
    component: AccessibilityHelper,
    headerTitle: 'Accessibility',
  },
];

const RootStack = createStackNavigator();

const ThemeButton = (): React.ReactNode => {
  const isDark = useColorScheme() === 'dark';
  return (
    <View style={ss.themeButtons}>
      <IconButton
        children={<Text style={ss.themeTextIcon}>{isDark ? '🌙' : '🔆'}</Text>}
        onPress={() => {
          Appearance.setColorScheme(isDark ? 'light' : 'dark');
        }}
      />
    </View>
  );
};

const InnerApp = () => {
  const isDark = useColorScheme() === 'dark';
  const CustomDefaultTheme = {
    ...DefaultTheme,
    colors: {
      ...DefaultTheme.colors,
      background: '#FFFFFF', // react-navigation is off-white but our example app background is white
    },
  };

  return (
    <NavigationContainer theme={isDark ? DarkTheme : CustomDefaultTheme}>
      <RootStack.Navigator initialRouteName="Home">
        <RootStack.Screen
          name="Home"
          component={HomeScreen}
          options={{headerShown: false}}
        />
        {screens.map((item, index) => {
          return (
            <RootStack.Screen
              key={item.name + index}
              name={item.name}
              component={item.component}
              options={{
                headerTitle: item.headerTitle ?? item.name,
                headerRight: ThemeButton,
              }}
            />
          );
        })}
      </RootStack.Navigator>
    </NavigationContainer>
  );
};

const App = () => {
  return (
    <LivingDesignProvider>
      <InnerApp />
    </LivingDesignProvider>
  );
};

export {App};

const ss = StyleSheet.create({
  themeButtons: {
    flexDirection: 'row',
    marginRight: 16,
    gap: 16,
  },
  themeTextIcon: {
    fontSize: 16,
  },
});
