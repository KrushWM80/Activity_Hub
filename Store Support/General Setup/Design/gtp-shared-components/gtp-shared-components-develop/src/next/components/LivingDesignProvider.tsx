import * as React from 'react';

import type {CommonViewProps} from '../types/ComponentTypes';

import {SnackbarProvider} from './SnackbarProvider';

export type LivingDesignProviderProps = CommonViewProps & {
  /**
   * The content for the living design provider.
   */
  children?: React.ReactNode;
};

/**
 * A utility component that contains all the required React Native providers.
 * This provider currently adds only Snackbar to your app, however, it will
 * be used to include more providers in the future.
 * NOTE: use this provider to wrap your app at the top level. Caveat for Me@Walmart miniapp developers:
 * make sure this provider only exists at the composite (core) level, not at the miniapp level.
 * (see: https://jira.walmart.com/browse/CEEMP-2883)
 *
 * ## Usage
 * ```js
 * import {LivingDesignProvider} from '@walmart/gtp-shared-components`;
 *
 * <LivingDesignProvider>
 *   <App />
 * </LivingDesignProvider>
 * ```
 */
export const LivingDesignProvider: React.FC<LivingDesignProviderProps> = (
  props,
) => {
  const {children} = props;

  return <SnackbarProvider>{children}</SnackbarProvider>;
};
