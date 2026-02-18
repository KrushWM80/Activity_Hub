import * as utils from '../';

test('Test resolveNubbinAlignmentStyle', () => {
  const bottomRight = utils.resolveNubbinAlignmentStyle('bottomRight');
  expect(bottomRight).toEqual({alignItems: 'flex-start'});
  const bottomCenter = utils.resolveNubbinAlignmentStyle('bottomCenter');
  expect(bottomCenter).toEqual({alignItems: 'center'});
  const bottomLeft = utils.resolveNubbinAlignmentStyle('bottomLeft');
  expect(bottomLeft).toEqual({alignItems: 'flex-end'});

  const right = utils.resolveNubbinAlignmentStyle('right');
  expect(right).toEqual({
    flexDirection: 'row',
    alignItems: 'center',
  });
  const left = utils.resolveNubbinAlignmentStyle('left');
  expect(left).toEqual({
    flexDirection: 'row-reverse',
    alignItems: 'center',
  });

  const topRight = utils.resolveNubbinAlignmentStyle('topRight');
  expect(topRight).toEqual({
    flexDirection: 'column-reverse',
    alignItems: 'flex-start',
  });
  const topCenter = utils.resolveNubbinAlignmentStyle('topCenter');
  expect(topCenter).toEqual({
    flexDirection: 'column-reverse',
    alignItems: 'center',
  });
  const topLeft = utils.resolveNubbinAlignmentStyle('topLeft');
  expect(topLeft).toEqual({
    flexDirection: 'column-reverse',
    alignItems: 'flex-end',
  });
});

describe('Test resolvedPositionStyle', () => {
  test('nubbin undefined', () => {
    const bottomRight = utils.resolvePopUpPositionStyle(
      'bottomRight',
      150,
      340,
      30,
      30,
      20,
      20,
      20,
    );
    expect(bottomRight).toEqual({left: 165, top: 390});
    const bottomLeft = utils.resolvePopUpPositionStyle(
      'bottomLeft',
      150,
      340,
      30,
      30,
      20,
      20,
      20,
    );
    expect(bottomLeft).toEqual({left: 145, top: 390});
    const topRight = utils.resolvePopUpPositionStyle(
      'topRight',
      150,
      340,
      30,
      30,
      20,
      20,
      20,
    );
    expect(topRight).toEqual({left: 165, top: 300});
    const topLeft = utils.resolvePopUpPositionStyle(
      'topLeft',
      150,
      340,
      30,
      30,
      20,
      20,
      20,
    );
    expect(topLeft).toEqual({left: 145, top: 300});
  });

  test('nubbin values 0', () => {
    const style = utils.resolvePopUpPositionStyle(
      'bottomLeft',
      150,
      340,
      30,
      30,
      20,
      20,
      20,
      0,
      0,
    );
    expect(style).toEqual({left: 145, top: 390});
  });
  test('nubbin exist', () => {
    const bottomRight = utils.resolvePopUpPositionStyle(
      'bottomRight',
      150,
      340,
      30,
      30,
      20,
      20,
      20,
      50,
      50,
    );
    expect(bottomRight).toEqual({left: 90, top: 390});
    const bottomLeft = utils.resolvePopUpPositionStyle(
      'bottomLeft',
      150,
      340,
      30,
      30,
      20,
      20,
      20,
      50,
      50,
    );
    expect(bottomLeft).toEqual({left: 220, top: 390});
    const topRight = utils.resolvePopUpPositionStyle(
      'topRight',
      150,
      340,
      30,
      30,
      20,
      20,
      20,
      50,
      50,
    );
    expect(topRight).toEqual({left: 90, top: 300});
    const topLeft = utils.resolvePopUpPositionStyle(
      'topLeft',
      150,
      340,
      30,
      30,
      20,
      20,
      20,
      50,
      50,
    );
    expect(topLeft).toEqual({left: 220, top: 300});
  });
});

