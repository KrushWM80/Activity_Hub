import * as React from 'react';
import {Header} from '../components';
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableHeaderSelect,
  DataTableCellSelect,
  DataTableRow,
} from '@walmart/gtp-shared-components';
import {dataTable} from './screensFixtures';

const DataTableCheckboxRecipe = () => {
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
          {headerLabels.map((label, index) => (
            <DataTableHeader key={index} numberOfColumns={totalHeader}>
              {label}
            </DataTableHeader>
          ))}
          <DataTableHeaderSelect
            key={'headerSelect_'}
            alignment={'right'}
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

  const renderTableBodySelect = (data: Array<any>) => {
    return (
      <DataTableBody key={'body'}>
        {data.map(item => {
          const {id, name, itemNumber, itemName, dDate} = item;
          const columns = 3;
          return (
            <DataTableRow key={id}>
              <DataTableCell key={'id'} numberOfColumns={columns}>
                {id ?? itemNumber}
              </DataTableCell>
              <DataTableCell key={'name'} numberOfColumns={columns}>
                {name ?? itemName}
              </DataTableCell>
              <DataTableCellSelect
                variant="numeric"
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
    <>
      <Header>Data Table with checkBox</Header>
      <DataTable key={'simple'}>
        {renderTableHeaderSelect(dataTable.selectHeader)}
        {renderTableBodySelect(simpleData)}
      </DataTable>
    </>
  );
};

export {DataTableCheckboxRecipe};
