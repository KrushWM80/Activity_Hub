import * as React from 'react';
import {Header} from '../components';
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableCellActions,
  TextField,
  IconButton,
  Icons,
  DataTableRow,
} from '@walmart/gtp-shared-components';
import {dataTable, displayPopupAlert} from './screensFixtures';

const DataTableCellActionsRecipe = () => {
  const [actionData, setActionData] = React.useState(dataTable.actionData);

  const renderTableHeaderSelect = (headerLabels: Array<any>) => {
    return (
      <DataTableHead key={'simple'}>
        <DataTableRow key={'simple_row'}>
          {headerLabels.map((label, index) => (
            <DataTableHeader
              key={index}
              width={index === 0 ? '20%' : index === 1 ? '50%' : '30%'}
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

  const updateData = (
    actionType: string,
    rowId: number,
    updatedValue: string = '',
  ) => {
    let updatedArray = actionData;
    if (actionType === 'Edit') {
      updatedArray = actionData.map(item => {
        const {id, name, isEdit} = item;
        if (id === rowId) {
          return {id: id, name: isEdit ? updatedValue : name, isEdit: true};
        } else {
          return {id, name, isEdit};
        }
      });
    } else if (actionType === 'EditDone') {
      updatedArray = actionData.map(item => {
        const {id, name, isEdit} = item;
        if (id === rowId) {
          return {id: id, name: name, isEdit: false};
        } else {
          return {id, name, isEdit};
        }
      });
    } else {
      updatedArray = actionData.filter(item => item.id !== rowId);
    }
    setActionData(updatedArray);
  };
  const renderTableBodySelect = (data: Array<any>) => {
    return (
      <DataTableBody key={'body'}>
        {data.map(item => {
          const {id, name, isEdit} = item;
          return (
            <DataTableRow key={id}>
              <DataTableCell key={'id'} width={'20%'}>
                {id}
              </DataTableCell>
              {isEdit ? (
                <TextField
                  value={name}
                  label={''}
                  onChangeText={value =>
                    updateData('Edit', id, value as string)
                  }
                  onSubmitEditing={() => {
                    updateData('EditDone', id);
                  }}
                />
              ) : (
                <DataTableCell key={'name'} width={'50%'}>
                  {name}
                </DataTableCell>
              )}
              <DataTableCellActions alignment="right" width={'30%'}>
                <IconButton
                  children={<Icons.PencilIcon />}
                  size="small"
                  onPress={() => {
                    updateData('Edit', id);
                  }}
                />
                <IconButton
                  children={<Icons.TrashCanIcon />}
                  size="small"
                  onPress={() => {
                    updateData('Delete', id);
                    displayPopupAlert(
                      'Deleted',
                      `Item ${id} deleted successfully`,
                    );
                  }}
                />
              </DataTableCellActions>
            </DataTableRow>
          );
        })}
      </DataTableBody>
    );
  };

  return (
    <>
      <Header>Data Table with Actions</Header>
      <DataTable key={'simple'}>
        {renderTableHeaderSelect(dataTable.actionHeader)}
        {renderTableBodySelect(actionData)}
      </DataTable>
    </>
  );
};

export {DataTableCellActionsRecipe};
