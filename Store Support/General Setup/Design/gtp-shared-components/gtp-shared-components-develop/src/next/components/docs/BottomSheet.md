### with small text content

```js
import * as React from 'react';
import {BottomSheet, Button, ButtonGroup} from '@walmart/gtp-shared-components';
import {loremIpsum} from '../../../../example/src/screens/screensFixtures.tsx';

const [modalIsOpen, setModalIsOpen] = React.useState(false);
const handleModalOnClosed = () => {};
const openModal = () => {
  setModalIsOpen(true);
};
const handleModalOnClose = () => {
  setModalIsOpen(false);
};
const handleModalCancel = () => {
  setModalIsOpen(false);
};
const handleModalContinue = () => {
  setModalIsOpen(false);
};

<>
  <Button variant="primary" onPress={openModal}>
    Show
  </Button>
  <BottomSheet
    showCloseHandle
    isOpen={modalIsOpen}
    onClose={handleModalOnClose}
    onClosed={handleModalOnClosed}
    title="Confirmation"
    actions={
      <ButtonGroup>
        <Button variant="tertiary" onPress={handleModalCancel}>
          Cancel
        </Button>
        <Button variant="primary" onPress={handleModalContinue}>
          Continue
        </Button>
      </ButtonGroup>
    }>
    {loremIpsum(1)}
  </BottomSheet>
</>
```

### with large text content

```js
import * as React from 'react';
import {BottomSheet, Button, ButtonGroup} from '@walmart/gtp-shared-components';
import {loremIpsum} from '../../../../example/src/screens/screensFixtures.tsx';

const [modalIsOpen, setModalIsOpen] = React.useState(false);
const handleModalOnClosed = () => {};
const openModal = () => {
  setModalIsOpen(true);
};
const handleModalOnClose = () => {
  setModalIsOpen(false);
};
const handleModalCancel = () => {
  setModalIsOpen(false);
};
const handleModalContinue = () => {
  setModalIsOpen(false);
};

<>
  <Button variant="primary" onPress={openModal}>
    Show
  </Button>
  <BottomSheet
    showCloseHandle
    isOpen={modalIsOpen}
    onClose={handleModalOnClose}
    onClosed={handleModalOnClosed}
    title="Confirmation"
    actions={
      <ButtonGroup>
        <Button variant="tertiary" onPress={handleModalCancel}>
          Cancel
        </Button>
        <Button variant="primary" onPress={handleModalContinue}>
          Continue
        </Button>
      </ButtonGroup>
    }>
    {loremIpsum(20)}
  </BottomSheet>
</>
```

### with mixed content

```js
import * as React from 'react';
import {StyleSheet,Image, View} from 'react-native';
import {Button, Body, Divider} from  '@walmart/gtp-shared-components';
import {loremIpsum} from '../../../../example/src/screens/screensFixtures.tsx';

const [modalIsOpen, setModalIsOpen] = React.useState(false);
const handleModalOnClosed = () => {};
const openModal = () => {
  setModalIsOpen(true);
};
const handleModalOnClose = () => {
  setModalIsOpen(false);
};

const ss = StyleSheet.create({
  button: {
    margin: 8,
    width: '60%',
    alignSelf: 'center',
  },
});

<>
  <Button variant="primary" onPress={openModal}>
    Show
  </Button>
  <BottomSheet
    showCloseHandle
    isOpen={modalIsOpen}
    onClose={handleModalOnClose}
    onClosed={handleModalOnClosed}
    title="Confirmation">
      <View style={{margin: 16}}>
      <Body>
        <Body weight="medium">You won’t get NextDay delivery</Body> on this order
        because your cart contains item(s) that aren’t “NextDay eligible.” If you
        want NextDay, we can save the other items for later.
      </Body>
      <Button
        UNSAFE_style={ss.button}
        variant="primary"
        isFullWidth
        onPress={handleModalOnClose}>
        Yes—Save my other items for later
      </Button>
      <Button
        UNSAFE_style={ss.button}
        variant="secondary"
        isFullWidth
        onPress={handleModalOnClose}>
        No—I want to keep shopping
      </Button>
      <Divider />
      <Body UNSAFE_style={ss.body}>For example:</Body>
      <Body>
        <Body weight="medium" style={ss.body}>
          NextDay
        </Body>{' '}
        +
        <Body weight="medium" style={ss.body}>
          {' '}
          NextDay
        </Body>{' '}
        =
        <Body weight="medium" style={ss.body}>
          {' '}
          NextDay
        </Body>
        !
      </Body>
      <Body>
        <Body weight="medium" style={ss.body}>
          NextDay
        </Body>{' '}
        +
        <Body weight="medium" style={ss.normal}>
          {' '}
          2Day
        </Body>{' '}
        =
        <Body weight="medium">
          <Body UNSAFE_style={ss.normal}> 2Day</Body> on entire order
        </Body>
      </Body>
      <Divider />
      <View style={{flexDirection: 'row', marginTop: 16}}>
      <Image
        source={{
          uri: 'https://gecgithub01.walmart.com/storage/user/67415/files/f9a3519d-45a9-437a-b41c-27d6cd1152b1',
          height: 400,
          width: 400,
          }}
        style={{marginRight: 16}}
        />
      <Body weight="medium">
        {loremIpsum(3)}
      </Body>
      </View>
    </View>
  </BottomSheet>
</>
```

### with back button
Note: this is not recommended to be used. There is an LD ticket in the backlog to investigate this: https://jira.walmart.com/browse/LD-1829
Added because of popular demand (e.g. CustomerTransaction/Returns team).

```js
import * as React from 'react';
import {StyleSheet, View, Text} from 'react-native';
import {BottomSheet, Button, ButtonGroup, getFont, IconButton, ChevronLeftIcon} from '@walmart/gtp-shared-components';
import {loremIpsum} from '../../../../example/src/screens/screensFixtures.tsx';

const [modalIsOpen, setModalIsOpen] = React.useState(false);
const handleModalOnClosed = () => {};
const openModal = () => {
  setModalIsOpen(true);
};
const handleModalOnClose = () => {
  setModalIsOpen(false);
};
const handleModalCancel = () => {
  setModalIsOpen(false);
};
const handleModalContinue = () => {
  setModalIsOpen(false);
};

const ss = StyleSheet.create({
  titleContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingRight: '27%',
  },
  title: {
    ...getFont('700'),
    fontSize: 18,
    lineHeight: 24,
    textAlign: 'center',
    color: '#2e2f32',
  },
  iconButton: {
    marginLeft: -12,
  },
});

<>
  <Button variant="primary" onPress={openModal}>
    Show
  </Button>
  <BottomSheet
    showCloseHandle
    isOpen={modalIsOpen}
    onClose={handleModalOnClose}
    onClosed={handleModalOnClosed}
    title={
      <View style={ss.titleContainer}>
        <IconButton
          size="large"
          onPress={() => console.log("Modal action 'Back' was tapped")}
          UNSAFE_style={ss.iconButton}>
           <ChevronLeftIcon />
        </IconButton>
        <Text style={ss.title}>Confirmation</Text>
      </View>
    }
    actions={
      <ButtonGroup>
        <Button variant="tertiary" onPress={handleModalCancel}>
          Cancel
        </Button>
        <Button variant="primary" onPress={handleModalContinue}>
          Continue
        </Button>
      </ButtonGroup>
    }>
    {loremIpsum(20)}
  </BottomSheet>
</>
```