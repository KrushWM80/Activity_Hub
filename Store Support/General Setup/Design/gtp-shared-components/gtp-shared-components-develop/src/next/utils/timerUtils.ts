import {jest} from '@jest/globals';
import {act} from '@testing-library/react-native';
import MockDate from 'mockdate';

const FRAME_TIME = 10;

global.requestAnimationFrame = (callback) => {
  setTimeout(callback as () => void, FRAME_TIME);
  return FRAME_TIME;
};

const advanceOneFrame = () => {
  const now = Date.now();
  MockDate.set(new Date(now + FRAME_TIME));
  act(() => {
    jest.advanceTimersByTime(FRAME_TIME);
  });
};

const timeTravel = (msToAdvance = FRAME_TIME) => {
  const numberOfFramesToRun = msToAdvance / FRAME_TIME;
  let framesElapsed = 0;

  // Step through each of the frames until we've ran them all
  while (framesElapsed < numberOfFramesToRun) {
    advanceOneFrame();
    framesElapsed++;
  }
};

export {timeTravel};
