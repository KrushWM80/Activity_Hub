import * as React from 'react';
import {StyleSheet, TextStyle, Text, View} from 'react-native';
import {
  colors,
  Skeleton,
  SkeletonVariant,
  getFont,
  Checkbox,
  TextField,
  TextFieldRef,
} from '@walmart/gtp-shared-components';

import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;

export const SkeletonPlayground: React.FC = () => {
  // ---------------
  // Rendering
  // ---------------

  const skalatonVariant = ['rectangle', 'rounded'];

  const tfRef = React.useRef<TextFieldRef | null>(null);
  type Traits = {
    variant: SkeletonVariant;
    height: string;
    width?: string;

    isOn?: boolean;
    disabled?: boolean;
    value?: boolean;
  };

  const defaultHeight = 16;
  const defaultwidth = '100%';
  const [traits, setTraits] = React.useState<Traits>({
    variant: 'rectangle',
    height: '16',
    width: '',
  });

  React.useEffect(() => {
    if (tfRef.current) {
      tfRef.current.blur();
    }
  }, [traits]);

  return (
    <View style={ss.container}>
      <View style={[ss.viewContainer]}>
        <Skeleton
          variant={traits.variant}
          height={traits.height ? parseInt(traits.height) : defaultHeight}
          width={traits.width ? parseInt(traits.width) : defaultwidth}
        />
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Skeleton traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Text style={ss.radioHeaderText}>variant</Text>
          {skalatonVariant.map((val, i) => (
            <Checkbox
              key={i}
              label={val}
              checked={traits.variant === val}
              onPress={() =>
                setTraits({
                  ...traits,
                  variant: val as SkeletonVariant,
                })
              }
            />
          ))}
          <Spacer />
          <Text style={ss.radioHeaderText}>height</Text>
          <TextField
            placeholder="Enter height here."
            label="Enter height"
            value={traits.height}
            onChangeText={txt =>
              setTraits({
                ...traits,
                height: txt as string,
              })
            }
          />

          <Spacer />
          <Text style={ss.radioHeaderText}>width</Text>
          <TextField
            placeholder="Enter width here."
            label="Enter width"
            value={traits.width}
            onChangeText={txt =>
              setTraits({
                ...traits,
                width: txt as string,
              })
            }
          />
        </View>
      </Page>
    </View>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  viewContainer: {
    backgroundColor: colors.white,
    height: 150,
    marginHorizontal: 16,
    borderRadius: 12,
    paddingVertical: 10,
    borderColor: colors.blue['90'],
    paddingHorizontal: 8,
    borderWidth: 0.5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  spacer: {
    height: 8,
  },
  innerContainer: {
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.blue['90'],
    borderTopColor: colors.blue['90'],
    borderBottomColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingHorizontal: 8,
    paddingBottom: 8,
    borderWidth: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
    borderTopColor: colors.blue['90'],
    borderLeftColor: colors.blue['90'],
    borderRightColor: colors.blue['90'],
    paddingRight: 16,
    paddingVertical: 8,
    marginTop: 8,
  },
  headerText: {
    fontSize: 20,
    fontWeight: '500',
    color: colors.blue['90'],
    textAlign: 'left',
    paddingVertical: 4,
    marginLeft: 12,
  },
  radioHeaderText: {
    ...getFont('500'),
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  } as TextStyle,
});
