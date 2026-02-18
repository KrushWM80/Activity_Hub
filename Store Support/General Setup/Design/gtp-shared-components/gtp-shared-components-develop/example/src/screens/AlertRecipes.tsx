import * as React from 'react';
import {StackNavigationProp} from '@react-navigation/stack';
import type {NavigationProps} from '../types';
import {NavDriver} from '../components/NavDriver';

type ButtonsScreenProps = {
  navigation: StackNavigationProp<NavigationProps, 'Home'>;
};

const AlertRecipes = ({navigation}: ButtonsScreenProps) => {
  const buttons = [
    {target: 'AlertRecipe', title: 'Alert Recipe'},
    {target: 'AlertTalkBackRecipe', title: 'Alert TalkBack'},
  ];

  return (
    <NavDriver
      navigation={navigation}
      header="Alert Recipes"
      buttons={buttons}
    />
  );
};

export {AlertRecipes};
