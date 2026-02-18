import * as React from 'react';
import {Header} from '../components';
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableCellStatus,
  DataTableRow,
  Tag,
} from '@walmart/gtp-shared-components';
import {dataTable} from './screensFixtures';

const DataTableStatusRecipe = () => {
  const simpleData = dataTable.statusData;
  const numberOfColumns = dataTable.statusHeader.length;
  const renderTableHeader = (headerLabels: Array<any>) => {
    return (
      <DataTableHead key={'simple'}>
        <DataTableRow key={'simple_row'}>
          {headerLabels.map((label, index) => (
            <DataTableHeader key={index} numberOfColumns={numberOfColumns}>
              {label}
            </DataTableHeader>
          ))}
        </DataTableRow>
      </DataTableHead>
    );
  };
  const renderTag = (status: string, id: number) => {
    const color = id === 1 ? 'green' : id === 2 ? 'purple' : 'gray';
    return (
      <Tag color={color} variant={'tertiary'}>
        {status}
      </Tag>
    );
  };
  const renderTableBody = (data: Array<any>) => {
    return (
      <DataTableBody key={'body'}>
        {data.map(item => {
          const {id, name, status} = item;
          return (
            <DataTableRow key={id}>
              <DataTableCell key={'name'} numberOfColumns={numberOfColumns}>
                {name}
              </DataTableCell>
              <DataTableCellStatus numberOfColumns={numberOfColumns}>
                {renderTag(status, id)}
              </DataTableCellStatus>
            </DataTableRow>
          );
        })}
      </DataTableBody>
    );
  };

  return (
    <>
      <Header>Data Table with Status</Header>
      <DataTable key={'simple'}>
        {renderTableHeader(dataTable.statusHeader)}
        {renderTableBody(simpleData)}
      </DataTable>
    </>
  );
};

export {DataTableStatusRecipe};
