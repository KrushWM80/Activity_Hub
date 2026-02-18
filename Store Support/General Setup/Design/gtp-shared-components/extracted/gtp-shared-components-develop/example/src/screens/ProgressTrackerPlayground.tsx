import * as React from 'react';
import {StyleSheet, TextStyle, View, Text, ViewStyle} from 'react-native';
import {
  getFont,
  Checkbox,
  colors,
  ProgressTracker,
  ProgressTrackerItem,
  ProgressTrackerVariant,
  Select,
  SelectOptions,
} from '@walmart/gtp-shared-components';
import {Page} from '../components';

const Spacer = () => <View style={ss.spacer} />;
const ProgressTrackerPlayground: React.FC = () => {
  const customStyleArr = [
    {
      label: 'customStyle1',
      val: {width: '70%', backgroundColor: colors.purple['10']},
    },
    {
      label: 'customStyle2',
      val: {width: '80%', backgroundColor: colors.gray['10']},
    },
    {
      label: 'customStyle3',
      val: {width: '90%', backgroundColor: colors.purple['10']},
    },
    {label: 'reset', val: {width: '100%', backgroundColor: 'transparent'}},
  ];

  const variantsTypes = ['error', 'info', 'success', 'warning'];
  type Traits = {
    variants?: ProgressTrackerVariant;
    activeIndex: number | undefined;
    customStyle?: string;
  };
  const [traits, setTraits] = React.useState<Traits>({
    variants: 'info',
    activeIndex: 0,
    customStyle: customStyleArr[3].label,
  });

  const activeIndexOptions: SelectOptions = [
    {text: '0', selected: true},
    {text: '1'},
    {text: '2'},
    {text: '3'},
  ];

  const getUnsafeStyle = React.useMemo(() => {
    return customStyleArr.filter(v => v.label === traits.customStyle);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [traits.customStyle]);

  return (
    <View style={ss.container}>
      <View style={ss.buttonContainer}>
        <ProgressTracker
          UNSAFE_style={getUnsafeStyle[0].val as ViewStyle}
          activeIndex={traits.activeIndex}
          variant={traits.variants}>
          <ProgressTrackerItem>Label1</ProgressTrackerItem>
          <ProgressTrackerItem>Label2</ProgressTrackerItem>
          <ProgressTrackerItem>Label3</ProgressTrackerItem>
          <ProgressTrackerItem>Label4</ProgressTrackerItem>
        </ProgressTracker>
      </View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Progress Tracker traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Spacer />
          <Text style={ss.radioHeaderText}>variants</Text>
          {variantsTypes.map(v => (
            <Checkbox
              key={String(v)}
              label={v}
              checked={v === traits.variants}
              onPress={() =>
                setTraits({
                  ...traits,
                  variants: v as ProgressTrackerVariant,
                })
              }
            />
          ))}
          <Spacer />
          <Select
            size="small"
            UNSAFE_style={{marginVertical: 8}}
            selectOptions={activeIndexOptions}
            placeholder="Select active Index"
            label={<Text style={ss.activeIndexHdr}>activeIndex</Text>}
            onChange={selected => {
              setTraits({
                ...traits,
                activeIndex: Number(selected[0].text),
              });
            }}
          />

          <Spacer />
          <Spacer />
          <Text style={ss.radioHeaderText}>UNSAFE_style (examples)</Text>
          {customStyleArr.map((v, i) => (
            <Checkbox
              key={String(i)}
              label={v.label === 'reset' ? 'reset' : JSON.stringify(v.val)}
              checked={v.label === traits.customStyle}
              onPress={() =>
                setTraits({
                  ...traits,
                  customStyle: v.label,
                })
              }
            />
          ))}
        </View>
      </Page>
    </View>
  );
};
const ss = StyleSheet.create({
  container: {
    flex: 1,
  },
  buttonContainer: {
    height: 80,
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
  activeIndexHdr: {
    fontSize: 14,
    color: colors.black,
  } as TextStyle,
});

export {ProgressTrackerPlayground};
