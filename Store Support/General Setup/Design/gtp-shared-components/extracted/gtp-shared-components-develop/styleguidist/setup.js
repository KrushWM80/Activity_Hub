/* global global */

/**
 * Setup
 *
 * {@link https://react-styleguidist.js.org/docs/cookbook.html#how-to-hide-some-components-in-style-guide-but-make-them-available-in-examples}
 */

import {View} from 'react-native';
import './addVersion';
import {Palette} from './palette';
import {IconWrapper} from './IconWrapper';
import {HorizontalContainer} from './HorizontalContainer';
import {Controller} from '../example/src/components';

global.View = View;
global.Palette = Palette;
global.IconWrapper = IconWrapper;
global.HorizontalContainer = HorizontalContainer;
global.Controller = Controller;
