import * as React from 'react';
import {StackNavigationProp} from '@react-navigation/stack';
import type {NavigationProps} from '../types';
import {NavDriver} from '../components/NavDriver';

type ButtonsScreenProps = {
  navigation: StackNavigationProp<NavigationProps, 'Home'>;
};

const SelectRecipes = ({navigation}: ButtonsScreenProps) => {
  const buttons = [
    {
      target: 'SelectWithExtraContentRecipe',
      title: 'Select w/Extra Content',
    },
    {
      target: 'SelectWithLocalStateUpdateRecipe',
      title: 'Select With local state update',
    },
    {
      target: 'SelectWithLongListRecipe',
      title: 'Select w/Long List of Options',
    },
    {
      target: 'SelectWithCustomTextRecipe',
      title: 'Select w/Custom Text',
    },
  ];

  return (
    <NavDriver
      navigation={navigation}
      header="Select Recipes"
      buttons={buttons}
    />
  );
};

export {SelectRecipes};
