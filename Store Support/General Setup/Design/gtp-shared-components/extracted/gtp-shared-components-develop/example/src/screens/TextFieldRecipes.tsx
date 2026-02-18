import * as React from 'react';
import {StackNavigationProp} from '@react-navigation/stack';
import type {NavigationProps} from '../types';
import {NavDriver} from '../components/NavDriver';

type ButtonsScreenProps = {
  navigation: StackNavigationProp<NavigationProps, 'Home'>;
};

const TextFieldRecipes = ({navigation}: ButtonsScreenProps) => {
  const buttons = [
    {target: 'TextFieldRecipe', title: 'TextField Recipe'},
    {
      target: 'TextFieldAccessibilityRecipe',
      title: 'TextField Accessibility Recipe',
    },
  ];

  return (
    <NavDriver
      navigation={navigation}
      header="TextField Recipes"
      buttons={buttons}
    />
  );
};

export {TextFieldRecipes};
