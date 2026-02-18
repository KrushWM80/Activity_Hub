import * as React from 'react';
import {View, StyleSheet} from 'react-native';

import {
  Icons,
  colors,
  Button,
  _KeyboardAvoidingView as KeyboardAvoidingView,
} from '@walmart/gtp-shared-components';
import {Page, Header, VariantText} from '../components';
import {displayPopupAlert} from './screensFixtures';

// ---------------
// Rendering
// ---------------
const ButtonWithForwardRef = React.forwardRef<View>((props, ref) => {
  const buttonRef = ref as React.RefObject<View>;
  return (
    <>
      <Header>
        Button{'\n  '}
        <VariantText>using forwardRef</VariantText>
      </Header>
      <View style={[ss.outerContainer, ss.innerContainerRow]}>
        <Button
          ref={ref}
          variant="secondary"
          onPress={() => {
            displayPopupAlert('Action', 'Button forwardRef pressed');
          }}>
          Button w/ forwardRef
        </Button>
        <Button
          variant="primary"
          onPress={() => {
            buttonRef?.current?.measure(
              (
                x: number,
                y: number,
                width: number,
                height: number,
                pageX: number,
                pageY: number,
              ) => {
                displayPopupAlert(
                  'Action',
                  `Button w/ forwardRef measured: x: ${x}, y: ${y}, width: ${width}, height: ${height}, pageX: ${pageX}, pageY: ${pageY}`,
                );
              },
            );
          }}>
          Measure
        </Button>
      </View>
    </>
  );
});

const ButtonWithLargeFont = () => {
  return (
    <>
      <Header>
        Button (tertiary){'\n  '}
        <VariantText>{'UNSAFE_style={{fontSize: 24}}'}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Button
            size="large"
            variant="tertiary"
            leading={<Icons.ArticleIcon />}
            testID="spec-sheet-icon"
            // eslint-disable-next-line react-native/no-inline-styles
            UNSAFE_style={{fontSize: 24}}
            onPress={() => console.log('Button pressed')}>
            Large font
          </Button>
        </View>
      </View>
    </>
  );
};

const ButtonWithFontColor = () => {
  return (
    <>
      <Header>
        Button (tertiary){'\n  '}
        <VariantText>
          {"UNSAFE_style={{color: colors.blue['100']}}"}
        </VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Button
            size="large"
            variant="tertiary"
            leading={<Icons.ArticleIcon />}
            testID="spec-sheet-icon"
            UNSAFE_style={{color: colors.blue['100']}}
            onPress={() => console.log('Button pressed')}>
            Color blue
          </Button>
        </View>
      </View>
    </>
  );
};

const ButtonWithFontWeight = () => {
  return (
    <>
      <Header>
        Button (tertiary){'\n  '}
        <VariantText>{"UNSAFE_style={{fontWeight: 'bold'}}"}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Button
            size="large"
            variant="tertiary"
            leading={<Icons.ArticleIcon />}
            testID="spec-sheet-icon"
            // eslint-disable-next-line react-native/no-inline-styles
            UNSAFE_style={{fontWeight: 'bold'}}
            onPress={() => console.log('Button pressed')}>
            Font weight bold
          </Button>
        </View>
      </View>
    </>
  );
};

const ButtonWithLineHeight = () => {
  return (
    <>
      <Header>
        Button (tertiary){'\n  '}
        <VariantText>{'UNSAFE_style={{lineHeight: 26}}'}</VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Button
            size="large"
            variant="tertiary"
            leading={<Icons.ArticleIcon />}
            testID="spec-sheet-icon"
            // eslint-disable-next-line react-native/no-inline-styles
            UNSAFE_style={{lineHeight: 26}}
            onPress={() => console.log('Button pressed')}>
            Font line height
          </Button>
        </View>
      </View>
    </>
  );
};

const Spacer = () => <View style={ss.spacer} />;
const ButtonWithLongTitle = () => {
  return (
    <>
      <Header>
        Button (secondary){'\n  '}
        <VariantText>
          with long title text{'\n'}(from homeoffice-me-chatbot-mini-app){' '}
        </VariantText>
      </Header>
      <View style={ss.outerContainer}>
        <View style={ss.innerContainer}>
          <Button
            size="medium"
            variant="secondary"
            isFullWidth
            onPress={() => console.log('pressed')}>
            Receiving an associate from another team
          </Button>
          <Spacer />
          <Button
            size="medium"
            variant="secondary"
            isFullWidth
            onPress={() => console.log('pressed')}>
            Sending an associate to another team
          </Button>
        </View>
      </View>
    </>
  );
};

const ButtonRecipes: React.FC = () => {
  const buttonRef = React.useRef<View | null>(null);
  return (
    <KeyboardAvoidingView>
      <Page>
        <ButtonWithForwardRef ref={buttonRef} />
        <ButtonWithLongTitle />
        <Header>
          NOTE{'\n  '}{' '}
          <VariantText>
            the following are unsafe, non-recommended options
          </VariantText>
        </Header>
        <ButtonWithLargeFont />
        <ButtonWithFontColor />
        <ButtonWithFontWeight />
        <ButtonWithLineHeight />
      </Page>
    </KeyboardAvoidingView>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  innerContainer: {
    padding: 10,
  },
  innerContainerRow: {
    padding: 10,
    flex: 1,
    justifyContent: 'space-around',
    flexDirection: 'row',
  },
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
  spacer: {
    height: 8,
  },
});

export {ButtonRecipes};
