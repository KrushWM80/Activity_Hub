import {StyleSheet, View} from 'react-native';
import React, {FC, useMemo} from 'react';
import {Body, Button, PhoneIcon, colors} from '@walmart/gtp-shared-components';

type Props = {
  taskName: string;
  isEdit?: boolean;
  action?: (task: string) => void;
};
interface TaskContent {
  title: string;
  subTitle: string;
  media: React.ReactNode;
  completeStatus: string;
}

const TaskItem: FC<Props> = ({taskName, isEdit}) => {
  const taskContent: TaskContent = useMemo(() => {
    return {
      title: `tasks.${taskName}.title`,
      subTitle: `tasks.${taskName}.subTitle`,
      media: <PhoneIcon />,
      completeStatus: `tasks.${taskName}.completeStatus`,
    };
  }, [taskName]);

  const statusContent = () => {
    // Return complete status

    //return initial status
    return 'Start';
  };

  return (
    <View style={ss.taskContainer}>
      <View style={ss.taskStatusContainer}>
        <PhoneIcon />
      </View>
      <View style={ss.taskContent}>
        <Body size="medium" weight={isEdit ? '700' : '400'}>
          {taskContent?.title}
        </Body>
        <Body size="small" UNSAFE_style={{color: colors?.gray[100]}}>
          {statusContent()}
        </Body>
      </View>
      <View style={ss.buttonContainer}>
        {isEdit ? (
          <Button onPress={() => {}} variant="tertiary" children={'taskEdit'} />
        ) : (
          <Button
            onPress={() => {}}
            variant="secondary"
            children={'taskStart'}
          />
        )}
      </View>
    </View>
  );
};
const ss = StyleSheet.create({
  taskContainer: {
    flex: 1,
    flexDirection: 'row',
    paddingHorizontal: 16,
    padding: 16,
  },
  buttonContainer: {width: '30%', alignItems: 'flex-end'},
  taskStatusContainer: {width: '10%', marginTop: 6},
  taskContent: {width: '60%'},
});
export {TaskItem};
