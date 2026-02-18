import * as React from 'react';
import {ScrollView, SafeAreaView, StyleSheet} from 'react-native';

type PageProps = {
  color?: string;
  children: React.ReactNode;
};

const Page: React.FC<PageProps> = (props: PageProps) => {
  const {color, children} = props;

  return (
    <SafeAreaView style={[ss.container, color ? {backgroundColor: color} : {}]}>
      <ScrollView keyboardShouldPersistTaps="always" style={ss.content}>
        {children}
      </ScrollView>
    </SafeAreaView>
  );
};

export default Page;

const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 0,
    paddingBottom: 16,
    paddingRight: 16,
    paddingLeft: 16,
  },
});
