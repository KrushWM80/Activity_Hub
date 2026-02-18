Modals focus the user’s attention on a single task in a window that sits on top of the page content.

```js
import * as React from 'react';
import {Modal, Button, ButtonGroup} from '@walmart/gtp-shared-components';

const [modalIsOpen, setModalIsOpen] = React.useState(false);
const [modalActionPressed, setModalActionPressed] = React.useState('');
const [modalSize, setModalSize] = React.useState('auto');
  const openModal = (modalType) => {
    setModalIsOpen(true);
    setModalSize(modalType)
    setModalActionPressed('');
  };

  const handleModalOnClose = () => {
    setModalIsOpen(false);
  };

  const handleModalCancel = () => {
    setModalActionPressed('Cancel');
    setModalIsOpen(false);
  };

  const handleModalContinue = () => {
    setModalActionPressed('Continue');
    setModalIsOpen(false);
  };

  const handleModalOnClosed = () => {
    if (modalActionPressed !== '') {
      console.log(`Modal action '${modalActionPressed}' was tapped`);
    }
  };


<>
  <Button variant="primary" onPress={()=>openModal('small')}>
    Show Modal Small
  </Button>
   <Button variant="primary" UNSAFE_style={{marginTop:10}} onPress={()=>openModal('medium')}>
    Show Modal Medium
  </Button>
   <Button variant="primary" UNSAFE_style={{marginTop:10}} onPress={()=>openModal('large')}>
    Show Modal Large
  </Button>
   <Button variant="primary"  UNSAFE_style={{marginTop:10}} onPress={()=>openModal('auto')}>
    Show Modal Auto
  </Button>
  <Modal
    isOpen={modalIsOpen}
    onClose={handleModalOnClose}
    onClosed={handleModalOnClosed}
    title="Confirmation"
    size={modalSize}
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
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
    tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
    veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
    commodo consequat.
  </Modal>
</>
```
