import * as React from 'react';
import {StyleSheet, Text, TextStyle, View} from 'react-native';

import {colors as Colors, colorVariants} from '../utils/colors';

/**
 * This is an internal component used in ColorsScreen and icons.md
 * It displays color stripes, one stripe per color variant
 *
 * ```js
 * import {_ColorPalette} from '@walmart/gtp-shared-components`;
 * ```
 * @internal
 */
const _ColorPalette: React.FC = () => {
  const colors = Object.keys(Colors)
    .map((key) => {
      if (colorVariants.includes(key)) {
        return {
          colorName: key,
          variants: Colors[key as keyof typeof Colors],
        };
      }
    })
    .filter((u) => u !== undefined);

  // ---------------
  // Rendering
  // ---------------
  return (
    <>
      {colors.map((colorObj, outerIndex) => {
        const {colorName, variants}: Partial<typeof colorObj> = colorObj!;
        if (typeof colorObj!.variants === 'object') {
          return Object.keys(variants).map((key, index) => {
            const hexValue = variants[key as keyof typeof colorObj];
            const textColor: string = `${100 - index * 10}`;
            return (
              <View key={`${colorName}-${index}`} style={ss.colorRow}>
                <Text
                  style={[
                    ss.colorText,
                    {
                      color:
                        index < 4
                          ? Colors.gray[textColor as keyof typeof Colors.gray]
                          : Colors.white,
                    } as TextStyle,
                    {backgroundColor: hexValue},
                  ]}>{`${
                  'Colors.' + colorObj!.colorName
                }[${key}] (${hexValue})`}</Text>
              </View>
            );
          });
        } else {
          const hexVal = colorObj?.variants;
          return (
            <View key={`${colorName}-${outerIndex}`} style={ss.colorRow}>
              <Text
                style={[
                  ss.colorText,
                  {backgroundColor: hexVal as string},
                ]}>{`Colors.${colorName} (${hexVal})`}</Text>
            </View>
          );
        }
      })}
    </>
  );
};

// ---------------
// Styles
// ---------------
const ss = StyleSheet.create({
  colorRow: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  colorText: {
    fontWeight: 'bold',
    width: '100%',
    lineHeight: 40,
    fontSize: 14,
    color: Colors.gray[100],
  },
  colorStripe: {
    height: 40,
    width: 200,
  },
});

_ColorPalette.displayName = '_ColorPalette';
export {_ColorPalette};
