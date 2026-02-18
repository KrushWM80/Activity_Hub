import * as React from 'react';
import {View, StyleSheet} from 'react-native';
import {Header} from '../components';
import {
  DataTable,
  DataTableBody,
  DataTableCell,
  DataTableHead,
  DataTableHeader,
  DataTableCellActions,
  DataTableCellActionsMenu,
  DataTableCellActionsMenuItem,
  IconButton,
  Icons,
  DataTableRow,
} from '@walmart/gtp-shared-components';
import {dataTable, displayPopupAlert} from './screensFixtures';

const DataTableCellActionsMenuRecipe = () => {
  const [rowId, setRowId] = React.useState(0);
  const renderTableHeaderSelect = (headerLabels: Array<any>) => {
    return (
      <DataTableHead key={'simple'}>
        <DataTableRow key={'simple_row'}>
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

  const isMenuOpen = (_rowId: number): boolean => {
    return rowId === _rowId;
  };
  const setMenuRow = (_rowId: number) => {
    setRowId(_rowId);
  };
  const renderTableBodySelect = (data: Array<any>) => {
    return (
      <DataTableBody key={'body'}>
        {data.map(item => {
          const {id, name} = item;
          return (
            <DataTableRow key={id}>
              <DataTableCell key={'id'}>{id}</DataTableCell>
              <DataTableCell key={'name'}>{name}</DataTableCell>
              <DataTableCellActions alignment="right">
                <IconButton
                  children={<Icons.PencilIcon />}
                  size="small"
                  onPress={() =>
                    displayPopupAlert(
                      'Action',
                      `Edit button pressed for ${name}`,
                    )
                  }
                />
                <IconButton
                  children={<Icons.TrashCanIcon />}
                  size="small"
                  onPress={() =>
                    displayPopupAlert(
                      'Action',
                      `Delete button pressed for ${name}`,
                    )
                  }
                />
                <DataTableCellActionsMenu
                  isOpen={isMenuOpen(id)}
                  onClose={() => setMenuRow(0)}
                  trigger={
                    <IconButton
                      children={<Icons.MoreIcon />}
                      onPress={() => setMenuRow(id)}
                    />
                  }>
                  <DataTableCellActionsMenuItem
                    onPress={() => {
                      displayPopupAlert(
                        'Email',
                        `Email Action Pressed ${name}`,
                      );
                    }}>
                    Email
                  </DataTableCellActionsMenuItem>
                  <DataTableCellActionsMenuItem
                    onPress={() => {
                      displayPopupAlert(
                        'Print',
                        `Print Action Pressed ${name}`,
                      );
                    }}>
                    Print
                  </DataTableCellActionsMenuItem>
                  <DataTableCellActionsMenuItem
                    onPress={() => {
                      displayPopupAlert(
                        'Disable',
                        `Disable Action Pressed ${name}`,
                      );
                      setMenuRow(0);
                    }}>
                    Disable
                  </DataTableCellActionsMenuItem>
                </DataTableCellActionsMenu>
              </DataTableCellActions>
            </DataTableRow>
          );
        })}
      </DataTableBody>
    );
  };

  return (
    <View style={styles.container}>
      <Header>Data Table with Action Menus</Header>
      <DataTable key={'simple'}>
        {renderTableHeaderSelect(dataTable.menuHeader)}
        {renderTableBodySelect(dataTable.menuData)}
      </DataTable>
    </View>
  );
};
const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 8,
  },
});

export {DataTableCellActionsMenuRecipe};
