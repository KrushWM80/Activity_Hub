/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {Text, View} from 'react-native';
import {Header, Page, Section, DirectionView} from '../components';
import {Callout, Link, useSimpleReducer} from '@walmart/gtp-shared-components';

export const CalloutOverview: React.FC = () => {
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
    </Page>
  );
};
