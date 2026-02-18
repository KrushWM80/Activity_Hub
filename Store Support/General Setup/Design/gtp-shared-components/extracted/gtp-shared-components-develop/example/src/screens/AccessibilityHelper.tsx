import * as React from 'react';
import {Text} from 'react-native';
import {Button, useAccessibilityFocus} from '@walmart/gtp-shared-components';
import {Header, Page, Section, VariantText} from '../components';
import {useFocusEffect} from '@react-navigation/native';

const AccessibilityHelper: React.FC = () => {
  const [focusRef, setFocus] = useAccessibilityFocus();

  useFocusEffect(setFocus);

  return (
    <>
      <Page>
        <>
          <Header>
            Accessibility Helper{'\n'}{' '}
            <VariantText>with useAccessibilityFocus hook</VariantText>
          </Header>
          <Section>
            <Text>
              Android - TalkBack / iOS - Voice Over focus the Button component 2
              where the useAccessibilityFocus is referenced when navigated from
              previous screen using react navigation library.
            </Text>
            <Button onPress={() => {}}>Component 1</Button>
            <Button ref={focusRef} onPress={() => {}}>
              Component 2
            </Button>
          </Section>
        </>
      </Page>
    </>
  );
};

export {AccessibilityHelper};
