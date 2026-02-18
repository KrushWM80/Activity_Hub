/* global global */

/**
 * Setup
 *
 * {@link https://react-styleguidist.js.org/docs/cookbook.html#how-to-hide-some-components-in-style-guide-but-make-them-available-in-examples}
 */

import {View} from 'react-native';
import './add-version';
import {Palette} from './palette';
import IconWrapper from './icon-wrapper';
import HorizontalContainer from './horizontal-container';

global.View = View;
global.Palette = Palette;
global.IconWrapper = IconWrapper;
global.HorizontalContainer = HorizontalContainer;
