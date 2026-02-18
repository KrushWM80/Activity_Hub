// @ts-nocheck
import React from 'react';

import {Caption} from '@walmart/gtp-shared-components';

const styles = StyleSheet.create({
    caption: {
      height: 16,
      paddingHorizontal: 8,
      marginTop: 8,
    },
});

const captionProps = {
  weight: '400',
  UNSAFE_style: styles.caption,
};

<Caption {...captionProps}>...</Caption>
