import * as React from 'react';
import {StackNavigationProp} from '@react-navigation/stack';
import type {NavigationProps} from '../types';
import {NavDriver} from '../components/NavDriver';

type ButtonsScreenProps = {
  navigation: StackNavigationProp<NavigationProps, 'Home'>;
};

const FormGroupRecipes = ({navigation}: ButtonsScreenProps) => {
  const buttons = [
    {
      target: 'FormGroupCheckboxRecipe',
      title: 'FormGroup Checkbox Recipe',
    },
    {target: 'FormGroupRadioRecipe', title: 'FormGroup Radio Recipe'},
  ];

  return (
    <NavDriver
      navigation={navigation}
      header="FormGroup Recipes"
      buttons={buttons}
    />
  );
};

export {FormGroupRecipes};
