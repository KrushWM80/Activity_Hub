import * as React from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  TextInput,
  SectionList,
  TouchableOpacity,
  TouchableWithoutFeedback,
} from 'react-native';
import {
  Caption,
  Checkbox,
  Button,
  colors,
  Icons,
  BottomSheet,
} from '@walmart/gtp-shared-components';

import {
  getUniqFilteredList,
  getTeamsData,
  getLabel,
  getListData,
  getListLabel,
  addBrackets,
  toTitleCase,
  MY_TEAM,
} from './utils';
import {facilityData} from './facilityData';

// This is based on consumer code from Facilities Management team
// https://gecgithub01.walmart.com/GIODA/facilities-management-miniapp/blob/release-9/src/common/SearchableDropdown/CustomCheckbox.tsx
// added for CEEMP-2853

const BottomSheetWithScrollableContentRecipe: React.FC = () => {
  const [searchPhraseTeams, setSearchPhraseTeams] = React.useState('');
  const [searchPhraseAssociates, setSearchPhraseAssociates] =
    React.useState('');
  let userTeams: Array<any> = [];
  let signOffUsers: Array<any> = [];
  /* Remove duplicates from user teams and  signoff users*/
  const suggestedTeams = getUniqFilteredList(
    [...userTeams, ...signOffUsers],
    'teamId',
  );
  /* Format signoff and teams data*/
  const list = facilityData.map(({teamId = '', teamName = '', associates}) => ({
    data: associates,
    teamId,
    teamName,
  }));

  /* Retrieve team id from object*/
  const userTeamMap = suggestedTeams.map(teams => teams?.teamId);

  const [dropdownClick, setDropDownClick] = React.useState(false);
  /* Filter the suggested team data from original array*/
  const finalSuggestedData = list.filter(item =>
    userTeamMap?.includes(item?.teamId),
  );
  const [teamItems, setTeamItems] = React.useState<string[]>([]);
  const [signOffItems, setSignOffItems] = React.useState<string[]>([]);
  /* Adding section title for watch list team*/
  const isEveryItemPresent = list.every(team => Boolean(team?.teamId));
  const listWithTeam = [
    {section: 'suggested', data: finalSuggestedData},
    {
      section: 'teams',
      data: isEveryItemPresent ? list : list.slice(1),
    },
  ];

  const [isSignOffConditionValid, setIsSignOffConditionValid] =
    React.useState(false);

  const handleCheck = (item: string) => {
    const currentItems = isSignOffConditionValid ? teamItems : signOffItems;
    let updatedList = isSignOffConditionValid
      ? [...teamItems]
      : [...signOffItems];
    if (currentItems.includes(item)) {
      updatedList = currentItems.filter(i => i !== item);
    } else {
      updatedList = [...currentItems, item];
    }
    if (isSignOffConditionValid) {
      setTeamItems(updatedList);
    } else {
      setSignOffItems(updatedList);
    }
  };

  const searchInput = (searchPhrase: string) => {
    return (
      <>
        <Caption weight={'500'} UNSAFE_style={styles.headerStyle}>
          {'Search Team'}
        </Caption>
        <View style={styles.container}>
          <Icons.SearchIcon color={colors.gray[100]} size={16} />
          <TextInput
            style={styles.textInputStyle}
            placeholderTextColor={colors.gray[100]}
            numberOfLines={1}
            maxLength={400}
            placeholder={'Search'}
            onChangeText={onTextChange}
            value={searchPhrase}
            returnKeyType="done"
            returnKeyLabel="Done"
          />
        </View>
      </>
    );
  };
  const renderSelectedItems = () => {
    const checkedItems = isSignOffConditionValid ? teamItems : signOffItems;
    return (
      checkedItems.length > 0 && (
        <ScrollView
          style={styles.horizontalScroll}
          contentContainerStyle={styles.checkedItemScrollView}
          showsHorizontalScrollIndicator={false}
          horizontal>
          {checkedItems.map((item, index) => {
            return (
              <TouchableWithoutFeedback key={index}>
                <View style={styles.selectedItemView}>
                  <Caption UNSAFE_style={styles.selectedItemText}>
                    {toTitleCase(item)}
                  </Caption>
                  <TouchableOpacity
                    testID="close-icon"
                    onPress={() => handleCheck(item)}
                    hitSlop={{top: 10, bottom: 10, left: 10, right: 10}}
                    style={styles.closeIconContainer}>
                    <Icons.CloseIcon
                      UNSAFE_style={styles.closeIconStyle}
                      color="black"
                    />
                  </TouchableOpacity>
                </View>
              </TouchableWithoutFeedback>
            );
          })}
        </ScrollView>
      )
    );
  };

  const isItemChecked = (item: any) => {
    return isSignOffConditionValid
      ? teamItems.includes(item)
      : signOffItems.includes(item);
  };

  const renderSectionList = (data: any, searchPhrase: string) => {
    return (
      // eslint-disable-next-line react-native/no-inline-styles
      <View style={{height: '100%'}}>
        {searchInput(searchPhrase)}
        {renderSelectedItems()}
        <SectionList
          keyboardShouldPersistTaps={'always'}
          stickySectionHeadersEnabled={false}
          sections={data}
          //Combining updateCellsBatchingPeriod with maxToRenderPerBatch will lead you to achieve your desired fillrate / performance
          updateCellsBatchingPeriod={100}
          maxToRenderPerBatch={20}
          renderItem={({item}) => {
            const label = isSignOffConditionValid
              ? getLabel(item, userTeams)
              : getListLabel(item, item?.userId);
            return (
              <Checkbox
                UNSAFE_style={styles.checkboxStyle}
                label={label}
                checked={isItemChecked(label)}
                onPress={() => handleCheck(label)}
              />
            );
          }}
          renderSectionHeader={({section}) => {
            return section?.teamName ? (
              <>
                <View style={styles.bottomBar} />
                <Caption
                  // @ts-ignore
                  style={styles.headerTitle}>
                  {toTitleCase(
                    isSignOffConditionValid
                      ? section?.section
                      : section?.teamName,
                  )}
                  {!isSignOffConditionValid &&
                  userTeams.some(item => item?.teamId === section?.teamId)
                    ? ` ${addBrackets(MY_TEAM?.toLowerCase())}`
                    : ''}
                </Caption>
              </>
            ) : null;
          }}
          keyExtractor={(item, index) => item + index}
        />
      </View>
    );
  };

  const handleDropdownClose = () => {
    setDropDownClick(false);
  };
  const onTextChange = (text: string) => {
    if (isSignOffConditionValid) {
      setSearchPhraseTeams(text);
    } else {
      setSearchPhraseAssociates(text);
    }
  };
  return (
    <>
      <Button
        variant="primary"
        size="medium"
        isFullWidth
        UNSAFE_style={styles.button}
        onPress={() => {
          setDropDownClick(true);
          setIsSignOffConditionValid(true);
        }}>
        Open BottomSheet w/Teams Data
      </Button>
      <Button
        variant="secondary"
        size="medium"
        UNSAFE_style={styles.button}
        isFullWidth
        onPress={() => {
          setDropDownClick(true);
          setIsSignOffConditionValid(false);
        }}>
        Open BottomSheet w/Associates Data
      </Button>
      <BottomSheet
        isOpen={dropdownClick}
        childrenContainScrollableComponent={true}
        onClose={handleDropdownClose}
        onBackButtonPress={handleDropdownClose}
        title={isSignOffConditionValid ? 'Signoff' : 'Team'}
        actions={
          <Button
            variant="primary"
            size="medium"
            isFullWidth
            onPress={handleDropdownClose}>
            Assign
          </Button>
        }>
        {renderSectionList(
          isSignOffConditionValid
            ? getTeamsData(listWithTeam, searchPhraseTeams)
            : getListData(list, searchPhraseAssociates),
          isSignOffConditionValid ? searchPhraseTeams : searchPhraseAssociates,
        )}
      </BottomSheet>
    </>
  );
};
const styles = StyleSheet.create({
  bottomBar: {
    borderBottomWidth: 1,
    borderBottomColor: colors.gray[10],
    borderBottomEndRadius: 0.5,
    marginVertical: 4,
  },
  horizontalScroll: {minHeight: 55, maxHeight: 60},
  checkboxStyle: {
    padding: 6,
  },
  headerTitle: {
    fontSize: 16,
    lineHeight: 24,
    marginTop: 16,
    marginHorizontal: 6,
    marginBottom: 8,
    color: colors.gray[100],
  },
  headerStyle: {marginBottom: 4},
  textInputStyle: {
    justifyContent: 'center',
    flex: 1,
    color: colors.gray[160],
    paddingLeft: 10,
    height: 40,
  },
  container: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: colors.gray[80],
    borderRadius: 4,
    paddingLeft: 10,
    marginBottom: 8,
  },
  selectedItemText: {
    color: colors.white,
  },
  selectedItemView: {
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.gray[160],
    borderRadius: 16,
    paddingVertical: 4,
    paddingHorizontal: 12,
    margin: 4,
    height: 32,
  },
  closeIconContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: colors.white,
    marginLeft: 8,
  },
  closeIconStyle: {width: 8, height: 8},
  checkedItemScrollView: {
    paddingVertical: 5,
    height: 55,
    alignItems: 'center',
  },
  button: {alignSelf: 'center', padding: 16},
});

export {BottomSheetWithScrollableContentRecipe};
