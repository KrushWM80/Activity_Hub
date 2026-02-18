import React from 'react';

import {colors} from '../../../src/next/utils';

type ColorKey = keyof typeof colors;
type ColorTileProps = {
  index?: number;
  key: string;
  keyName: string;
  color: string;
};
type ColorTableRowProps = {
  colorKey: ColorKey;
};

const ColorTile = (colorTileProps: ColorTileProps) => {
  const {keyName, index = 0, key, color} = colorTileProps;
  return (
    <div
      key={key}
      className="color-picker-preview-box"
      style={{
        backgroundColor: color,
        color:
          index > 10 ||
          keyName === 'high' ||
          keyName === 'max' ||
          keyName === 'base' ||
          keyName === 'black'
            ? '#fff'
            : '#000',
      }}>
      {keyName} <br></br> {`(${color})`}
    </div>
  );
};
const ColorTableRow = (colorTableRowProps: ColorTableRowProps) => {
  const {colorKey} = colorTableRowProps;
  if (colorKey === 'white' || colorKey === 'black') {
    return (
      <tr className="color-picker-table-tr">
        <td className="color-picker-table-td"> {`${colorKey}`}</td>
        <td className="color-picker-table-td">
          <ColorTile
            keyName={colorKey}
            key={colorKey}
            color={colors[colorKey]}
          />
        </td>
      </tr>
    );
  }
  const colorValues = colors[colorKey];
  return (
    <tr className="color-picker-table-tr">
      <td className="color-picker-table-td"> {`${colorKey}`}</td>
      <td className="color-picker-table-td">
        <div className="color-picker-grid-column">
          {Object.keys(colorValues).map((key, index) => {
            const keyName = key.padStart(2, '0');
            return (
              <ColorTile
                keyName={keyName}
                key={keyName}
                index={index}
                color={colorValues[key as keyof typeof colorValues]}
              />
            );
          })}
        </div>
      </td>
    </tr>
  );
};

const ColorPalette = () => {
  const colorKeys = Object.keys(colors) as Array<ColorKey>;
  return (
    <div>
      <table className="color-picker">
        {colorKeys.map((key) => {
          return <ColorTableRow key={key} colorKey={key} />;
        })}
      </table>
    </div>
  );
};

export default ColorPalette;
