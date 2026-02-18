// @ts-nocheck
import React from 'react';

import {Caption as Test} from '@walmart/gtp-shared-components/dist';

<Test UNSAFE_style={styles.caption}>{key.replace(/Icon/, '')}</Test>;

const styles = StyleSheet.create({
    caption: {
      height: 16,
      paddingHorizontal: 8,
      marginTop: 8,
    },
});
