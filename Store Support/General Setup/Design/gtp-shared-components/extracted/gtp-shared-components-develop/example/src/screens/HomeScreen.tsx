import * as React from 'react';
import {
  SafeAreaView,
  StyleSheet,
  Text,
  useColorScheme,
  View,
} from 'react-native';
import {useTheme} from '@react-navigation/native';
import {StackNavigationProp} from '@react-navigation/stack';
import {colors, Button, Link} from '@walmart/gtp-shared-components';
import {NavigationProps} from '../types';
import {Page, Header, Section, HomeScreenHeader} from '../components';

type Props = {
  navigation: StackNavigationProp<NavigationProps, 'Home'>;
};

const Divider = () => <View style={ss.divider} />;

type CellProps = {
  name: string;
  overview?: boolean;
  playground?: boolean;
  recipes?: boolean;
  navigation: any;
};

const Cell = (props: CellProps) => {
  const {
    name,
    overview = false,
    playground = false,
    recipes = false,
    navigation,
  } = props;
  const theme = useTheme();
  const isDark = useColorScheme() === 'dark';

  return (
    <>
      <View style={ss.cellContainer}>
        <Text style={[ss.componentLabel, {color: theme.colors.text}]}>
          {name}
        </Text>
        <View style={ss.optionsContainer}>
          <Link
            color={isDark ? 'white' : 'default'}
            disabled={!overview}
            onPress={() => navigation.navigate(`${name}Overview`)}
            UNSAFE_style={[
              ss.optionButton,
              !overview ? ss.optionButtonDisabled : {},
            ]}>
            Overview
          </Link>
          <Link
            color={isDark ? 'white' : 'default'}
            disabled={!recipes}
            onPress={() => navigation.navigate(`${name}Recipes`)}
            UNSAFE_style={[
              ss.optionButton,
              !recipes ? ss.optionButtonDisabled : {},
            ]}>
            Recipes
          </Link>
          <Link
            color={isDark ? 'white' : 'default'}
            disabled={!playground}
            onPress={() => navigation.navigate(`${name}Playground`)}
            UNSAFE_style={[
              ss.optionButton,
              !playground ? ss.optionButtonDisabled : {},
            ]}>
            Playground
          </Link>
        </View>
      </View>
      <Divider />
    </>
  );
};

