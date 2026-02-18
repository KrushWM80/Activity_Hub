import * as React from 'react';
import {StyleSheet, Text, View, TextStyle} from 'react-native';
import {
  colors,
  getFont,
  Checkbox,
  Icons,
  TextField,
} from '@walmart/gtp-shared-components';

import {
  FilterTriggerAll,
  FilterTriggerSingle,
  FilterToggle,
  FilterTag,
} from '@walmart/gtp-shared-components/ax';

// import type {FilterSize} from '@walmart/gtp-shared-components/ax';

import {Page, RadioGroup} from '../components';

const Spacer = () => <View style={ss.spacer} />;

export const FilterPlayground: React.FC = () => {
  const [filterType, setFilterType] = React.useState('FilterTriggerAll');
  const [label, setLabel] = React.useState('Filters');
  // TODO: Add large size when LD specs are finalized
  // const [size, setSize] = React.useState<FilterSize>('small');
  const [appliedCount, setAppliedCount] = React.useState(null);
  const [hasLeading, setHasLeading] = React.useState(false);
  const [disabled, setDisabled] = React.useState(false);
  const [isOpen, setIsOpen] = React.useState(false);
  const [isApplied, setIsApplied] = React.useState(false);

  const renderFilter = (type: string) => {
    switch (type) {
      case 'FilterTriggerAll':
        return (
          <FilterTriggerAll
            // size={size}
            appliedCount={appliedCount}
            disabled={disabled}>
            {label}
          </FilterTriggerAll>
        );
      case 'FilterTriggerSingle':
        return (
          <FilterTriggerSingle
            // size={size}
            leading={hasLeading ? <Icons.TruckIcon /> : undefined}
            isApplied={isApplied}
            isOpen={isOpen}
            disabled={disabled}>
            {label}
          </FilterTriggerSingle>
        );
      case 'FilterToggle':
        return (
          <FilterToggle
            // size={size}
            leading={hasLeading ? <Icons.TruckIcon /> : undefined}
            isApplied={isApplied}
            disabled={disabled}>
            {label}
          </FilterToggle>
        );
      case 'FilterTag':
        return (
          <FilterTag
            // size={size}
            disabled={disabled}>
            {label}
          </FilterTag>
        );
      default:
        return null;
    }
  };

  return (
    <View style={ss.container}>
      <View style={ss.previewContainer}>{renderFilter(filterType)}</View>

      <Page>
        <View style={ss.header}>
          <Text style={ss.headerText}>Filter traits</Text>
        </View>
        <View style={ss.innerContainer}>
          <Text style={ss.radioHeaderText}>component</Text>
          <Spacer />
          <RadioGroup
            category="size"
            list={[
              'FilterTriggerAll',
              'FilterTriggerSingle',
              'FilterToggle',
              'FilterTag',
            ]}
            selected="FilterTriggerAll"
            onChange={(_, sel) => setFilterType(sel)}
          />
          {/* TODO: Add large size when LD specs are finalized */}
          {/* <Text style={ss.radioHeaderText}>size</Text>
          <Spacer />
          <RadioGroup
            category="size"
            list={['small', 'large']}
            selected="small"
            onChange={(_, sel) => setSize(sel as FilterSize)}
          /> */}
          <Spacer />
          <Text style={ss.radioHeaderText}>appliedCount</Text>
          <RadioGroup
            disabled={
              filterType !== 'FilterTriggerAll'
                ? ['N/A', '1', '2', '3', '4', '5']
                : []
            }
            category="value"
            orientation="horizontal"
            list={['N/A', '1', '2', '3', '4', '5']}
            selected="none"
            onChange={(_: any, sel: any) => {
              if (sel === 'N/A') {
                setAppliedCount(null);
              } else {
                setAppliedCount(sel);
              }
            }}
          />
          <Spacer />
          <Text style={ss.radioHeaderText}>children</Text>
          <TextField
            label="text label"
            size="small"
            value={label}
            onChangeText={_text => setLabel(_text as string)}
          />
          <Spacer />
          <Checkbox
            label="with leading icon"
            disabled={
              filterType !== 'FilterTriggerSingle' &&
              filterType !== 'FilterToggle'
            }
            checked={hasLeading}
            onPress={() => {
              setHasLeading(prev => {
                return !prev;
              });
            }}
          />
          <Spacer />
          <Checkbox
            label="isApplied"
            disabled={
              filterType !== 'FilterTriggerSingle' &&
              filterType !== 'FilterToggle'
            }
            checked={isApplied}
            onPress={() =>
              setIsApplied(prev => {
                return !prev;
              })
            }
          />
          <Spacer />
          <Checkbox
            label="isOpen"
            disabled={filterType !== 'FilterTriggerSingle'}
            checked={isOpen}
            onPress={() =>
              setIsOpen(prev => {
                return !prev;
              })
            }
          />
          <Spacer />
          <Checkbox
            label="disabled"
            checked={disabled}
            onPress={() =>
              setDisabled(prev => {
                return !prev;
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
  previewContainer: {
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
});
