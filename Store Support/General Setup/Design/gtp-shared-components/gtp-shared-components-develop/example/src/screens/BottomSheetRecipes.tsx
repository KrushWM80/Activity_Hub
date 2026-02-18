import * as React from 'react';
import {StackNavigationProp} from '@react-navigation/stack';
import type {NavigationProps} from '../types';
import {NavDriver} from '../components/NavDriver';

type ButtonsScreenProps = {
  navigation: StackNavigationProp<NavigationProps, 'Home'>;
};

const BottomSheetRecipes = ({navigation}: ButtonsScreenProps) => {
  const buttons = [
    {
      target: 'BottomSheetMultiTextInputsRecipe',
      title: 'With Multiple TextFields',
    },
    {
      target: 'BottomSheetDepartmentModalRecipe',
      title: 'Department Modal',
    },
    {
      target: 'BottomSheetKeyboardRecipe',
      title: 'Keyboard Behavior',
    },
    {
      target: 'BottomSheetWithScrollableContentRecipe',
      title: 'With Scrollable Content',
    },
    {
      target: 'BottomSheetWithFlatListContentRecipe',
      title: 'With FlatList Content',
    },
    {
      target: 'BottomSheetWithCustomHeightContentRecipe',
      title: 'With Custom Height Content',
    },
    {
      target: 'BottomSheetWithCustomActionsRecipe',
      title: 'With Custom Actions',
    },
    {
      target: 'BottomSheetWithExposedPropsRecipe',
      title: 'With BS Modal props',
    },
    {
      target: 'BottomSheetWithoutRNModalPropsRecipe',
      title: 'With withRNModal=false props',
    },
  ];

  return (
    <NavDriver
      navigation={navigation}
      header="BottomSheet Recipes"
      buttons={buttons}
    />
  );
};

export {BottomSheetRecipes};
