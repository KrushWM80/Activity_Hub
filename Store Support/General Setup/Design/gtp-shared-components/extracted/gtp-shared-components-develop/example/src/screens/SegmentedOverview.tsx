import * as React from 'react';
import {StyleSheet, View} from 'react-native';
import {Section, Page, Header} from '../components';
import {
  Segmented,
  Segment,
  useSimpleReducer,
  colors,
} from '@walmart/gtp-shared-components';
import {segments} from './screensFixtures';

const SegmentedOverview = () => {
  type SegmentItem = {
    index: number;
    label: string;
  };

  type SegmentsState = {
    selectedSegment1: number;
    selectedSegment2: number;
    selectedSegment3: number;
    selectedSegment4: number;
  };

  const initialState = {
    selectedSegment1: 0,
    selectedSegment2: 0,
    selectedSegment3: 0,
    selectedSegment4: 0,
  };

  const [state, setState] = useSimpleReducer<SegmentsState>(initialState);

  const renderSegment = (segmentItem: SegmentItem) => {
    const {index, label} = segmentItem;
    return <Segment key={`Segment_${index}`}>{label}</Segment>;
  };

  return (
    <Page>
      <View style={ss.outerContainer}>
        <Header>Enabled Segments - with size Small</Header>
        <Section inset={false}>
          <Segmented
            size="small"
            selectedIndex={state.selectedSegment1 as number}
            onChange={(index: number) => setState('selectedSegment1', index)}>
            {segments.map(item => renderSegment(item))}
          </Segmented>
        </Section>
        <Header>Enabled Segments - with size Large</Header>
        <Section inset={false}>
          <Segmented
            size="large"
            selectedIndex={state.selectedSegment2 as number}
            onChange={(index: number) => setState('selectedSegment2', index)}>
            {segments.map(item => renderSegment(item))}
          </Segmented>
        </Section>
        <Header>Disabled Segments - with size Small</Header>
        <Section inset={false}>
          <Segmented
            size="small"
            disabled={true}
            selectedIndex={state.selectedSegment3 as number}
            onChange={(index: number) => setState('selectedSegment3', index)}>
            {segments.map(item => renderSegment(item))}
          </Segmented>
        </Section>
        <Header>Disabled Segments - with size Large</Header>
        <Section inset={false}>
          <Segmented
            size="large"
            disabled={true}
            selectedIndex={state.selectedSegment4 as number}
            onChange={(index: number) => setState('selectedSegment4', index)}>
            {segments.map(item => renderSegment(item))}
          </Segmented>
        </Section>
      </View>
    </Page>
  );
};
const ss = StyleSheet.create({
  outerContainer: {
    backgroundColor: colors.gray['5'],
    borderWidth: 1,
    padding: 5,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderColor: colors.gray['10'],
  },
});
export {SegmentedOverview};
