import * as React from 'react';
import {StackNavigationProp} from '@react-navigation/stack';
import type {NavigationProps} from '../types';
import {NavDriver} from '../components/NavDriver';

type ButtonsScreenProps = {
  navigation: StackNavigationProp<NavigationProps, 'Home'>;
};

const DataTableRecipes = ({navigation}: ButtonsScreenProps) => {
  const buttons = [
    {target: 'DataTableBulkActionsRecipe', title: 'Bulk Actions'},
    {target: 'DataTableCellActionsRecipe', title: 'Cell Actions'},
    {
      target: 'DataTableCellActionsMenuRecipe',
      title: 'Cell Actions Menu',
    },
    {target: 'DataTableCheckboxRecipe', title: 'Checkbox'},
    {target: 'DataTableScrollRecipe', title: 'Scroll'},
    {target: 'DataTableSortRecipe', title: 'Sort'},
    {target: 'DataTableStatusRecipe', title: 'Status'},
  ];

  return (
    <NavDriver
      navigation={navigation}
      header="DataTable Recipes"
      buttons={buttons}
    />
  );
};

export {DataTableRecipes};
