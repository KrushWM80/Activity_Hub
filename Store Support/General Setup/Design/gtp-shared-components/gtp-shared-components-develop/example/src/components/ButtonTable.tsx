import * as React from 'react';
import {View, StyleSheet} from 'react-native';
import ButtonContainer from '../components/ButtonContainer';
import {colors, Divider, Icons} from '@walmart/gtp-shared-components';

interface ButtonTableProps {
  button: React.ReactElement;
  small?: boolean;
  isFullWidth?: boolean;
  isLoading?: boolean;
  color?: string;
  leading?: React.ReactElement;
  trailing?: React.ReactElement;
}

const ButtonTable: React.FC<ButtonTableProps> = ({
  button,
  isFullWidth = true,
  isLoading = false,
  color = colors.gray['10'],
  leading,
  trailing,
}: ButtonTableProps) => {
  return (
    <View style={[styles.outerContainer, {backgroundColor: color}]}>
      <View style={styles.innerContainer}>
        <View style={styles.container}>
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Small',
              size: 'small',
            })}
          </ButtonContainer>
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Small',
              size: 'small',
              isLoading,
            })}
          </ButtonContainer>
          <Divider />
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Medium',
              size: 'medium',
            })}
          </ButtonContainer>
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Medium',
              size: 'medium',
              isLoading,
            })}
          </ButtonContainer>
          <Divider />

          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Large',
              size: 'large',
            })}
          </ButtonContainer>
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Large',
              size: 'large',
              isLoading,
            })}
          </ButtonContainer>
          <Divider />
        </View>
        <View style={styles.container}>
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Small',
              disabled: true,
              size: 'small',
            })}
          </ButtonContainer>
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Small',
              disabled: true,
              size: 'small',
              isLoading,
            })}
          </ButtonContainer>
          <Divider />
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Medium',
              disabled: true,
              size: 'medium',
            })}
          </ButtonContainer>
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Medium',
              disabled: true,
              size: 'medium',
              isLoading,
            })}
          </ButtonContainer>
          <Divider />
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Large',
              disabled: true,
              size: 'large',
            })}
          </ButtonContainer>
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Large',
              disabled: true,
              size: 'large',
              isLoading,
            })}
          </ButtonContainer>
          <Divider />
        </View>
      </View>
      {leading && (
        <View style={styles.innerContainer}>
          <View style={styles.container}>
            <ButtonContainer>
              {React.cloneElement(button, {
                children: 'With leading',
                leading,
              })}
            </ButtonContainer>
            <ButtonContainer>
              {React.cloneElement(button, {
                children: 'With leading',
                leading,
                isLoading,
              })}
            </ButtonContainer>
            <Divider />
          </View>
          <View style={styles.container}>
            <ButtonContainer>
              {React.cloneElement(button, {
                children: 'With leading',
                leading,
                disabled: true,
              })}
            </ButtonContainer>
            <ButtonContainer>
              {React.cloneElement(button, {
                children: 'With leading',
                leading,
                disabled: true,
                isLoading,
              })}
            </ButtonContainer>
            <Divider />
          </View>
        </View>
      )}
      {trailing && (
        <View style={styles.innerContainer}>
          <View style={styles.container}>
            <ButtonContainer>
              {React.cloneElement(button, {
                children: 'With trailing',
                trailing,
              })}
            </ButtonContainer>
            <ButtonContainer>
              {React.cloneElement(button, {
                children: 'With trailing',
                trailing,
                isLoading,
              })}
            </ButtonContainer>
            <Divider />
          </View>
          <View style={styles.container}>
            <ButtonContainer>
              {React.cloneElement(button, {
                children: 'With trailing',
                trailing,
                disabled: true,
              })}
            </ButtonContainer>
            <ButtonContainer>
              {React.cloneElement(button, {
                children: 'With trailing',
                trailing,
                disabled: true,
                isLoading,
              })}
            </ButtonContainer>
            <Divider />
          </View>
        </View>
      )}
      {isFullWidth && (
        <>
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Beam me up, Scotty',
              isFullWidth: true,
              leading: <Icons.ArrowUpIcon color={colors.white} />,
              trailing: <Icons.ExternalLinkIcon color={colors.white} />,
            })}
          </ButtonContainer>
          <ButtonContainer>
            {React.cloneElement(button, {
              children: 'Beam me up, Scotty',
              isFullWidth: true,
              isLoading,
            })}
          </ButtonContainer>
        </>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  outerContainer: {
    padding: 10,
    borderBottomLeftRadius: 12,
    borderBottomRightRadius: 12,
    borderBottomWidth: 1,
    borderLeftWidth: 1,
    borderRightWidth: 1,
    borderBottomColor: colors.gray['10'],
    borderLeftColor: colors.gray['10'],
    borderRightColor: colors.gray['10'],
  },
  innerContainer: {
    flexDirection: 'row',
  },
  container: {
    flex: 1,
    flexDirection: 'column',
    alignItems: 'center',
  },
  divider: {
    height: 4,
  },
});

export default ButtonTable;
