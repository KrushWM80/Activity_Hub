import * as React from 'react';
import {Controller, Header, Page, Section} from '../components';
import {StyleSheet} from 'react-native';
import {DateDropdown} from '@walmart/gtp-shared-components';

const DateDropdownOverview: React.FC = () => {
  const [date, setDate] = React.useState<Date | undefined>(undefined);

  return (
    <Page>
      <Header>Date Selector</Header>
      <Section inset={false}>
        <Controller setValueProp="onSelect">
          <DateDropdown
            value={date}
            onSelect={dt => {
              if (dt) {
                setDate(dt);
              }
            }}
            label="Date"
            helperText="Select one of these dates!"
            UNSAFE_style={ss.innerElement}
          />
        </Controller>
      </Section>
      <Header>Date Selector - with Success State</Header>
      <Section inset={false}>
        <Controller setValueProp="onSelect">
          <DateDropdown
            value={date}
            label="Date"
            helperText="Select one of these dates!"
            onSelect={dt => {
              if (dt) {
                setDate(dt);
              }
            }}
            UNSAFE_style={ss.innerElement}
          />
        </Controller>
      </Section>
      <Header>Date Selector - disabled</Header>
      <Section inset={false}>
        <Controller setValueProp="onSelect">
          <DateDropdown
            value={date}
            disabled={true}
            label="Date"
            onSelect={dt => {
              if (dt) {
                setDate(dt);
              }
            }}
            UNSAFE_style={ss.innerElement}
          />
        </Controller>
      </Section>
      <Header>Date Selector - with Error State</Header>
      <Section inset={false}>
        <Controller setValueProp="onSelect">
          <DateDropdown
            value={date}
            error={date ? '' : 'this field is required'}
            label="Date"
            helperText="Select one of these dates!"
            onSelect={dt => {
              if (dt) {
                setDate(dt);
              }
            }}
            UNSAFE_style={ss.innerElement}
          />
        </Controller>
      </Section>
    </Page>
  );
};

const ss = StyleSheet.create({
  innerElement: {
    marginHorizontal: 16,
  },
  section: {
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  sectionVerticalZero: {
    paddingVertical: 0,
  },
  listItem: {
    backgroundColor: 'transparent',
  },
  switches: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    alignItems: 'flex-start',
  },
  noLabels: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  radios: {
    paddingVertical: 12,
    paddingHorizontal: 16,
    alignItems: 'flex-start',
  },
});

export {DateDropdownOverview};
