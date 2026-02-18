import * as React from 'react';
import {Header, Page} from '../components';
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableHeaderSelect,
  DataTableCellSelect,
  DataTableBulkActions,
  DataTableRow,
  ButtonGroup,
  Button,
} from '@walmart/gtp-shared-components';
import {dataTable, displayPopupAlert} from './screensFixtures';

const DataTableBulkActionsRecipe = () => {
  const simpleData = dataTable.selectData;
  const [simpleHeaderChecked, setSimpleHeaderChecked] = React.useState<
    string[]
  >([]);
  const [isHeaderPressed, setHeaderPressed] = React.useState(false);
  const [simpleCellChecked, setSimpleCellChecked] = React.useState<string[]>(
    [],
  );

  const renderTableHeaderSelect = (headerLabels: Array<any>) => {
    const totalHeader = headerLabels.length + 1;
    return (
      <DataTableHead key={'simple'}>
        <DataTableRow key={'simple_row'}>
          <DataTableHeaderSelect
            key={'headerSelect_'}
            alignment={'left'}
            numberOfColumns={totalHeader}
            onChange={() => {
              setHeaderPressed(true);
              setSimpleHeaderChecked(
                addOrRemoveElement(simpleHeaderChecked, 'Check'),
              );
            }}
            indeterminate={
              simpleCellChecked.length > 0 && simpleHeaderChecked.length === 0
            }
            checked={simpleHeaderChecked.includes('Check')}
          />
          {headerLabels.map((label, index) => (
            <DataTableHeader key={index} numberOfColumns={totalHeader}>
              {label}
            </DataTableHeader>
          ))}
        </DataTableRow>
      </DataTableHead>
    );
  };

  React.useEffect(() => {
    if (simpleCellChecked.length === simpleData.length) {
      setSimpleHeaderChecked(['Check']);
    } else {
      setSimpleHeaderChecked([]);
    }
  }, [simpleCellChecked, simpleData]);

  React.useEffect(() => {
    if (isHeaderPressed) {
      if (simpleHeaderChecked.length === 1) {
        const ids = simpleData.map(item => `${item?.id}`);
        setSimpleCellChecked(ids);
      } else {
        setSimpleCellChecked([]);
      }
      setHeaderPressed(false);
    }
  }, [isHeaderPressed, simpleHeaderChecked, simpleData]);

  const addOrRemoveElement = (sourceArray: string[], label: string) => {
    if (sourceArray.includes(label)) {
      return sourceArray.filter(key => key !== label);
    } else {
      return [...sourceArray, label];
    }
  };

  const selectAll = () => {
    setSimpleHeaderChecked(['Check']);
    const ids = simpleData.map(item => `${item?.id}`);
    setSimpleCellChecked(ids);
  };
  const clearAll = () => {
    setSimpleHeaderChecked([]);
    setSimpleCellChecked([]);
  };
  const renderTableBodySelect = (data: Array<any>) => {
    return (
      <DataTableBody key={'body'}>
        {data.map(item => {
          const {id, name, itemNumber, itemName, dDate} = item;
          const columns = 3;
          return (
            <DataTableRow key={id}>
              <DataTableCellSelect
                variant="alphanumeric"
                key={'count'}
                numberOfColumns={columns}
                checked={simpleCellChecked.includes(`${id}`)}
                onChange={() => {
                  setHeaderPressed(false);
                  setSimpleCellChecked(
                    addOrRemoveElement(simpleCellChecked, `${id}`),
                  );
                }}
              />
              <DataTableCell key={'id'} numberOfColumns={columns}>
                {id ?? itemNumber}
              </DataTableCell>
              <DataTableCell key={'name'} numberOfColumns={columns}>
                {name ?? itemName}
              </DataTableCell>

              {dDate && (
                <DataTableCell key={'dDate'} numberOfColumns={columns}>
                  {dDate}
                </DataTableCell>
              )}
            </DataTableRow>
          );
        })}
      </DataTableBody>
    );
  };

  return (
    <Page>
      <Header>Data Table with Bulk Actions</Header>
      <DataTableBulkActions
        actionContent={
          <ButtonGroup>
            <Button
              onPress={() =>
                displayPopupAlert(
                  'Action 1',
                  `Selected Ids ${simpleCellChecked}`,
                )
              }>
              Custom Action 1
            </Button>
            <Button
              onPress={() =>
                displayPopupAlert(
                  'Action 2',
                  `Selected Ids ${simpleCellChecked}`,
                )
              }>
              Custom Action 2
            </Button>
          </ButtonGroup>
        }
        count={simpleCellChecked.length}
        onClearSelected={clearAll}
        onSelectAll={selectAll}
      />
      <DataTable key={'simple'}>
        {renderTableHeaderSelect(dataTable.selectHeader)}
        {renderTableBodySelect(simpleData)}
      </DataTable>
    </Page>
  );
};

export {DataTableBulkActionsRecipe};
