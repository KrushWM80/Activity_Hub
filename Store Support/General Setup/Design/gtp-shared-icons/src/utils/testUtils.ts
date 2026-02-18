import {Platform} from 'react-native';

const testID = (id: string) =>
  Platform.OS === 'ios'
    ? {testID: id}
    : {accessible: true, accessibilityLabel: id};

export {testID};
