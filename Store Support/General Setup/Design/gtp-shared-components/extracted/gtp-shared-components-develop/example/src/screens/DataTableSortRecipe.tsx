import * as React from 'react';
import {Header} from '../components';
import {View, StyleSheet} from 'react-native';
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableRow,
  useSimpleReducer,
  DataTableHeaderSortType,
} from '@walmart/gtp-shared-components';
import {dataTable} from './screensFixtures';

type SortType = {
  simplSortType: DataTableHeaderSortType;
  scrollSortType: DataTableHeaderSortType;
};

const initialState: SortType = {
  simplSortType: 'ascending',
  scrollSortType: 'descending',
};

const DataTableSortRecipe = () => {
  const [state, setState] = useSimpleReducer<SortType>(initialState);

  const sortNumber = (a: string, b: string, type: string) => {
    const valueA = parseInt(a.replace(/,/g, ''), 10);
    const valueB = parseInt(b.replace(/,/g, ''), 10);
    return type === 'descending' ? valueB - valueA : valueA - valueB;
  };
  const sortString = (a: string, b: string, type: string) => {
    return type === 'descending' ? b.localeCompare(a) : a.localeCompare(b);
  };

  const onDataSort = (tableType: string, type: DataTableHeaderSortType) => {
    if (tableType === 'simple') {
      let sortedArray = simpleData;
      if (type !== 'none') {
        sortedArray = [...dataTable.simpleData].sort((a, b) =>
          sortString(a.name, b.name, type),
        );
      }
      setState('simplSortType', type);
      setSimpleData(sortedArray);
    } else {
      let sortedArray = scrollData;
      if (type !== 'none') {
        sortedArray = [...dataTable.scrollData].sort((a, b) =>
          sortNumber(a.quantity, b.quantity, type),
        );
      }
      setScrollData(sortedArray);
      setState('scrollSortType', type);
    }
  };
  const [simpleData, setSimpleData] = React.useState(
    dataTable.simpleData.sort((a, b) =>
      sortString(a.name, b.name, 'ascending'),
    ),
  );
  const [scrollData, setScrollData] = React.useState(
    dataTable.scrollData.sort((a, b) =>
      sortNumber(a.quantity, b.quantity, 'descending'),
    ),
  );

  const renderTableHeader = (
    headerLabels: Array<any>,
    tableType: string,
    sortType: DataTableHeaderSortType,
  ) => {
    return (
      <DataTableHead key={tableType}>
        <DataTableRow>
          {headerLabels.map((label, index) =>
            dataTable.sortLabel.includes(label) ? (
              <DataTableHeader
                key={index}
                alignment={
                  dataTable.rightAlignLabel.includes(label) ? 'right' : 'left'
                }
                sort={sortType}
                onSort={type =>
                  onDataSort(tableType, type as DataTableHeaderSortType)
                }>
                {label}
              </DataTableHeader>
            ) : (
              <DataTableHeader
                key={index}
                alignment={
                  dataTable.rightAlignLabel.includes(label) ? 'right' : 'left'
                }>
                {label}
              </DataTableHeader>
            ),
          )}
        </DataTableRow>
      </DataTableHead>
    );
  };

  const renderTableBody = (data: Array<any>) => {
    return (
      <DataTableBody key={`body_${data.length}`}>
        {data.map(item => {
          const {id, name, count, itemNumber, itemName, quantity, date, dDate} =
            item;
          return (
            <DataTableRow key={id ?? itemNumber}>
              <DataTableCell key={'id'}>{id ?? itemNumber}</DataTableCell>
              {name && <DataTableCell key={'name'}>{name}</DataTableCell>}
              {itemName && (
                <DataTableCell key={'itemName'}>{itemName}</DataTableCell>
              )}
              {count && (
                <DataTableCell variant="numeric" key={'count'}>
                  {count}
                </DataTableCell>
              )}
              {quantity && (
                <DataTableCell key={'quantity'} variant="numeric">
                  {quantity}
                </DataTableCell>
              )}
              {(dDate || date) && (
                <DataTableCell key={'dDate'}>{dDate ?? date}</DataTableCell>
              )}
            </DataTableRow>
          );
        })}
      </DataTableBody>
    );
  };

  return (
    <>
      <Header>Data Table For Sort</Header>
      <View style={styles.tableOne}>
        <DataTable key={'simple'}>
          {renderTableHeader(
            dataTable.simpleHeader,
            'simple',
            state.simplSortType as DataTableHeaderSortType,
          )}
          {renderTableBody(simpleData)}
        </DataTable>
      </View>
      <DataTable key={'scroll'}>
        {renderTableHeader(
          dataTable.scrollHeader,
          'scroll',
          state.scrollSortType as DataTableHeaderSortType,
        )}
        {renderTableBody(scrollData)}
      </DataTable>
    </>
  );
};
const styles = StyleSheet.create({
  tableOne: {
    height: 230,
  },
});
export {DataTableSortRecipe};