describe('Test calculateMenuPosition', () => {
  //example S.W=390 and S.H=844
  const screenWidth = 390;
  const screenHeight = 844;
  test('it returns bottomRight when pagX<S.W/2 and pageY>S.H/4 ', () => {
    expect(
      utils.calculateMenuPosition(screenWidth, screenHeight, 150, 233),
    ).toEqual('bottomRight');
  });
  test('it returns topRight when pagX<S.W/2 and pageY<S.H/4 ', () => {
    expect(
      utils.calculateMenuPosition(screenWidth, screenHeight, 150, 703),
    ).toEqual('topRight');
  });
  test('it returns bottomLeft when pagX>S.W/2 and pageY>S.H/4 ', () => {
    expect(
      utils.calculateMenuPosition(screenWidth, screenHeight, 250, 233),
    ).toEqual('bottomLeft');
  });
  test('it returns bottomRight when pagX>S.W/2 and pageY<S.H/4 ', () => {
    expect(
      utils.calculateMenuPosition(screenWidth, screenHeight, 250, 703),
    ).toEqual('topLeft');
  });
});

describe('Test resolveSpotlightContainerStyle', () => {
  test('should return empty object if childrenLayout is undefined', () => {
    const result = utils.resolveSpotlightContainerStyle(
      'topRight',
      undefined,
      10,
      5,
    );
    expect(result).toEqual({});
  });

  test('should return empty object if childrenLayout.width is undefined', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: undefined};
    const result = utils.resolveSpotlightContainerStyle(
      'topRight',
      //@ts-ignore
      childrenLayout,
      10,
      5,
    );
    expect(result).toEqual({});
  });

  test('should return empty object if nubbinWidth is undefined', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: 200};
    const result = utils.resolveSpotlightContainerStyle(
      'topRight',
      childrenLayout,
      //@ts-ignore
      undefined,
      5,
    );
    expect(result).toEqual({});
  });

  test('should return empty object if nubbinOffset is undefined', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: 200};
    const result = utils.resolveSpotlightContainerStyle(
      'topRight',
      childrenLayout,
      10,
      //@ts-ignore
      undefined,
    );
    expect(result).toEqual({});
  });

  test('should return correct style for bottomRight position', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: 200};
    const result = utils.resolveSpotlightContainerStyle(
      'bottomRight',
      childrenLayout,
      10,
      5,
    );
    expect(result).toEqual({
      marginLeft: 90,
      marginBottom: 4,
      marginRight: 0,
      marginTop: 0,
    });
  });

  test('should return correct style for bottomCenter position', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: 200};
    const result = utils.resolveSpotlightContainerStyle(
      'bottomCenter',
      childrenLayout,
      10,
      5,
    );
    expect(result).toEqual({
      marginBottom: 4,
      marginRight: 0,
      marginLeft: 0,
      marginTop: 0,
    });
  });

  test('should return correct style for bottomLeft position', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: 200};
    const result = utils.resolveSpotlightContainerStyle(
      'bottomLeft',
      childrenLayout,
      10,
      5,
    );
    expect(result).toEqual({
      marginRight: 90,
      marginBottom: 4,
      marginLeft: 0,
      marginTop: 0,
    });
  });

  test('should return correct style for topRight position', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: 200};
    const result = utils.resolveSpotlightContainerStyle(
      'topRight',
      childrenLayout,
      10,
      5,
    );
    expect(result).toEqual({
      marginLeft: 90,
      marginTop: 4,
      marginRight: 0,
      marginBottom: 0,
    });
  });

  test('should return correct style for topLeft position', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: 200};
    const result = utils.resolveSpotlightContainerStyle(
      'topLeft',
      childrenLayout,
      10,
      5,
    );
    expect(result).toEqual({
      marginRight: 90,
      marginTop: 4,
      marginBottom: 0,
      marginLeft: 0,
    });
  });

  test('should return correct style for topCenter position', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: 200};
    const result = utils.resolveSpotlightContainerStyle(
      'topCenter',
      childrenLayout,
      10,
      5,
    );
    expect(result).toEqual({
      marginTop: 4,
      marginBottom: 0,
      marginLeft: 0,
      marginRight: 0,
    });
  });

  test('should return correct style for left position', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: 200};
    const result = utils.resolveSpotlightContainerStyle(
      'left',
      childrenLayout,
      10,
      5,
    );
    expect(result).toEqual({
      marginBottom: 0,
      marginLeft: 4,
      marginRight: 0,
      marginTop: 0,
    });
  });

  test('should return correct style for right position', () => {
    const childrenLayout = {x: 0, y: 0, height: 0, width: 200};
    const result = utils.resolveSpotlightContainerStyle(
      'right',
      childrenLayout,
      10,
      5,
    );
    expect(result).toEqual({
      marginBottom: 0,
      marginLeft: 0,
      marginRight: 4,
      marginTop: 0,
    });
  });
});
