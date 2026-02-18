import * as React from 'react';

import {SnackbarContext} from '../components/SnackbarProvider';

/**
 * The `useSnackbar` hook provides a function called `addSnack` which allows you to render
 * a `Snackbar` component anywhere in the app on top of all other content.
 * The `LivingDesignProvider` must be added to the application's root to be able to use `useSnack` and `addSnack`.
 *
 * ## Usage
 * ```js
 * // at the top level
 * import {LivingDesignProvider} from '@walmart/gtp-shared-components';
 *
 * <LivingDesignProvider>
 *  <App />
 * </LivingDesignProvider>
 *
 * // at the component level
 * import {useSnackbar} from '@walmart/gtp-shared-components`;
 *
 * const {addSnack} = useSnackbar();
 *
 * <Button
 *   onPress={() =>
 *     addSnack({
 *       message: 'A snack with action button',
 *       actionButton: {
 *         caption: 'Action',
 *         onPress: () => {
 *           Alert.alert('Action Button pressed');
 *         },
 *       },
 *       onClose: () => {},
 *       customPosition: '25%', // optionally you can pass a custom vertical position
                                // it can be an absolute number (e.g. 200) or a percent (e.g 25%) of the screen height
                                // measured from the bottom of the screen.
 *     })
 *   }>
 *   Add Snack w/ Action Button
 * </Button>
 * ```
 */
export const useSnackbar = () => React.useContext(SnackbarContext);
