import React, {useCallback, useMemo} from 'react';
import {View, StyleSheet} from 'react-native';
import {
  Caption,
  Card,
  Heading,
  Alert,
  List,
} from '@walmart/gtp-shared-components';
import {TaskItem} from '../components/TaskItem';
import {alertRecipeData} from './screensFixtures';
const AlertRecipe = () => {
  const errorAlert = useCallback((task: any) => {
    const {alertContent} = task;
    if (alertContent) {
      return (
        <View style={ss.margins}>
          <Alert variant="warning" children={alertContent} />
        </View>
      );
    }
    return null;
  }, []);

  const TaskItemList = useMemo(() => {
    return (
      <List>
        {alertRecipeData?.map(task => {
          return (
            <View style={ss.taskItemContainer} key={`_${task.TaskName}`}>
              <TaskItem taskName={task.TaskName} />
              {errorAlert(task)}
            </View>
          );
        })}
      </List>
    );
  }, [errorAlert]);
  return (
    <Card UNSAFE_style={ss.margins}>
      <View style={ss.cardContainer}>
        <Caption children={'taskCaption'} />
        <Heading children={'taskTitle'} />
      </View>
      {TaskItemList}
    </Card>
  );
};
const ss = StyleSheet.create({
  cardContainer: {
    width: '100%',
    paddingHorizontal: 16,
    paddingTop: 16,
  },
  margins: {marginHorizontal: 16, marginBottom: 16},
  taskItemContainer: {flex: 1},
});
export {AlertRecipe};
