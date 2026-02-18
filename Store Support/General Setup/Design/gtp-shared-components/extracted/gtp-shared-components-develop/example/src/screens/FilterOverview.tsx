import * as React from 'react';
import {SafeAreaView, View, StyleSheet} from 'react-native';
import {Icons} from '@walmart/gtp-shared-components';
import {
  FilterTriggerAll,
  FilterTriggerSingle,
  FilterToggle,
  FilterTag,
} from '@walmart/gtp-shared-components/ax';

import {Header, Page, Section, Spacer} from '../components';

export const FilterOverview: React.FC = () => {
  return (
    <SafeAreaView style={ss.container}>
      <Page>
        <Header>FilterTriggerAll</Header>
        <Section horizontal>
          <View style={ss.column}>
            <FilterTriggerAll />
            <Spacer />
            <FilterTriggerAll>Filters</FilterTriggerAll>
            <Spacer />
            <FilterTriggerAll appliedCount={0} />
            <Spacer />
            <FilterTriggerAll appliedCount={1} />
            <Spacer />
            <FilterTriggerAll appliedCount={1}>Filters</FilterTriggerAll>
          </View>
          <View style={ss.column}>
            <FilterTriggerAll disabled />
            <Spacer />
            <FilterTriggerAll disabled>Filters</FilterTriggerAll>
            <Spacer />
            <FilterTriggerAll disabled appliedCount={0} />
            <Spacer />
            <FilterTriggerAll disabled appliedCount={1} />
            <Spacer />
            <FilterTriggerAll disabled appliedCount={1}>
              Filters
            </FilterTriggerAll>
          </View>
        </Section>
        <Header>FilterTriggerSingle</Header>
        <Section horizontal>
          <View style={ss.column}>
            <FilterTriggerSingle leading={<Icons.TruckIcon />}>
              Closed
            </FilterTriggerSingle>
            <Spacer />
            <FilterTriggerSingle leading={<Icons.TruckIcon />} isOpen>
              Opened
            </FilterTriggerSingle>
            <Spacer />
            <FilterTriggerSingle leading={<Icons.TruckIcon />} isApplied>
              Closed Applied
            </FilterTriggerSingle>
            <Spacer />
            <FilterTriggerSingle leading={<Icons.TruckIcon />} isApplied isOpen>
              Open Applied
            </FilterTriggerSingle>
          </View>
          <View style={ss.column}>
            <FilterTriggerSingle leading={<Icons.TruckIcon />} disabled>
              Closed
            </FilterTriggerSingle>
            <Spacer />
            <FilterTriggerSingle leading={<Icons.TruckIcon />} isOpen disabled>
              Opened
            </FilterTriggerSingle>
            <Spacer />
            <FilterTriggerSingle
              leading={<Icons.TruckIcon />}
              isApplied
              disabled>
              Closed Applied
            </FilterTriggerSingle>
            <Spacer />
            <FilterTriggerSingle
              leading={<Icons.TruckIcon />}
              isApplied
              isOpen
              disabled>
              Open Applied
            </FilterTriggerSingle>
          </View>
        </Section>

        <Header>FilterToggle</Header>
        <Section horizontal>
          <View style={ss.column}>
            <FilterToggle>Filter</FilterToggle>
            <Spacer />
            <FilterToggle isApplied>Applied</FilterToggle>
            <Spacer />
            <FilterToggle leading={<Icons.ClockIcon />}>With Icon</FilterToggle>
            <Spacer />
            <FilterToggle leading={<Icons.ClockIcon />} isApplied>
              With Icon Applied
            </FilterToggle>
          </View>
          <View style={ss.column}>
            <FilterToggle disabled>Filter</FilterToggle>
            <Spacer />
            <FilterToggle isApplied disabled>
              Applied
            </FilterToggle>
            <Spacer />
            <FilterToggle leading={<Icons.ClockIcon />} disabled>
              With Icon
            </FilterToggle>
            <Spacer />
            <FilterToggle leading={<Icons.ClockIcon />} isApplied disabled>
              With Icon Applied
            </FilterToggle>
          </View>
        </Section>

        <Header>FilterTag</Header>
        <Section horizontal color="white">
          <View style={ss.column}>
            <FilterTag>Filter Details</FilterTag>
          </View>
          <View style={ss.column}>
            <FilterTag disabled>Filter Details</FilterTag>
          </View>
        </Section>
      </Page>
    </SafeAreaView>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
    paddingBottom: 18,
  },
  column: {
    flexDirection: 'column',
    alignItems: 'center',
  },
});
