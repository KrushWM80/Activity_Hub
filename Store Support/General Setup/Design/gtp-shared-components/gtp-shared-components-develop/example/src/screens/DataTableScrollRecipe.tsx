import * as React from 'react';
import {StyleSheet} from 'react-native';
import {Header, VariantText, Page} from '../components';
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableRow,
} from '@walmart/gtp-shared-components';
import {dataTable} from './screensFixtures';

const DataTableScrollRecipe = () => {
  const renderTableHeader = (headerLabels: Array<any>) => {
    return (
      <DataTableHead key={`header_${headerLabels.length}`}>
        <DataTableRow>
          {headerLabels.map((label, index) => (
            <DataTableHeader
              key={index}
              alignment={
                dataTable.rightAlignLabel.includes(label) ? 'right' : 'left'
              }>
              {label}
            </DataTableHeader>
          ))}
        </DataTableRow>
      </DataTableHead>
    );
  };

  const renderTableBody = (data: Array<any>) => {
    return (
      <DataTableBody key={'body'}>
        {data.map(item => {
          const {itemNumber, itemName, quantity, dDate, id, name, count, date} =
            item;
          return (
            <DataTableRow key={`${itemNumber}_${data.length}`}>
              <DataTableCell key={'id'}>{itemNumber ?? id}</DataTableCell>
              {name && <DataTableCell key={'name'}>{name}</DataTableCell>}
              <DataTableCell key={'itemName'}>{itemName}</DataTableCell>
              {count && (
                <DataTableCell variant="numeric" key={'count'}>
                  {count}
                </DataTableCell>
              )}
              <DataTableCell variant="numeric" key={'quantity'}>
                {quantity}
              </DataTableCell>
              <DataTableCell key={'dDate'}>{dDate ?? date}</DataTableCell>
            </DataTableRow>
          );
        })}
      </DataTableBody>
    );
  };

  return (
    <Page>
      <Header>
        Data Table <VariantText>horizontal prop false</VariantText>
      </Header>

      <DataTable key={'scroll1'} UNSAFE_style={style.tableHeight}>
        {renderTableHeader(dataTable.scrollHeader)}
        {renderTableBody(dataTable.scrollData)}
      </DataTable>
      <Header>
        Data Table <VariantText>horizontal prop True</VariantText>
      </Header>
      <DataTable
        key={'scroll2'}
        horizontalScroll={true}
        UNSAFE_style={style.tableHeight}>
        {renderTableHeader(dataTable.scrollHeader)}
        {renderTableBody(dataTable.scrollData)}
      </DataTable>
      <Header>
        Data Table
        <VariantText>
          Auto horizontal true when No.Of.columns &gt; 5
        </VariantText>{' '}
      </Header>
      <DataTable key={'autoHorizontal'} UNSAFE_style={style.tableHeight}>
        {renderTableHeader(dataTable.autoHorizontalHeader)}
        {renderTableBody(dataTable.autoHorizontalData)}
      </DataTable>
    </Page>
  );
};
const style = StyleSheet.create({
  tableHeight: {
    height: 400,
  },
});
export {DataTableScrollRecipe};
