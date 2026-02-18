import * as React from 'react';
import {SafeAreaView, StyleSheet} from 'react-native';
import {Icons} from '@walmart/gtp-shared-components';
import {
  FilterGroup,
  FilterTriggerAll,
  FilterTriggerSingle,
  FilterToggle,
  FilterTag,
} from '@walmart/gtp-shared-components/ax';

import {Header, Page, Section, VariantText} from '../components';

export const FilterGroupOverview: React.FC = () => {
  return (
    <SafeAreaView style={ss.container}>
      <Page>
        <Header>
          FilterGroup Trigger All <VariantText>(inline)</VariantText>
        </Header>
        <Section>
          <FilterGroup>
            <FilterTriggerAll />
            <FilterTriggerAll>Filters</FilterTriggerAll>
            <FilterTriggerAll appliedCount={0} />
            <FilterTriggerAll appliedCount={1} />
            <FilterTriggerAll appliedCount={1}>Filters</FilterTriggerAll>
          </FilterGroup>
        </Section>

        <Header>
          FilterGroup Trigger All <VariantText>(wrapping)</VariantText>
        </Header>
        <Section>
          <FilterGroup wrapping>
            <FilterTriggerAll />
            <FilterTriggerAll>Filters</FilterTriggerAll>
            <FilterTriggerAll appliedCount={0} />
            <FilterTriggerAll appliedCount={1} />
            <FilterTriggerAll appliedCount={1}>Filters</FilterTriggerAll>
          </FilterGroup>
        </Section>
        <Header>
          FilterGroup Trigger Single <VariantText>(inline)</VariantText>
        </Header>
        <Section>
          <FilterGroup>
            <FilterTriggerSingle leading={<Icons.TruckIcon />}>
              Closed
            </FilterTriggerSingle>
            <FilterTriggerSingle leading={<Icons.TruckIcon />} isOpen>
              Opened
            </FilterTriggerSingle>
            <FilterTriggerSingle leading={<Icons.TruckIcon />} isApplied>
              Closed Applied
            </FilterTriggerSingle>
            <FilterTriggerSingle leading={<Icons.TruckIcon />} isApplied isOpen>
              Open Applied
            </FilterTriggerSingle>
          </FilterGroup>
        </Section>

        <Header>
          FilterGroup Trigger Single <VariantText>(wrapping)</VariantText>
        </Header>
        <Section>
          <FilterGroup wrapping>
            <FilterTriggerSingle leading={<Icons.TruckIcon />}>
              Closed
            </FilterTriggerSingle>
            <FilterTriggerSingle leading={<Icons.TruckIcon />} isOpen>
              Opened
            </FilterTriggerSingle>
            <FilterTriggerSingle leading={<Icons.TruckIcon />} isApplied>
              Closed Applied
            </FilterTriggerSingle>
            <FilterTriggerSingle leading={<Icons.TruckIcon />} isApplied isOpen>
              Open Applied
            </FilterTriggerSingle>
          </FilterGroup>
        </Section>

        <Header>
          FilterGroup Toggle <VariantText>(inline)</VariantText>
        </Header>
        <Section>
          <FilterGroup>
            <FilterToggle>Filter</FilterToggle>
            <FilterToggle isApplied>Applied</FilterToggle>
            <FilterToggle leading={<Icons.ClockIcon />}>With Icon</FilterToggle>
            <FilterToggle leading={<Icons.ClockIcon />} isApplied>
              With Icon Applied
            </FilterToggle>
          </FilterGroup>
        </Section>

        <Header>
          FilterGroup Toggle <VariantText>(wrapping)</VariantText>
        </Header>
        <Section>
          <FilterGroup wrapping>
            <FilterToggle>Filter</FilterToggle>
            <FilterToggle isApplied>Applied</FilterToggle>
            <FilterToggle leading={<Icons.ClockIcon />}>With Icon</FilterToggle>
            <FilterToggle leading={<Icons.ClockIcon />} isApplied>
              With Icon Applied
            </FilterToggle>
          </FilterGroup>
        </Section>

        <Header>
          FilterGroup Tag <VariantText>(inline)</VariantText>
        </Header>
        <Section>
          <FilterGroup>
            <FilterTag>Apparel</FilterTag>
            <FilterTag>Front End</FilterTag>
            <FilterTag>Fuel</FilterTag>
            <FilterTag>Meat & Produce</FilterTag>
            <FilterTag>Optometry</FilterTag>
            <FilterTag>Pharmacy</FilterTag>
          </FilterGroup>
        </Section>

        <Header>
          FilterGroup Tag <VariantText>(wrapping)</VariantText>
        </Header>
        <Section>
          <FilterGroup wrapping>
            <FilterTag>Apparel</FilterTag>
            <FilterTag>Front End</FilterTag>
            <FilterTag>Fuel</FilterTag>
            <FilterTag>Meat & Produce</FilterTag>
            <FilterTag>Optometry</FilterTag>
            <FilterTag>Pharmacy</FilterTag>
          </FilterGroup>
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
});
