import * as React from 'react';
import {View, StyleSheet, ScrollView, Pressable} from 'react-native';
import {
  Body,
  BottomSheet,
  Button,
  Checkbox,
  Divider,
  Icons,
  List,
  ListItem,
  Radio,
  TabNavigation,
  TabNavigationItem,
  TextField,
} from '@walmart/gtp-shared-components';
import {
  FilterGroup,
  FilterTriggerAll,
  FilterTriggerSingle,
  FilterToggle,
  FilterTag,
} from '@walmart/gtp-shared-components/ax';

import {useSafeAreaInsets} from 'react-native-safe-area-context';

export const FilterGroupRecipes: React.FC = () => {
  const [selectedTab, setSelectedTab] = React.useState(0);

  const renderTab = (title: string, index: number) => {
    return (
      <TabNavigationItem
        key={index}
        isCurrent={selectedTab === index}
        onPress={() => setSelectedTab(index)}>
        {title}
      </TabNavigationItem>
    );
  };

  const renderRecipe = (index: number) => {
    switch (index) {
      case 0:
        return <RecipeAllWithLabel />;
      case 1:
        return <RecipeAllPlusSingle />;
      case 2:
        return <RecipeAllPlusToggle />;
      case 3:
        return <RecipeAllPlusSinglePlusToggle />;
      case 4:
        return <RecipeFilterTag key={0} />;
      case 5:
        return <RecipeFilterTag key={1} wrapping />;
    }
  };

  return (
    <View style={ss.container}>
      {/* eslint-disable-next-line react-native/no-inline-styles */}
      <TabNavigation UNSAFE_style={{flexShrink: 0}}>
        {renderTab('All w/ Label', 0)}
        {renderTab('All + Single', 1)}
        {renderTab('All + Toggle', 2)}
        {renderTab('All + Single + Toggle', 3)}
        {renderTab('Filter Tag inline', 4)}
        {renderTab('Filter Tag wrapping', 5)}
      </TabNavigation>
      {renderRecipe(selectedTab)}
    </View>
  );
};

