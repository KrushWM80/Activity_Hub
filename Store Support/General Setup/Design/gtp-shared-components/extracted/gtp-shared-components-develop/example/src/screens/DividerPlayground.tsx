import * as React from 'react';
import {Page} from '../components';
import {Checkbox, Divider, colors} from '@walmart/gtp-shared-components';
import {StyleSheet, Text, View} from 'react-native';

const Spacer = () => <View style={ss.spacer} />;
export const DividerPlayground: React.FC = () => {
  const dividerColor = [
    {backgroundColor: '#b36a16', height: 2},
    {backgroundColor: '#590b0e', height: 4},
    {backgroundColor: '#004f9a', height: 6},
    {backgroundColor: '#1d5f02', height: 8},
    {backgroundColor: '#661648', height: 1},
  ];
  const [styleVal, setStyleVal] = React.useState(0);
  // ---------------
  // Rendering
  // ---------------
  return (
    <Page>
      <View style={ss.viewContainer}>
        <Divider
          UNSAFE_style={{
            backgroundColor: dividerColor[styleVal].backgroundColor,
            height: dividerColor[styleVal].height,
          }}
        />
      </View>
      <View style={ss.header}>
        <Text style={ss.headerText}>Divider traits</Text>
      </View>
      <View style={ss.innerContainer}>
        <Spacer />
        <View>
          <Text style={ss.radioHeaderText}>UNSAFE_style</Text>
          <Text style={ss.radioInfoText}>(examples)</Text>
        </View>
        {dividerColor.map((v, i) => (
          <Checkbox
            key={i}
            label={JSON.stringify(v)}
            checked={i == styleVal}
            onPress={() => setStyleVal(i)}
          />
        ))}
      </View>
    </Page>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  viewContainer: {
    flex: 1,
    borderWidth: 0.5,
    borderColor: colors.blue['90'],
    paddingHorizontal: 10,
    paddingVertical: 40,
    backgroundColor: 'transparent',
    borderRadius: 15,
    marginBottom: 40,
  },
  buttonContainer: {
    height: 80,
    marginHorizontal: 16,
    borderRadius: 12,
    borderColor: colors.blue['90'],
    paddingHorizontal: 10,
    paddingVertical: 40,
    borderWidth: 0.5,
    justifyContent: 'center',
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
  spacer: {
    height: 8,
  },
  headerVariantText: {
    color: colors.blue['90'],
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
    lineHeight: 28,
    fontSize: 20,
    color: colors.blue['90'],
  },
  traitsLeft: {
    flex: 0.5,
    borderRightWidth: 1,
    borderRightColor: colors.blue['90'],
    paddingBottom: 8,
  },
  radioInfoText: {
    lineHeight: 28,
    fontSize: 12,
    color: colors.blue['70'],
  },
});
