/* eslint-disable react-native/no-inline-styles */
import * as React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {Link, Popover, useSimpleReducer} from '@walmart/gtp-shared-components';

import {Header, Page, Section, VariantText} from '../components';

const Spacer = () => <View style={ss.spacer} />;

export const PopoverRecipes: React.FC = () => {
  type PopoverOpenState = {
    defaultPopover: boolean;
    directionalPopover: boolean;
    directionalNubbinPopover: boolean;
  };

  const [popoverState, setPopoverState] = useSimpleReducer<PopoverOpenState>({
    defaultPopover: false,
    directionalPopover: false,
    directionalNubbinPopover: false,
  });

  const defaultPopover = () => {
    return (
      <>
        <Header>
          Popover (default){'\n  '}
          <VariantText>{`<Popover \n\t content={<Text>Popover text</Text>} \n\t isOpen={true} \n\t onClose={closeHandler}> \n\t\t <Link onPress={popoverHandler}> \n\t\t\t\t link \n\t\t </Link> \n</Popover>`}</VariantText>
        </Header>
        <Section space={10}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Popover
              content={<Text>Popover text here.</Text>}
              isOpen={popoverState.defaultPopover as boolean}
              onClose={() =>
                setPopoverState(
                  'defaultPopover',
                  !(popoverState.defaultPopover as boolean),
                )
              }>
              <Link
                onPress={() =>
                  setPopoverState(
                    'defaultPopover',
                    !(popoverState.defaultPopover as boolean),
                  )
                }>
                Popover
              </Link>
            </Popover>
          </View>
        </Section>
      </>
    );
  };

  const directionalPopover = () => {
    return (
      <>
        <Header>
          Popover (with hasNubbin=false and position='right'){'\n  '}
          <VariantText>{`<Popover \n\t content={<Text>Popover text</Text>} \n\t isOpen={true} \n\t onClose={closeHandler} \n\t hasNubbin={false} \n\t position="right"> \n\t\t <Link onPress={popoverHandler}> \n\t\t\t\t link \n\t\t </Link> \n</Popover>`}</VariantText>
        </Header>
        <Section space={10}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Popover
              content={<Text>Popover text here.</Text>}
              isOpen={popoverState.directionalPopover as boolean}
              onClose={() =>
                setPopoverState(
                  'directionalPopover',
                  !(popoverState.directionalPopover as boolean),
                )
              }
              hasNubbin={false}
              position="right">
              <Link
                onPress={() =>
                  setPopoverState(
                    'directionalPopover',
                    !(popoverState.directionalPopover as boolean),
                  )
                }>
                popover
              </Link>
            </Popover>
          </View>
        </Section>
      </>
    );
  };

  const directionalNubbinPopover = () => {
    return (
      <>
        <Header>
          Popover (with hasNubbin=true and position='topRight'){'\n  '}
          <VariantText>{`<Popover \n\t content={<Text>Popover text</Text>} \n\t isOpen={true} \n\t onClose={closeHandler} \n\t hasNubbin={true} \n\t position="topRight"> \n\t\t <Link onPress={popoverHandler}> \n\t\t\t\t link \n\t\t </Link> \n</Popover>`}</VariantText>
        </Header>
        <Section space={10}>
          <View style={ss.innerContainer}>
            <Spacer />
            <Popover
              content={<Text>Popover text here.</Text>}
              isOpen={popoverState.directionalNubbinPopover as boolean}
              onClose={() =>
                setPopoverState(
                  'directionalNubbinPopover',
                  !(popoverState.directionalNubbinPopover as boolean),
                )
              }
              hasNubbin={true}
              position="topRight">
              <Link
                onPress={() =>
                  setPopoverState(
                    'directionalNubbinPopover',
                    !(popoverState.directionalNubbinPopover as boolean),
                  )
                }>
                Popover
              </Link>
            </Popover>
          </View>
        </Section>
      </>
    );
  };

  return (
    <Page>
      {defaultPopover()}
      {directionalPopover()}
      {directionalNubbinPopover()}
    </Page>
  );
};

const ss = StyleSheet.create({
  overlayBody: {
    textAlign: 'center',
    margin: 16,
  },
  innerContainer: {
    padding: 10,
    alignItems: 'center',
    justifyContent: 'center',
  },
  spacer: {
    height: 8,
  },
});
