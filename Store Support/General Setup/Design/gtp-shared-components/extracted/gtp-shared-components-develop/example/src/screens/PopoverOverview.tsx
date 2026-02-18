/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {View} from 'react-native';
import {
  Checkbox,
  Link,
  Popover,
  useSimpleReducer,
  delay,
} from '@walmart/gtp-shared-components';

import {Header, Page, Section, DirectionView} from '../components';

export const PopoverOverview: React.FC = () => {
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
  const [hasSpotlight, setHasSpotlight] = React.useState(false);
  const [contentChecked, setContentChecked] = React.useState(false);
  const [overrideSpotlightColor, setOverrideSpotlightColor] =
    React.useState(false);

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

  return (
    <Page>
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
            hasSpotlight={hasSpotlight}
            spotlightColor={overrideSpotlightColor ? '#ff00ff' : undefined}
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
            hasSpotlight={hasSpotlight}
            spotlightColor={overrideSpotlightColor ? '#ff00ff' : undefined}
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
            hasSpotlight={hasSpotlight}
            spotlightColor={overrideSpotlightColor ? '#ff00ff' : undefined}
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
            hasSpotlight={hasSpotlight}
            spotlightColor={overrideSpotlightColor ? '#ff00ff' : undefined}
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
            hasSpotlight={hasSpotlight}
            spotlightColor={overrideSpotlightColor ? '#ff00ff' : undefined}
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
            hasSpotlight={hasSpotlight}
            spotlightColor={overrideSpotlightColor ? '#ff00ff' : undefined}
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
            hasSpotlight={hasSpotlight}
            spotlightColor={overrideSpotlightColor ? '#ff00ff' : undefined}
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
            hasSpotlight={hasSpotlight}
            spotlightColor={overrideSpotlightColor ? '#ff00ff' : undefined}
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
        <Checkbox
          label="Show Spotlight"
          checked={hasSpotlight}
          onPress={() => setHasSpotlight(!hasSpotlight)}
          UNSAFE_style={{marginTop: 10}}
        />
        <Checkbox
          label="Override Spotlight Color"
          checked={overrideSpotlightColor}
          onPress={() => setOverrideSpotlightColor(!overrideSpotlightColor)}
          UNSAFE_style={{marginTop: 10}}
        />
      </Section>
    </Page>
  );
};
