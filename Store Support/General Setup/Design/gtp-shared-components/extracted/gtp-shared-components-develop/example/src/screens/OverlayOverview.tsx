/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {Header, Page, Section, DirectionView} from '../components';
import {
  Button,
  Callout,
  Checkbox,
  Link,
  Popover,
  Tooltip,
  useSimpleReducer,
  SpinnerOverlay,
  Body,
  delay,
} from '@walmart/gtp-shared-components';

export const OverlayOverview: React.FC = () => {
  type CalloutOpenState = {
    isCalloutOpen1: boolean;
    closeText1: string;
    isCalloutOpen2: boolean;
    closeText2: string;
    isCalloutOpen3: boolean;
    closeText3: string;
    isCalloutOpen4: boolean;
    closeText4: string;
    isCalloutOpen5: boolean;
    closeText5: string;
    isCalloutOpen6: boolean;
    closeText6: string;
    isCalloutOpen7: boolean;
    closeText7: string;
    isCalloutOpen8: boolean;
    closeText8: string;
  };

  const [calloutState, setCalloutState] = useSimpleReducer<CalloutOpenState>({
    isCalloutOpen1: false,
    closeText1: 'Close',
    isCalloutOpen2: false,
    closeText2: 'Got it',
    isCalloutOpen3: false,
    closeText3: 'Dismiss',
    isCalloutOpen4: false,
    closeText4: 'OK',
    isCalloutOpen5: false,
    closeText5: 'Cerca',
    isCalloutOpen6: false,
    closeText6: 'Fermer',
    isCalloutOpen7: false,
    closeText7: 'Chiudere',
    isCalloutOpen8: false,
    closeText8: 'Inchide',
  });

  type PopoverOpenState = {
    isPopoverOpen1: boolean;
    isPopoverOpen2: boolean;
    isPopoverOpen3: boolean;
    isPopoverOpen4: boolean;
    isPopoverOpen5: boolean;
    isPopoverOpen6: boolean;
    isPopoverOpen7: boolean;
    isPopoverOpen8: boolean;
  };

  const [popoverState, setPopoverState] = useSimpleReducer<PopoverOpenState>({
    isPopoverOpen1: false,
    isPopoverOpen2: false,
    isPopoverOpen3: false,
    isPopoverOpen4: false,
    isPopoverOpen5: false,
    isPopoverOpen6: false,
    isPopoverOpen7: false,
    isPopoverOpen8: false,
  });

  const [hasNubbin, setHasNubbin] = React.useState(true);
  const [contentChecked, setContentChecked] = React.useState(false);

  const content = () => {
    return (
      <View style={{width: 200}}>
        <Checkbox
          label="I must contain at least one focusable element."
          checked={contentChecked}
          onPress={() => {
            setContentChecked(previousState => !previousState);
          }}
        />
      </View>
    );
  };

  const SpinnerOverlayWithContent = () => {
    const [showOverlay, setShowOverlay] = React.useState(false);
    const [darken, setDarken] = React.useState(false);
    const [transparent, setTransparent] = React.useState(true);

    return (
      <>
        <Header>SpinnerOverlay (with children)</Header>
        <Section>
          <Button onPress={() => setShowOverlay(true)}>
            Show Spinner Overlay
          </Button>
          <Checkbox
            label="Darkened"
            checked={darken}
            onPress={() => setDarken(!darken)}
          />
          <Checkbox
            label="Transparent"
            checked={transparent}
            onPress={() => setTransparent(!transparent)}
          />
        </Section>
        <SpinnerOverlay
          visible={showOverlay}
          onRequestClose={() => setShowOverlay(false)}
          darken={darken}
          spinnerColor={darken ? 'white' : 'gray'}
          transparent={transparent}>
          <Body
            weight="bold"
            UNSAFE_style={[styles.overlayBody, darken ? {color: 'white'} : {}]}>
            We're saving your selection
          </Body>
          <Button variant="primary" onPress={() => setShowOverlay(false)}>
            Close Overlay
          </Button>
        </SpinnerOverlay>
      </>
    );
  };

  const SpinnerOverlayAutoClosing = () => {
    const [showOverlay, setShowOverlay] = React.useState(false);
    React.useEffect(() => {
      // Simulates an API call finishing
      if (showOverlay) {
        delay(2000).then(() => setShowOverlay(false));
      }
    }, [showOverlay]);

    return (
      <>
        <Header>SpinnerOverlay (auto-closing)</Header>
        <Section>
          <Button onPress={() => setShowOverlay(true)}>
            Show Spinner Overlay
          </Button>
        </Section>
        <SpinnerOverlay
          visible={showOverlay}
          onRequestClose={() => setShowOverlay(false)}
          darken={true}
          spinnerColor={'white'}
          transparent={true}
        />
      </>
    );
  };

  return (
    <Page>
      <Header>Callouts</Header>
      <Section color="white">
        <DirectionView>
          <Callout
            content={'Example Callout content.'}
            isOpen={calloutState.isCalloutOpen1 as boolean}
            closeText={calloutState.closeText1 as string}
            onClose={() =>
              setCalloutState(
                'isCalloutOpen1',
                !(calloutState.isCalloutOpen1 as boolean),
              )
            }
            position="bottomRight">
            <Link
              onPress={() =>
                setCalloutState(
                  'isCalloutOpen1',
                  !(calloutState.isCalloutOpen1 as boolean),
                )
              }>
              Bottom{'\n'}Right
            </Link>
          </Callout>
          <Callout
            content={
              <View style={{width: 300, paddingHorizontal: 16}}>
                <Text style={{color: 'white'}}>
                  Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed
                  do eiusmod tempor incididunt ut labore et dolore magna aliqua
                </Text>
              </View>
            }
            isOpen={calloutState.isCalloutOpen2 as boolean}
            closeText={calloutState.closeText2 as string}
            onClose={() =>
              setCalloutState(
                'isCalloutOpen2',
                !(calloutState.isCalloutOpen2 as boolean),
              )
            }
            position="bottomCenter">
            <Link
              onPress={() =>
                setCalloutState(
                  'isCalloutOpen2',
                  !(calloutState.isCalloutOpen2 as boolean),
                )
              }>
              Bottom{'\n'}Center
            </Link>
          </Callout>
          <Callout
            content={'Example Callout content.'}
            isOpen={calloutState.isCalloutOpen3 as boolean}
            closeText={calloutState.closeText3 as string}
            onClose={() =>
              setCalloutState(
                'isCalloutOpen3',
                !(calloutState.isCalloutOpen3 as boolean),
              )
            }
            position="bottomLeft">
            <Link
              onPress={() =>
                setCalloutState(
                  'isCalloutOpen3',
                  !(calloutState.isCalloutOpen3 as boolean),
                )
              }>
              Bottom{'\n'}Left
            </Link>
          </Callout>
        </DirectionView>
        <DirectionView>
          <Callout
            content={'Example Callout content.'}
            isOpen={calloutState.isCalloutOpen4 as boolean}
            closeText={calloutState.closeText4 as string}
            onClose={() =>
              setCalloutState(
                'isCalloutOpen4',
                !(calloutState.isCalloutOpen4 as boolean),
              )
            }
            position="right">
            <Link
              onPress={() =>
                setCalloutState(
                  'isCalloutOpen4',
                  !(calloutState.isCalloutOpen4 as boolean),
                )
              }>
              Right
            </Link>
          </Callout>
          <Callout
            content={'Example Callout content.'}
            isOpen={calloutState.isCalloutOpen5 as boolean}
            closeText={calloutState.closeText5 as string}
            onClose={() =>
              setCalloutState(
                'isCalloutOpen5',
                !(calloutState.isCalloutOpen5 as boolean),
              )
            }
            position="left">
            <Link
              onPress={() =>
                setCalloutState(
                  'isCalloutOpen5',
                  !(calloutState.isCalloutOpen5 as boolean),
                )
              }>
              Left
            </Link>
          </Callout>
        </DirectionView>
        <DirectionView>
          <Callout
            content={'Example Callout content.'}
            isOpen={calloutState.isCalloutOpen6 as boolean}
            closeText={calloutState.closeText6 as string}
            onClose={() =>
              setCalloutState(
                'isCalloutOpen6',
                !(calloutState.isCalloutOpen6 as boolean),
              )
            }
            position="topRight">
            <Link
              onPress={() =>
                setCalloutState(
                  'isCalloutOpen6',
                  !(calloutState.isCalloutOpen6 as boolean),
                )
              }>
              Top{'\n'}Right
            </Link>
          </Callout>
          <Callout
            content={'Example Callout content.'}
            isOpen={calloutState.isCalloutOpen7 as boolean}
            closeText={calloutState.closeText7 as string}
            onClose={() =>
              setCalloutState(
                'isCalloutOpen7',
                !(calloutState.isCalloutOpen7 as boolean),
              )
            }
            position="topCenter">
            <Link
              onPress={() =>
                setCalloutState(
                  'isCalloutOpen7',
                  !(calloutState.isCalloutOpen7 as boolean),
                )
              }>
              Top{'\n'}Center
            </Link>
          </Callout>
          <Callout
            content={'Example Callout content.'}
            isOpen={calloutState.isCalloutOpen8 as boolean}
            closeText={calloutState.closeText8 as string}
            onClose={() =>
              setCalloutState(
                'isCalloutOpen8',
                !(calloutState.isCalloutOpen8 as boolean),
              )
            }
            position="topLeft">
            <Link
              onPress={() =>
                setCalloutState(
                  'isCalloutOpen8',
                  !(calloutState.isCalloutOpen8 as boolean),
                )
              }>
              Top{'\n'}Left
            </Link>
          </Callout>
        </DirectionView>
      </Section>
      <Header>Popovers</Header>
      <Section color="white">
        <DirectionView>
          <Popover
            content={content()}
            isOpen={popoverState.isPopoverOpen1 as boolean}
            onClose={() =>
              setPopoverState(
                'isPopoverOpen1',
                !(popoverState.isPopoverOpen1 as boolean),
              )
            }
            hasNubbin={hasNubbin}
            position="bottomRight">
            <Link
              onPress={() =>
                setPopoverState(
                  'isPopoverOpen1',
                  !(popoverState.isPopoverOpen1 as boolean),
                )
              }>
              Bottom{'\n'}Right
            </Link>
          </Popover>
          <Popover
            content={
              <View style={{width: 300}}>
                <Checkbox
                  checked={contentChecked}
                  onPress={async () => {
                    setContentChecked(previousState => !previousState);
                    await delay(400);
                    setPopoverState(
                      'isPopoverOpen2',
                      !(popoverState.isPopoverOpen2 as boolean),
                    );
                  }}
                  label="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
                />
              </View>
            }
            isOpen={popoverState.isPopoverOpen2 as boolean}
            onClose={() =>
              setPopoverState(
                'isPopoverOpen2',
                !(popoverState.isPopoverOpen2 as boolean),
              )
            }
            hasNubbin={hasNubbin}
            position="bottomCenter">
            <Link
              onPress={() =>
                setPopoverState(
                  'isPopoverOpen2',
                  !(popoverState.isPopoverOpen2 as boolean),
                )
              }>
              Bottom{'\n'}Center
            </Link>
          </Popover>
          <Popover
            content={content()}
            isOpen={popoverState.isPopoverOpen3 as boolean}
            onClose={() =>
              setPopoverState(
                'isPopoverOpen3',
                !(popoverState.isPopoverOpen3 as boolean),
              )
            }
            hasNubbin={hasNubbin}
            position="bottomLeft">
            <Link
              onPress={() =>
                setPopoverState(
                  'isPopoverOpen3',
                  !(popoverState.isPopoverOpen3 as boolean),
                )
              }>
              Bottom{'\n'}Left
            </Link>
          </Popover>
        </DirectionView>
        <DirectionView>
          <Popover
            content={content()}
            isOpen={popoverState.isPopoverOpen4 as boolean}
            onClose={() =>
              setPopoverState(
                'isPopoverOpen4',
                !(popoverState.isPopoverOpen4 as boolean),
              )
            }
            hasNubbin={hasNubbin}
            position="right">
            <Link
              onPress={() =>
                setPopoverState(
                  'isPopoverOpen4',
                  !(popoverState.isPopoverOpen4 as boolean),
                )
              }>
              Right
            </Link>
          </Popover>
          <Popover
            content={content()}
            isOpen={popoverState.isPopoverOpen5 as boolean}
            onClose={() =>
              setPopoverState(
                'isPopoverOpen5',
                !(popoverState.isPopoverOpen5 as boolean),
              )
            }
            hasNubbin={hasNubbin}
            position="left">
            <Link
              onPress={() =>
                setPopoverState(
                  'isPopoverOpen5',
                  !(popoverState.isPopoverOpen5 as boolean),
                )
              }>
              Left
            </Link>
          </Popover>
        </DirectionView>
        <DirectionView>
          <Popover
            content={content()}
            isOpen={popoverState.isPopoverOpen6 as boolean}
            onClose={() =>
              setPopoverState(
                'isPopoverOpen6',
                !(popoverState.isPopoverOpen6 as boolean),
              )
            }
            hasNubbin={hasNubbin}
            position="topRight">
            <Link
              onPress={() =>
                setPopoverState(
                  'isPopoverOpen6',
                  !(popoverState.isPopoverOpen6 as boolean),
                )
              }>
              Top{'\n'}Right
            </Link>
          </Popover>
          <Popover
            content={content()}
            isOpen={popoverState.isPopoverOpen7 as boolean}
            onClose={() =>
              setPopoverState(
                'isPopoverOpen7',
                !(popoverState.isPopoverOpen7 as boolean),
              )
            }
            hasNubbin={hasNubbin}
            position="topCenter">
            <Link
              onPress={() =>
                setPopoverState(
                  'isPopoverOpen7',
                  !(popoverState.isPopoverOpen7 as boolean),
                )
              }>
              Top{'\n'}Center
            </Link>
          </Popover>
          <Popover
            content={content()}
            isOpen={popoverState.isPopoverOpen8 as boolean}
            onClose={() =>
              setPopoverState(
                'isPopoverOpen8',
                !(popoverState.isPopoverOpen8 as boolean),
              )
            }
            hasNubbin={hasNubbin}
            position="topLeft">
            <Link
              onPress={() =>
                setPopoverState(
                  'isPopoverOpen8',
                  !(popoverState.isPopoverOpen8 as boolean),
                )
              }>
              Top{'\n'}Left
            </Link>
          </Popover>
        </DirectionView>
        <Checkbox
          label="Show Nubbin"
          checked={hasNubbin}
          onPress={() => setHasNubbin(!hasNubbin)}
          UNSAFE_style={{marginTop: 10}}
        />
      </Section>
      <SpinnerOverlayWithContent />
      <SpinnerOverlayAutoClosing />
      <Header>Tooltips (Legacy Support)</Header>
      <Section space={10}>
        <Tooltip point="top">Short.</Tooltip>
        <Tooltip point="topLeft">
          This is a long tooltip that should wrap onto new lines.
        </Tooltip>
        <Tooltip removable point="bottomRight" onRemove={() => {}}>
          This is a removable tooltip that should wrap onto new lines.
        </Tooltip>
      </Section>
    </Page>
  );
};

const styles = StyleSheet.create({
  overlayBody: {
    textAlign: 'center',
    margin: 16,
  },
});
