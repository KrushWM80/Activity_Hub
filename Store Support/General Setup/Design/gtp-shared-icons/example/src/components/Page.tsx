/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {ScrollView, View} from 'react-native';

type PageProps = {
  children: React.ReactNode;
};

class Page extends React.Component<PageProps> {
  render() {
    return (
      <ScrollView style={{flex: 1, backgroundColor: 'white'}}>
        <View style={{padding: 16}}>{this.props.children}</View>
      </ScrollView>
    );
  }
}

export {Page};