const RecipeAllWithLabel: React.FC = () => {
  const insets = useSafeAreaInsets();
  const [bottomSheetVisible, setBottomSheetVisible] = React.useState(false);
  const [radioSelected, setRadioSelected] = React.useState<
    string | undefined
  >();
  const [checkboxSelected, setCheckboxSelected] = React.useState<string[]>([]);
  const [appliedCount, setAppliedCount] = React.useState<number | undefined>();

  const handleCheckboxPress = (option: string) => {
    if (checkboxSelected.includes(option)) {
      setCheckboxSelected(checkboxSelected.filter(item => item !== option));
    } else {
      setCheckboxSelected([...checkboxSelected, option]);
    }
  };

  const handleRadioPress = (option: string) => {
    setRadioSelected(option);
  };

  const handleSubmit = () => {
    let _appliedCount = 0;
    if (radioSelected) {
      _appliedCount++;
    }
    if (checkboxSelected.length > 0) {
      _appliedCount += checkboxSelected.length;
    }
    setAppliedCount(_appliedCount > 0 ? _appliedCount : undefined);
    setBottomSheetVisible(false);
  };

  return (
    <>
      <FilterGroup>
        <FilterTriggerAll
          appliedCount={appliedCount}
          onPress={() => setBottomSheetVisible(true)}>
          All Filters
        </FilterTriggerAll>
      </FilterGroup>
      <ScrollView style={[ss.content, {marginBottom: insets.bottom}]}>
        {Array.from({length: 10}).map((_, i) => (
          <View key={i} style={ss.contentSlot}>
            <Body weight="600" UNSAFE_style={ss.contentText}>
              Content slot {i + 1}
            </Body>
          </View>
        ))}
      </ScrollView>
      <BottomSheet
        title="All Filters"
        isOpen={bottomSheetVisible}
        onClose={() => setBottomSheetVisible(false)}
        UNSAFE_style={{paddingBottom: insets.bottom}}
        actions={
          <Button variant="primary" isFullWidth={true} onPress={handleSubmit}>
            Apply
          </Button>
        }>
        <>
          <Body UNSAFE_style={ss.margin}>Category 1</Body>
          <Divider />
          <Radio
            label="Option 1"
            checked={radioSelected === 'Option 1'}
            onPress={() => handleRadioPress('Option 1')}
            UNSAFE_style={ss.margin}
          />
          <Radio
            label="Option 2"
            checked={radioSelected === 'Option 2'}
            onPress={() => handleRadioPress('Option 2')}
            UNSAFE_style={ss.margin}
          />
          <Radio
            label="Option 3"
            checked={radioSelected === 'Option 3'}
            onPress={() => handleRadioPress('Option 3')}
            UNSAFE_style={ss.margin}
          />
          <Body UNSAFE_style={ss.margin}>Category 2</Body>
          <Divider />
          <Checkbox
            label="Option 1"
            checked={checkboxSelected.includes('Option 1')}
            onPress={() => handleCheckboxPress('Option 1')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 2"
            checked={checkboxSelected.includes('Option 2')}
            onPress={() => handleCheckboxPress('Option 2')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 3"
            checked={checkboxSelected.includes('Option 3')}
            onPress={() => handleCheckboxPress('Option 3')}
            UNSAFE_style={ss.margin}
          />
        </>
      </BottomSheet>
    </>
  );
};

const RecipeAllPlusSingle: React.FC = () => {
  const insets = useSafeAreaInsets();
  const [bottomSheetVisible, setBottomSheetVisible] = React.useState(false);
  const [statusBottomSheetVisible, setStatusBottomSheetVisible] =
    React.useState(false);
  const [radioSelected, setRadioSelected] = React.useState<
    string | undefined
  >();
  const [checkboxSelected, setCheckboxSelected] = React.useState<string[]>([]);

  const [appliedCount, setAppliedCount] = React.useState<number | undefined>();

  const handleCheckboxPress = (option: string) => {
    if (checkboxSelected.includes(option)) {
      setCheckboxSelected(checkboxSelected.filter(item => item !== option));
    } else {
      setCheckboxSelected([...checkboxSelected, option]);
    }
  };

  const handleRadioPress = (option: string) => {
    setRadioSelected(option);
  };

  const handleSubmit = () => {
    let _appliedCount = 0;
    if (radioSelected) {
      _appliedCount++;
    }
    if (checkboxSelected.length > 0) {
      _appliedCount += checkboxSelected.length;
    }

    setAppliedCount(_appliedCount > 0 ? _appliedCount : undefined);

    setBottomSheetVisible(false);
    setStatusBottomSheetVisible(false);
  };

  return (
    <>
      <FilterGroup>
        <FilterTriggerAll
          appliedCount={appliedCount}
          onPress={() => setBottomSheetVisible(true)}
        />
        <FilterTriggerSingle
          isOpen={statusBottomSheetVisible}
          isApplied={checkboxSelected.length > 0}
          onPress={() => setStatusBottomSheetVisible(true)}>
          Status
        </FilterTriggerSingle>
      </FilterGroup>
      <ScrollView style={[ss.content, {marginBottom: insets.bottom}]}>
        {Array.from({length: 10}).map((_, i) => (
          <View key={i} style={ss.contentSlot}>
            <Body weight="600" UNSAFE_style={ss.contentText}>
              Content slot {i + 1}
            </Body>
          </View>
        ))}
      </ScrollView>
      <BottomSheet
        title="All Filters"
        isOpen={bottomSheetVisible}
        onClose={() => setBottomSheetVisible(false)}
        UNSAFE_style={{paddingBottom: insets.bottom}}
        actions={
          <Button variant="primary" isFullWidth={true} onPress={handleSubmit}>
            Apply
          </Button>
        }>
        <>
          <Body UNSAFE_style={ss.margin}>Category 1</Body>
          <Divider />
          <Radio
            label="Option 1"
            checked={radioSelected === 'Option 1'}
            onPress={() => handleRadioPress('Option 1')}
            UNSAFE_style={ss.margin}
          />
          <Radio
            label="Option 2"
            checked={radioSelected === 'Option 2'}
            onPress={() => handleRadioPress('Option 2')}
            UNSAFE_style={ss.margin}
          />
          <Radio
            label="Option 3"
            checked={radioSelected === 'Option 3'}
            onPress={() => handleRadioPress('Option 3')}
            UNSAFE_style={ss.margin}
          />
          <Body UNSAFE_style={ss.margin}>Category 2</Body>
          <Divider />
          <Checkbox
            label="Option 1"
            checked={checkboxSelected.includes('Option 1')}
            onPress={() => handleCheckboxPress('Option 1')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 2"
            checked={checkboxSelected.includes('Option 2')}
            onPress={() => handleCheckboxPress('Option 2')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 3"
            checked={checkboxSelected.includes('Option 3')}
            onPress={() => handleCheckboxPress('Option 3')}
            UNSAFE_style={ss.margin}
          />
        </>
      </BottomSheet>
      <BottomSheet
        title="Filter by Status"
        isOpen={statusBottomSheetVisible}
        onClose={() => setStatusBottomSheetVisible(false)}
        UNSAFE_style={{paddingBottom: insets.bottom}}
        actions={
          <Button variant="primary" isFullWidth={true} onPress={handleSubmit}>
            Apply
          </Button>
        }>
        <>
          <Body UNSAFE_style={ss.margin}>Category 2</Body>
          <Divider />
          <Checkbox
            label="Option 1"
            checked={checkboxSelected.includes('Option 1')}
            onPress={() => handleCheckboxPress('Option 1')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 2"
            checked={checkboxSelected.includes('Option 2')}
            onPress={() => handleCheckboxPress('Option 2')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 3"
            checked={checkboxSelected.includes('Option 3')}
            onPress={() => handleCheckboxPress('Option 3')}
            UNSAFE_style={ss.margin}
          />
        </>
      </BottomSheet>
    </>
  );
};

const RecipeAllPlusSinglePlusToggle: React.FC = () => {
  const insets = useSafeAreaInsets();
  const [bottomSheetVisible, setBottomSheetVisible] = React.useState(false);
  const [statusBottomSheetVisible, setStatusBottomSheetVisible] =
    React.useState(false);

  const [checkboxSelected, setCheckboxSelected] = React.useState<string[]>([]);

  const [appliedCount, setAppliedCount] = React.useState<number | undefined>();

  const [createdByMe, setCreatedByMe] = React.useState<boolean>(false);

  React.useEffect(() => {
    let _appliedCount = 0;

    if (checkboxSelected.length > 0) {
      _appliedCount += checkboxSelected.length;
    }
    if (createdByMe) {
      _appliedCount++;
    }
    setAppliedCount(_appliedCount > 0 ? _appliedCount : undefined);
  }, [checkboxSelected, createdByMe]);

  const handleCheckboxPress = (option: string) => {
    if (checkboxSelected.includes(option)) {
      setCheckboxSelected(checkboxSelected.filter(item => item !== option));
    } else {
      setCheckboxSelected([...checkboxSelected, option]);
    }
  };

  const handleSubmit = () => {
    setBottomSheetVisible(false);
    setStatusBottomSheetVisible(false);
  };

  return (
    <>
      <FilterGroup>
        <FilterTriggerAll
          appliedCount={appliedCount}
          onPress={() => setBottomSheetVisible(true)}
        />
        <FilterTriggerSingle
          isOpen={statusBottomSheetVisible}
          isApplied={checkboxSelected.length > 0}
          onPress={() => setStatusBottomSheetVisible(true)}>
          Status
        </FilterTriggerSingle>
        <FilterToggle
          isApplied={createdByMe}
          onPress={() => setCreatedByMe(!createdByMe)}>
          Created by me
        </FilterToggle>
      </FilterGroup>
      <ScrollView style={[ss.content, {marginBottom: insets.bottom}]}>
        {Array.from({length: 10}).map((_, i) => (
          <View key={i} style={ss.contentSlot}>
            <Body weight="600" UNSAFE_style={ss.contentText}>
              Content slot {i + 1}
            </Body>
          </View>
        ))}
      </ScrollView>
      <BottomSheet
        title="All Filters"
        isOpen={bottomSheetVisible}
        onClose={() => setBottomSheetVisible(false)}
        UNSAFE_style={{paddingBottom: insets.bottom}}
        actions={
          <Button variant="primary" isFullWidth={true} onPress={handleSubmit}>
            Apply
          </Button>
        }>
        <>
          <Body UNSAFE_style={ss.margin}>Status</Body>
          <Divider />
          <Checkbox
            label="Option 1"
            checked={checkboxSelected.includes('Option 1')}
            onPress={() => handleCheckboxPress('Option 1')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 2"
            checked={checkboxSelected.includes('Option 2')}
            onPress={() => handleCheckboxPress('Option 2')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 3"
            checked={checkboxSelected.includes('Option 3')}
            onPress={() => handleCheckboxPress('Option 3')}
            UNSAFE_style={ss.margin}
          />
          <Body UNSAFE_style={ss.margin}>Created by me</Body>
          <Divider />
          <Checkbox
            label="Created by me"
            checked={createdByMe}
            onPress={() => setCreatedByMe(!createdByMe)}
            UNSAFE_style={ss.margin}
          />
        </>
      </BottomSheet>
      <BottomSheet
        title="Filter by Status"
        isOpen={statusBottomSheetVisible}
        onClose={() => setStatusBottomSheetVisible(false)}
        UNSAFE_style={{paddingBottom: insets.bottom}}
        actions={
          <Button variant="primary" isFullWidth={true} onPress={handleSubmit}>
            Apply
          </Button>
        }>
        <>
          <Checkbox
            label="Option 1"
            checked={checkboxSelected.includes('Option 1')}
            onPress={() => handleCheckboxPress('Option 1')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 2"
            checked={checkboxSelected.includes('Option 2')}
            onPress={() => handleCheckboxPress('Option 2')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 3"
            checked={checkboxSelected.includes('Option 3')}
            onPress={() => handleCheckboxPress('Option 3')}
            UNSAFE_style={ss.margin}
          />
        </>
      </BottomSheet>
    </>
  );
};

const RecipeAllPlusToggle: React.FC = () => {
  const insets = useSafeAreaInsets();
  const [bottomSheetVisible, setBottomSheetVisible] = React.useState(false);
  const [radioSelected, setRadioSelected] = React.useState<
    string | undefined
  >();
  const [checkboxSelected, setCheckboxSelected] = React.useState<string[]>([]);
  const [appliedCount, setAppliedCount] = React.useState<number | undefined>();

  const [togglesApplied, setTogglesApplied] = React.useState<string[]>([]);

  React.useEffect(() => {
    let _appliedCount = 0;
    if (radioSelected) {
      _appliedCount++;
    }
    if (checkboxSelected.length > 0) {
      _appliedCount += checkboxSelected.length;
    }
    setAppliedCount(_appliedCount > 0 ? _appliedCount : undefined);
  }, [radioSelected, checkboxSelected, togglesApplied]);

  const handleCheckboxPress = (option: string) => {
    if (checkboxSelected.includes(option)) {
      setCheckboxSelected(checkboxSelected.filter(item => item !== option));
    } else {
      setCheckboxSelected([...checkboxSelected, option]);
    }
  };

  const handleToggleApply = (label: string) => {
    if (togglesApplied.includes(label)) {
      setTogglesApplied(togglesApplied.filter(item => item !== label));
    } else {
      setTogglesApplied([...togglesApplied, label]);
    }
    handleCheckboxPress(label);
  };

  const handleRadioPress = (option: string) => {
    setRadioSelected(option);
  };

  const handleSubmit = () => {
    setBottomSheetVisible(false);
  };

  return (
    <>
      <FilterGroup>
        <FilterTriggerAll
          appliedCount={appliedCount}
          onPress={() => setBottomSheetVisible(true)}
        />
        <FilterToggle
          leading={<Icons.EmailIcon />}
          isApplied={checkboxSelected.includes('Option 1')}
          onPress={() => {
            handleToggleApply('Option 1');
          }}>
          Option 1
        </FilterToggle>
        <FilterToggle
          isApplied={checkboxSelected.includes('Option 2')}
          onPress={() => {
            handleToggleApply('Option 2');
          }}>
          Option 2
        </FilterToggle>
        <FilterToggle
          isApplied={checkboxSelected.includes('Option 3')}
          onPress={() => {
            handleToggleApply('Option 3');
          }}>
          Option 3
        </FilterToggle>
      </FilterGroup>
      <ScrollView style={[ss.content, {marginBottom: insets.bottom}]}>
        {Array.from({length: 10}).map((_, i) => (
          <View key={i} style={ss.contentSlot}>
            <Body weight="600" UNSAFE_style={ss.contentText}>
              Content slot {i + 1}
            </Body>
          </View>
        ))}
      </ScrollView>
      <BottomSheet
        title="All Filters"
        isOpen={bottomSheetVisible}
        onClose={() => setBottomSheetVisible(false)}
        UNSAFE_style={{paddingBottom: insets.bottom}}
        actions={
          <Button variant="primary" isFullWidth={true} onPress={handleSubmit}>
            Apply
          </Button>
        }>
        <>
          <Body UNSAFE_style={ss.margin}>Category 1</Body>
          <Divider />
          <Radio
            label="Option 1"
            checked={radioSelected === 'Option 1'}
            onPress={() => handleRadioPress('Option 1')}
            UNSAFE_style={ss.margin}
          />
          <Radio
            label="Option 2"
            checked={radioSelected === 'Option 2'}
            onPress={() => handleRadioPress('Option 2')}
            UNSAFE_style={ss.margin}
          />
          <Radio
            label="Option 3"
            checked={radioSelected === 'Option 3'}
            onPress={() => handleRadioPress('Option 3')}
            UNSAFE_style={ss.margin}
          />
          <Body UNSAFE_style={ss.margin}>Category 2</Body>
          <Divider />
          <Checkbox
            label="Option 1"
            checked={checkboxSelected.includes('Option 1')}
            onPress={() => handleCheckboxPress('Option 1')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 2"
            checked={checkboxSelected.includes('Option 2')}
            onPress={() => handleCheckboxPress('Option 2')}
            UNSAFE_style={ss.margin}
          />
          <Checkbox
            label="Option 3"
            checked={checkboxSelected.includes('Option 3')}
            onPress={() => handleCheckboxPress('Option 3')}
            UNSAFE_style={ss.margin}
          />
        </>
      </BottomSheet>
    </>
  );
};

type RecipeFilterTagProps = {
  wrapping?: boolean;
};

const RecipeFilterTag: React.FC<RecipeFilterTagProps> = props => {
  const {wrapping = false} = props;
  const insets = useSafeAreaInsets();
  const [searchValue, setSearchValue] = React.useState('');
  const [tags, setTags] = React.useState<string[]>([]);
  const listItems = [
    'Deli & Bakery',
    'Food & Consumables',
    'Meat & Produce',
    'Admin & Support team',
    'Digital',
    'Digital Overnight',
    'Asset Protection',
    'Apparel',
    'Auto Care Center',
    'Entertainment',
    'Home',
    'Seasonal',
  ];
  return (
    <>
      {/* eslint-disable-next-line react-native/no-inline-styles */}
      <View style={{minHeight: 100, paddingHorizontal: 16}}>
        <TextField
          type="search"
          size="large"
          label="Search and filter by team"
          placeholder="Search..."
          value={searchValue}
          trailing={
            searchValue.length > 0 && (
              <Pressable onPress={() => setSearchValue('')}>
                <Icons.CloseIcon size="medium" />
              </Pressable>
            )
          }
          onChangeText={txt => {
            setSearchValue(txt);
          }}
        />
      </View>

      {tags.length > 0 && (
        <FilterGroup wrapping={wrapping}>
          {tags.map((tag, i) => (
            <FilterTag
              key={i}
              onPress={() => {
                setTags(tags.filter(t => t !== tag));
              }}>
              {tag}
            </FilterTag>
          ))}
        </FilterGroup>
      )}
      <ScrollView style={[ss.content, {marginBottom: insets.bottom}]}>
        <List>
          {listItems.map((v, i) =>
            v.toLowerCase().includes(searchValue.toLowerCase()) &&
            !tags.includes(v) ? (
              <ListItem
                key={i}
                leading={<Icons.AssociateIcon size="medium" />}
                trailing={
                  <Checkbox
                    checked={tags.includes(v)}
                    onPress={() => {
                      if (tags.includes(v)) {
                        setTags(tags.filter(t => t !== v));
                      } else {
                        setTags([...tags, v]);
                      }
                    }}
                  />
                }
                // eslint-disable-next-line react-native/no-inline-styles
                UNSAFE_style={{alignItems: 'center'}}>
                {v}
              </ListItem>
            ) : undefined,
          )}
        </List>
      </ScrollView>
    </>
  );
};

const ss = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'white',
  },
  content: {
    paddingHorizontal: 16,
  },
  contentSlot: {
    height: 70,
    marginTop: 16,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#7110EF',
    borderStyle: 'dashed',
    backgroundColor: '#F8F2FF',
  },
  contentText: {
    color: '#7110EF',
  },
  margin: {
    marginVertical: 14,
  },
});
