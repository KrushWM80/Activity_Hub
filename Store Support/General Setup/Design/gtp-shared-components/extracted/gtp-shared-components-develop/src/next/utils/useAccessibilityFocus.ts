import {MutableRefObject, useCallback, useRef} from 'react';
import {AccessibilityInfo, findNodeHandle} from 'react-native';

/**
 * This hook should be used to programmatically set focus on a component when the screen is loaded.
 * It should be used as a last resort.  Ideally focus would be managed with correct order of components in the tree and proper use of the "accessible" prop.
 *
 * Components that require setting programmatic focus on events (ex: a toast a result of an action) should use AccessibilityInfo.setAccessibilityFocus directly.
 *
 * `@returns {Object}` A ref that should be assigned to the "ref" property of the component that should be focused on the screen.
 *
 * ## Usage
 * ```js
 * import * as React from 'react';
 * import {Text} from 'react-native';
 * import {Button, useAccessibilityFocus} from '@walmart/gtp-shared-components';
 * import {Header, Page, Section, VariantText} from '../components';
 * import {useFocusEffect} from '@react-navigation/native';
 *
 * const AccessibilityHelper: React.FC = () => {
 *  const [focusRef, setFocus] = useAccessibilityFocus();
 *
 *  useFocusEffect(setFocus);
 *
 *  return (
 *    <>
 *      <Page>
 *        <>
 *          <Header>
 *            Accessibility Helper{'\n'}{' '}
 *            <VariantText>with useAccessibilityFocus hook</VariantText>
 *          </Header>
 *          <Section>
 *            <Text>
 *              Android - TalkBack / iOS - Voice Over focus the Button component 2
 *              where the useAccessibilityFocus is referenced when navigated from
 *              previous screen using react navigation library.
 *            </Text>
 *            <Button onPress={() => {}}>Component 1</Button>
 *            <Button ref={focusRef} onPress={() => {}}>
 *              Component 2
 *            </Button>
 *          </Section>
 *        </>
 *      </Page>
 *    </>
 *  );
 * };
 *
 * export {AccessibilityHelper};
 * ```
 *
 */
export function useAccessibilityFocus(): [MutableRefObject<any>, () => void] {
  const focusRef = useRef(null);

  const setFocus = useCallback(() => {
    if (focusRef.current) {
      const reactTag = findNodeHandle(focusRef.current);
      if (reactTag) {
        setTimeout(() => {
          // Due to screen lifecycle, we need to put a minor delay, or React Nav (or other) components may steal focus.
          AccessibilityInfo.setAccessibilityFocus(reactTag);
        }, 200);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [focusRef.current]);

  return [focusRef, setFocus];
}
