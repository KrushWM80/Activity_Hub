import * as React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator} from '@react-navigation/stack';
import {IconsScreen} from './screens/IconsScreen';
import {HomeScreen} from './screens/HomeScreen';

const Stack = createStackNavigator();
const App = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{headerShown: false}}
        />
        <Stack.Screen
          name="Icons"
          component={IconsScreen}
          options={{headerBackTitle: 'Home'}}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export {App};
