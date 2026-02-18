// @ts-nocheck
/* eslint-disable */
/**
 * This recipe is extracted from
 * https://gecgithub01.walmart.com/store-systems-associate-tech-platform/store-feature-orders/blob/main/src/storefeatureorders/components/DepartmentsModal/DepartmentModal.tsx
 * For ticket https://jira.walmart.com/browse/CEEMP-3747
 *
 */
import React, {useEffect, useMemo, useState} from 'react';
import {Section} from '../components';
import {
  BottomSheet,
  Button,
  Checkbox,
  ChevronLeftIcon,
  ChevronRightIcon,
  Divider,
  IconButton,
} from '@walmart/gtp-shared-components';
import {
  FlatList,
  Platform,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';
import {useSafeAreaInsets} from 'react-native-safe-area-context';

export const BottomSheetDepartmentModalRecipe: React.FC = () => {
  const [openModal, setOpenModal] = useState(false);
  return (
    <Section>
      <Button variant="primary" onPress={() => setOpenModal(true)}>
        Show BottomSheet
      </Button>
      <DepartmentModal
        visible={openModal}
        onDismiss={() => setOpenModal(false)}
        applyFilter={(selectedDepartmentCategory, filterType) => {
          console.log(
            'selectedDepartmentCategory:',
            selectedDepartmentCategory,
          );
          console.log('filterType:', filterType);
        }}
        departmentList={[
          {
            Department: 1,
            DepartmentDescription: 'Department 1',
            Categories: [
              {CategoryId: 1, CategoryDescription: 'Category 1'},
              {CategoryId: 2, CategoryDescription: 'Category 2'},
              {CategoryId: 3, CategoryDescription: 'Category 3'},
            ],
          },
          {
            Department: 2,
            DepartmentDescription: 'Department 2',
            Categories: [
              {CategoryId: 4, CategoryDescription: 'Category 4'},
              {CategoryId: 5, CategoryDescription: 'Category 5'},
              {CategoryId: 6, CategoryDescription: 'Category 6'},
            ],
          },
        ]}
      />
    </Section>
  );
};

export interface Category {
  CategoryId: number;
  CategoryDescription: string;
  selected?: boolean;
}

export interface Departments {
  Department: number;
  DepartmentDescription: string;
  isAllCategoriesSelected?: 'checked' | 'unchecked' | 'indeterminate';
  Categories: Category[];
}

export interface DepartmentModalProps {
  visible: boolean;
  onDismiss: () => void;
  applyFilter: (
    selectedDepartmentCategory: SelectedDepartmentCategoryType[],
    filterType: string,
  ) => void;
  departmentList: Array<Departments>;
  filterOnly?: boolean;
  recommendedDepartment?: any;
  singleDepartmentSelection?: boolean;
}

export type SelectedDepartmentCategoryType = {
  department: number;
  categories: number[];
};

enum ScreenState {
  DepartmentList = 'DepartmentList',
  CategoryList = 'CategoryList',
}

export const DepartmentModal: React.FC<DepartmentModalProps> = props => {
  const {
    visible,
    onDismiss,
    applyFilter,
    departmentList: propDepartmentList,
    filterOnly,
    recommendedDepartment,
    singleDepartmentSelection = false,
  } = props;
  const {bottom} = useSafeAreaInsets();
  const [toggle, setToggle] = useState(false);
  const [resetFilter, setResetFilter] = useState(false);
  const [screenState, setScreenState] = useState<ScreenState>(
    ScreenState.DepartmentList,
  );
  // The department tapped by user. Used to navigate to category list view
  const [departmentForCategoryListView, setDepartmentForCategoryListView] =
    useState<Departments>();
  // Department currently selected (Populates after checking any categories belonging to a dept)
  const [currentlySelectedDepartment, setCurrentlySelectedDepartment] =
    useState<Departments | null>();
  const departmentListRef = React.useRef();
  const categoryListRef = React.useRef();

  const departmentList: Departments[] = useMemo(() => {
    const departmentList: Departments[] = JSON.parse(
      JSON.stringify(propDepartmentList),
    );
    departmentList.forEach(department => {
      department.Categories.sort(
        (categoryA, categoryB) => categoryA.CategoryId - categoryB.CategoryId,
      );
    });
    return departmentList;
  }, [propDepartmentList]);

  useEffect(() => {
    if (recommendedDepartment) {
      departmentList?.forEach(department => {
        department.Categories.forEach(cat => {
          if (cat.CategoryId === recommendedDepartment.Category) {
            cat.selected = true;
          }
        });
      });
      setToggle(!toggle);
    }
  }, [departmentList, recommendedDepartment, toggle]);

  useEffect(() => {
    refreshCurrentlySelectedDepartment();
    // departmentListRef.current?.scrollToOffset({animated: false, offset: 0});
    // categoryListRef.current?.scrollToOffset({animated: false, offset: 0});
  }, [refreshCurrentlySelectedDepartment, screenState]);

  const applySelectedFilter = () => {
    const selectedDepartmentCategory: SelectedDepartmentCategoryType[] = [];
    departmentList.forEach(department => {
      const selectedCategory: Array<number> = [];
      department.Categories.forEach(category => {
        if (category?.selected) {
          selectedCategory.push(category.CategoryId);
        }
      });
      if (selectedCategory.length > 0) {
        selectedDepartmentCategory.push({
          department: department.Department,
          categories: selectedCategory,
        });
      }
    });
    Object.assign(propDepartmentList, departmentList);
    if (selectedDepartmentCategory.length) {
      applyFilter(selectedDepartmentCategory, 'department');
      onDismiss();
    } else {
      clearFilter();
    }
  };

  const refreshCurrentlySelectedDepartment = React.useCallback(() => {
    for (const department of departmentList) {
      const checkedCategoryCount = department.Categories.filter(
        category => category.selected,
      ).length;
      // Identify the currently checked department
      if (checkedCategoryCount === 0) {
        department.isAllCategoriesSelected = 'unchecked';
      } else {
        department.isAllCategoriesSelected =
          checkedCategoryCount === department.Categories.length
            ? 'checked'
            : 'indeterminate';
        setCurrentlySelectedDepartment(department);
        return;
      }
    }
    setCurrentlySelectedDepartment(null);
  }, [departmentList]);

  const onOpen = () => {
    setScreenState(ScreenState.DepartmentList);
    setResetFilter(!resetFilter);
    refreshCurrentlySelectedDepartment();
  };

  const onClose = () => {
    setResetFilter(!resetFilter);
    onDismiss();
  };

  const clearFilter = () => {
    departmentList.forEach(department => {
      department.isAllCategoriesSelected = 'unchecked';
      department.Categories.forEach(category => {
        category.selected = false;
      });
    });
    Object.assign(propDepartmentList, departmentList);
    setToggle(!toggle);
    if (filterOnly) {
      applyFilter([], 'department');
      onDismiss();
    }
  };

  const autoDeSelecting = (selectedDepartment: Departments) => {
    departmentList?.forEach(department => {
      if (department.Department === selectedDepartment.Department) {
        return;
      }
      department.isAllCategoriesSelected = 'unchecked';
      department.Categories.forEach(category => {
        category.selected = false;
      });
    });
  };

  const departmentsKeyExtractor = (item: Departments) =>
    item.Department.toString();
  const categoriesKeyExtractor = (item: Category) => item.CategoryId.toString();

  const flipToCategoriesListView = (department: Departments) => {
    setDepartmentForCategoryListView(department);
    setScreenState(ScreenState.CategoryList);
  };

  const selectAllCategories = (selectedDepartment: Departments) => {
    if (singleDepartmentSelection) {
      autoDeSelecting(selectedDepartment);
    }
    selectedDepartment.Categories.forEach(category => {
      category.selected = true;
    });
    selectedDepartment.isAllCategoriesSelected = 'checked';
    setToggle(!toggle);
  };

  const handleSelectAllCategoriesAction = (selectedDepartment: Departments) => {
    if (selectedDepartment.isAllCategoriesSelected !== 'checked') {
      selectAllCategories(selectedDepartment);
    } else {
      selectedDepartment.isAllCategoriesSelected = 'unchecked';
      selectedDepartment.Categories.forEach(category => {
        category.selected = false;
      });
      setToggle(!toggle);
    }
  };

  const selectItem = (item: Category) => {
    if (!departmentForCategoryListView) {
      return;
    }
    const {Categories} = departmentForCategoryListView;
    if (singleDepartmentSelection) {
      autoDeSelecting(departmentForCategoryListView);
    }
    item.selected = !item.selected;
    const checkedCategoryCount = Categories.filter(
      category => category.selected,
    ).length;
    if (checkedCategoryCount === 0) {
      departmentForCategoryListView.isAllCategoriesSelected = 'unchecked';
    } else if (checkedCategoryCount === Categories.length) {
      departmentForCategoryListView.isAllCategoriesSelected = 'checked';
    } else {
      departmentForCategoryListView.isAllCategoriesSelected = 'indeterminate';
    }
    setToggle(!toggle);
  };

  const departmentListItem = (
    item: any,
    idKey: string,
    titleKey: string,
    parentIndex: number,
  ) => {
    const isCheckedAy11 = item.selected ? 'checked' : 'not checked';
    const iosAnnocementAy11 =
      Platform.OS === 'ios' ? `checkbox ${isCheckedAy11}` : '';
    return (
      <View style={styles.departmentListItem}>
        <View
          style={{flexDirection: 'row', flex: 1}}
          accessibilityLabel={`${item[idKey]} ${item[titleKey]} ${iosAnnocementAy11}`}>
          <Text style={styles.listItemText}>
            {`${item[idKey]} ${item[titleKey]}`}
          </Text>
        </View>
        <View style={{alignSelf: 'flex-end'}}>
          <ChevronRightIcon size={'medium'} />
        </View>
      </View>
    );
  };

  const renderCategoryListItem = ({
    item,
    index,
  }: {
    item: Category;
    index: number;
  }) => {
    return (
      <View style={{marginLeft: 25}}>
        <Checkbox
          style={styles.categoriesListItem}
          indeterminate={false}
          checked={item.selected}
          label={`${item.CategoryId} ${item.CategoryDescription}`}
          key={item.CategoryId}
          onPress={() => {
            selectItem(item);
          }}
          {...accessibilityId(`checkbox${index}_${item.CategoryId}`)}
          accessibilityLabel={`${item.CategoryId} ${item.CategoryDescription}`}
          accessibilityRole="checkbox"
          testID={`checkbox${index}_${item.CategoryId}`}
        />
        <Divider />
      </View>
    );
  };

  const renderCategoriesListHeader = () => {
    const allCategoriesId = 'allCategories';
    const accessibilityState = () => {
      if (
        departmentForCategoryListView?.isAllCategoriesSelected === 'checked'
      ) {
        return true;
      } else if (
        departmentForCategoryListView?.isAllCategoriesSelected ===
        'indeterminate'
      ) {
        return 'mixed';
      } else {
        return false;
      }
    };

    return (
      <>
        <Text style={styles.listItemText}>
          {`${departmentForCategoryListView?.Department} ${departmentForCategoryListView?.DepartmentDescription}`}
        </Text>
        <Checkbox
          style={styles.categoriesListItem}
          indeterminate={
            departmentForCategoryListView?.isAllCategoriesSelected ===
            'indeterminate'
          }
          checked={
            departmentForCategoryListView?.isAllCategoriesSelected === 'checked'
          }
          accessibilityState={{checked: accessibilityState()}}
          label={`${t('textConstants.ALL_CATEGORIES')}`}
          key={allCategoriesId}
          accessibilityLabel={`${t('textConstants.ALL_CATEGORIES')}`}
          accessibilityRole="checkbox"
          {...accessibilityId(`checkbox${allCategoriesId}`)}
          onPress={() => {
            departmentForCategoryListView &&
              handleSelectAllCategoriesAction(departmentForCategoryListView);
          }}
          testID={'checkbox_allCategories'}
        />
        <Divider />
      </>
    );
  };

  const renderDepartmentListHeader = () => {
    if (!currentlySelectedDepartment) {
      return;
    }
    const selectedCategoriesCount =
      currentlySelectedDepartment.Categories.filter(
        category => category.selected,
      ).length;
    const totalCategoriesCount = currentlySelectedDepartment.Categories.length;
    return (
      <>
        <Text style={styles.subtitle} testID="SELECTED_DEPARTMENT">
          {t('textConstants.SELECTED_DEPARTMENT')}
        </Text>

        <TouchableOpacity
          style={styles.departmentHeaderCard}
          {...accessibilityId(
            `currentlySelected_${currentlySelectedDepartment.Department}`,
          )}
          accessibilityRole="button"
          accessibilityLabel={`${t('textConstants.SELECTED_DEPARTMENT')}, ${
            currentlySelectedDepartment.Department
          }, ${
            currentlySelectedDepartment.DepartmentDescription
          }. ${selectedCategoriesCount} of ${totalCategoriesCount} ${t(
            'textConstants.CATEGORIES_SELECTED',
          )}`}
          onPress={() => {
            flipToCategoriesListView(currentlySelectedDepartment);
          }}
          testID="SELECTED_DEPARTMENT_BUTTON">
          <View>
            <Text style={styles.selectedDeptTitle}>
              {`${currentlySelectedDepartment.Department} ${currentlySelectedDepartment.DepartmentDescription}`}
            </Text>
            <Text style={styles.selectedDeptSubtitle}>
              {`${selectedCategoriesCount}/${totalCategoriesCount} ${t(
                'textConstants.CATEGORIES_SELECTED',
              )}`}
            </Text>
          </View>
          <View style={{justifyContent: 'space-around', marginRight: 8}}>
            <ChevronRightIcon size={'medium'} />
          </View>
        </TouchableOpacity>

        <Text style={styles.subtitle}>
          {t('textConstants.ALL_DEPARTMENTS')}
        </Text>
      </>
    );
  };

  const renderDepartmentListItem = ({
    item,
    index,
  }: {
    item: Departments;
    index: number;
  }) => {
    return (
      <>
        <TouchableOpacity
          {...accessibilityId(`${item.Department}`)}
          accessibilityRole="button"
          accessibilityLabel={`${item.Department}, ${item.DepartmentDescription}`}
          onPress={() => {
            flipToCategoriesListView(item);
          }}>
          {departmentListItem(
            item,
            'Department',
            'DepartmentDescription',
            index,
          )}
        </TouchableOpacity>
        <Divider />
      </>
    );
  };

  const departmentFlatList = (
    <View style={{flex: 1, paddingBottom: bottom}}>
      <FlatList
        ref={departmentListRef}
        ListHeaderComponent={renderDepartmentListHeader}
        nestedScrollEnabled={true}
        data={departmentList}
        renderItem={renderDepartmentListItem}
        keyExtractor={departmentsKeyExtractor}
        maxToRenderPerBatch={10}
        extraData={toggle}
      />
    </View>
  );

  const categoryFlatList = (
    <View style={{flex: 1, paddingBottom: bottom}}>
      <FlatList
        ref={categoryListRef}
        ListHeaderComponent={renderCategoriesListHeader}
        nestedScrollEnabled={true}
        data={departmentForCategoryListView?.Categories}
        renderItem={renderCategoryListItem}
        keyExtractor={categoriesKeyExtractor}
        maxToRenderPerBatch={10}
        extraData={toggle}
      />
    </View>
  );

  const renderList = (state: ScreenState) => {
    switch (state) {
      case ScreenState.DepartmentList:
        return departmentFlatList;
      case ScreenState.CategoryList:
        return categoryFlatList;
    }
  };

  const screenTitle = (state: ScreenState) => {
    switch (screenState) {
      case ScreenState.DepartmentList:
        return t('textConstants.DEPARTMENTS');
      case ScreenState.CategoryList:
        return `${t('textConstants.DEPT')} ${
          departmentForCategoryListView?.Department
        } ${t('textConstants.CATEGORIES')}`;
    }
  };

  const backButtonAction = () => {
    setScreenState(ScreenState.DepartmentList);
  };

  const t = (x: string) => x;

  return (
    <BottomSheet
      //   UNSAFE_style={GlobalStyle.style.bottomSheetRadius}
      childrenContainScrollableComponent={true}
      isOpen={visible}
      onClose={onClose}
      onOpen={onOpen}
      backdropColor="gray"
      title={
        <View style={styles.titleContainer}>
          {screenState === ScreenState.CategoryList ? (
            <IconButton
              size="medium"
              onPress={backButtonAction}
              UNSAFE_style={styles.iconButton}
              accessibilityRole="button"
              accessibilityLabel="Back">
              <ChevronLeftIcon />
            </IconButton>
          ) : (
            <View style={{height: 40, width: 24}} />
          )}
          <Text style={styles.title} accessibilityRole="header">
            {screenTitle(screenState)}
          </Text>
        </View>
      }
      {...accessibilityId('departmentFilterModal')}>
      <View style={styles.containerStyle}>
        {renderList(screenState)}
        <View
          style={{
            borderColor: '#ccc',
            paddingTop: 20,
            borderTopWidth: 0.5,
            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',
            bottom: bottom,
          }}>
          <Button
            {...accessibilityId('clearDepartmentFilter')}
            variant={'tertiary'}
            size="small"
            onPress={clearFilter}>
            {t('textConstants.CLEAR_FILTER')}
          </Button>
          <View style={{flex: 1, paddingHorizontal: 10}}>
            <Button
              {...accessibilityId('applyDepartmentFilter')}
              isFullWidth={true}
              size="small"
              variant={'primary'}
              onPress={applySelectedFilter}>
              {t('textConstants.APPLY')}
            </Button>
          </View>
        </View>
      </View>
    </BottomSheet>
  );
};

const styles = StyleSheet.create({
  containerStyle: {flex: 1},
  titleContainer: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    alignItems: 'center',
  },
  title: {
    fontFamily: 'Bogle-Bold',
    fontSize: 16,
    textAlign: 'center',
    color: '#2e2f32',
    width: '90%',
  },
  iconButton: {
    marginLeft: -12,
  },
  categoriesListItem: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 16,
  },
  departmentListItem: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 16,
  },
  departmentHeaderCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: '#E6F1FC',
    width: '100%',
    paddingVertical: 12,
    paddingLeft: 16,
    borderRadius: 8,
    marginTop: 8,
    marginBottom: 24,
  },
  subtitle: {
    fontFamily: 'Bogle-Bold',
    fontSize: 16,
    textAlign: 'left',
    lineHeight: 24,
    color: '#2e2f32',
  },
  selectedDeptTitle: {
    fontFamily: 'Bogle-Regular',
    fontSize: 16,
    textAlign: 'left',
    lineHeight: 24,
    color: '#2e2f32',
  },
  selectedDeptSubtitle: {
    fontFamily: 'Bogle-Regular',
    fontSize: 14,
    textAlign: 'left',
    lineHeight: 20,
    color: '#2e2f32',
  },
  listItemText: {
    fontFamily: 'Bogle-Regular',
    fontSize: 16,
    textAlign: 'left',
    lineHeight: 24,
    color: '#2e2f32',
  },
});

export interface TestIDType {
  accessibilityLabel?: string;
  testID: string;
}

export const accessibilityId: (_testId: string) => TestIDType = (
  _testID: string,
) => ({
  testID: _testID,
});