const HomeScreen = ({navigation}: Props) => {
  // Foundation
  const foundation = [
    {target: 'ColorsOverview', title: 'Colors'},
    {target: 'IconsOverview', title: 'Icons'},
    {target: 'TypographyOverview', title: 'Typography'},
  ];

  // Other Recipes
  // TODO not clear where these two belong, grouped the separately for now
  const otherRecipesButtons = [
    {target: 'IconTintColorRecipe', title: 'Icon tintColor'},
    {target: 'ToggleablesRecipe', title: 'Toggleables'},
  ];

  // Utility
  const utility = [{target: 'AccessibilityHelper', title: 'Accessibility'}];

  // Components
  // TODO: for entries where one or more of (overview, recipes, playground) are not specified, the corresponding target does not exist
  // e.g. AlertOverview, AlertPlayground don't exist and need to be created
  const ld_components = [
    {
      component: {
        name: 'Alert',
        recipes: true,
        overview: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Badge',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'BottomSheet',
        overview: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'Button',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'ButtonGroup',
        overview: true,
      },
    },
    {
      component: {
        name: 'Callout',
        overview: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'Card',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Checkbox',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Chip',
        overview: true,
        playground: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'ChipGroup',
        overview: true,
        playground: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'CircularProgressIndicator',
        overview: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Collapse',
        overview: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'DataTable',
        recipes: true,
      },
    },
    {
      component: {
        name: 'DateDropdown',
        overview: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Divider',
        overview: true,
        playground: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'ErrorMessage',
        overview: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'FormGroup',
        overview: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'Forms', // TODO needs to be refactored
        overview: true,
      },
    },
    {
      component: {
        name: 'IconButton',
        overview: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Indicator', // TODO needs to be refactored
        overview: true,
      },
    },
    {
      component: {
        name: 'Layout', // TODO needs to be refactored
        overview: true,
      },
    },
    {
      component: {
        name: 'Link',
        overview: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'List',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Menu',
        overview: true,
      },
    },
    {
      component: {
        name: 'Messaging', // TODO needs to be refactored
        overview: true,
      },
    },
    {
      component: {
        name: 'Metric',
        recipes: true,
        overview: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'MetricGroup',
        recipes: true,
      },
    },
    {
      component: {
        name: 'Modal',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Overlay', // TODO needs to be refactored
        overview: true,
      },
    },
    {
      component: {
        name: 'Popover',
        overview: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'ProgressIndicator',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'ProgressTracker',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Radio',
        overview: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'SeeDetails',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Segmented',
        overview: true,
      },
    },

    {
      component: {
        name: 'Select',
        overview: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'Skeleton',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'Snackbar',
        overview: true,
      },
    },
    {
      component: {
        name: 'Spinner',
        overview: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'SpotIcon',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'StyledText',
        overview: true,
        playground: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'Switch',
        overview: true,
        playground: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'TabNavigation',
        overview: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'Tag',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
    {
      component: {
        name: 'TextArea',
        overview: true,
      },
    },
    {
      component: {
        name: 'TextField',
        overview: true,
        recipes: true,
      },
    },
    {
      component: {
        name: 'WizardFooter',
        overview: true,
      },
    },
    {
      component: {
        name: 'Variants',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
  ];

  const ax_components = [
    {
      component: {
        name: 'Filter',
        overview: true,
        recipes: false,
        playground: true,
      },
    },
    {
      component: {
        name: 'FilterGroup',
        overview: true,
        recipes: true,
        playground: true,
      },
    },
  ];

  return (
    <SafeAreaView style={ss.container}>
      <HomeScreenHeader />
      <Page>
        <Header>Foundation</Header>
        <Section>
          <View style={ss.foundationSection}>
            {foundation.map(({target, title}) => {
              return (
                <Button
                  key={target}
                  variant="secondary"
                  onPress={() => navigation.navigate(target as any)}
                  UNSAFE_style={ss.foundationContentButton}>
                  {title ?? target}
                </Button>
              );
            })}
          </View>
        </Section>
        <Header>LD Components</Header>
        <Section>
          {ld_components.map(item => {
            return (
              <Cell
                {...item.component}
                navigation={navigation}
                key={`${item.component.name}Component`}
              />
            );
          })}
        </Section>
        <Header>AX Components</Header>
        <Section>
          {ax_components.map(item => {
            return (
              <Cell
                {...item.component}
                navigation={navigation}
                key={`${item.component.name}Component`}
              />
            );
          })}
        </Section>
        <Header>Other Recipes</Header>
        <Section>
          {otherRecipesButtons.map(({target, title}) => {
            return (
              <Button
                key={target}
                variant="secondary"
                isFullWidth
                onPress={() => navigation.navigate(target as any)}
                UNSAFE_style={ss.contentButton}>
                {title ?? target}
              </Button>
            );
          })}
        </Section>
        <Header>Utility</Header>
        <Section>
          {utility.map(({target, title}) => {
            return (
              <Button
                key={target}
                variant="secondary"
                isFullWidth
                onPress={() => navigation.navigate(target as any)}
                UNSAFE_style={ss.contentButton}>
                {title ?? target}
              </Button>
            );
          })}
        </Section>
      </Page>
    </SafeAreaView>
  );
};

const ss = StyleSheet.create({
  container: {
    backgroundColor: 'transparent',
    flex: 1,
    paddingBottom: 18,
  },
  content: {
    flex: 0,
    padding: 16,
  },
  innerContent: {
    paddingBottom: 16,
  },
  contentButton: {
    maxWidth: '40%',
    alignSelf: 'flex-start',
    marginBottom: 12,
  },
  foundationContentButton: {
    // maxWidth: '25%',
    alignSelf: 'center',
  },
  foundationSection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  divider: {
    height: 0.8,
    backgroundColor: colors.gray['50'],
  },
  cellContainer: {
    justifyContent: 'space-between',
  },
  optionsContainer: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginBottom: 12,
    marginRight: 12,
    gap: 22,
  },
  optionButton: {
    fontSize: 15,
    marginVertical: 8,
    alignSelf: 'flex-end',
  },
  optionButtonDisabled: {
    opacity: 0.5,
    color: colors.gray['50'],
  },
  componentLabel: {
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export {HomeScreen};
