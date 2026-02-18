import * as React from 'react';
import {StyleSheet} from 'react-native';
import {Header, Section, VariantText} from '.';
import {Button, BottomSheet, Carousel} from '@walmart/gtp-shared-components';
import {
  LongBottomSheetContent,
  ShortBottomSheetContent,
  carouselItems,
  carouselHeader,
  carouselFooter,
} from '../screens/screensFixtures';
import {IconsOverview} from '../screens';

const BottomSheetsLegacy = () => {
  type bsStateType = {
    bottomSheetSize?: number | 'auto' | 'small' | 'medium' | 'large';
    bottomSheetContent?: number;
    bottomSheetDismissable?: boolean;
    bottomSheetResizable?: boolean;
    bottomSheetBack?: boolean;
    bottomSheetTitle?: string;
  };
  const [isSheetVisible, setIsSheetVisible] = React.useState(false);
  const [isBsCarouselSheetVisible, setIsBsCarouselSheetVisible] =
    React.useState(false);
  const [isBsIconsSheetVisible, setIsBsIconsSheetVisible] =
    React.useState(false);

  const [bsState, setBsState] = React.useState({
    bottomSheetSize: 0,
    bottomSheetDismissable: true,
    bottomSheetResizable: true,
    bottomSheetBack: true,
  } as Partial<bsStateType>);

  const handleOnResize = (height: number | undefined) =>
    console.log('---- height:', height);

  const closeModals = () => {
    handleOnResize(0);
    setIsSheetVisible(false);
    setIsBsCarouselSheetVisible(false);
    setIsBsIconsSheetVisible(false);
  };

  return (
    <>
      <Header>
        BottomSheet{'\n'}{' '}
        <VariantText>legacy calls (ensure backwards compatibility)</VariantText>
      </Header>
      <Section>
        <Button
          variant="primary"
          onPress={() => {
            setBsState({
              ...bsState,
              bottomSheetContent: 1,
              bottomSheetSize: 'auto',
              bottomSheetDismissable: true,
              bottomSheetResizable: true,
              bottomSheetBack: true,
              bottomSheetTitle: 'Auto Sheet Title',
            });
            setIsSheetVisible(true);
          }}>
          Auto-Sized Sheet w/Title
        </Button>
        <Button
          variant="primary"
          onPress={() => {
            setBsState({
              ...bsState,
              bottomSheetContent: 1,
              bottomSheetSize: 'large',
              bottomSheetDismissable: true,
              bottomSheetResizable: true,
              bottomSheetBack: true,
              bottomSheetTitle: undefined,
            });
            setIsSheetVisible(true);
          }}>
          Large Sheet
        </Button>
        <Button
          variant="primary"
          onPress={() => {
            setBsState({
              ...bsState,
              bottomSheetContent: 2,
              bottomSheetSize: 'auto',
              bottomSheetDismissable: true,
              bottomSheetResizable: false,
              bottomSheetBack: true,
              bottomSheetTitle: undefined,
            });
            setIsSheetVisible(true);
          }}>
          Dismissable Medium Sheet
        </Button>
        <Button
          variant="primary"
          onPress={() => {
            setBsState({
              ...bsState,
              bottomSheetContent: 2,
              bottomSheetSize: 'small',
              bottomSheetDismissable: true,
              bottomSheetResizable: false,
              bottomSheetBack: true,
              bottomSheetTitle: 'Title goes here!',
            });
            setIsSheetVisible(true);
          }}>
          Dismissable Small Sheet w/Back &amp; Title
        </Button>
        <Button
          variant="primary"
          onPress={() => {
            setBsState({
              ...bsState,
              bottomSheetSize: 'large',
              bottomSheetDismissable: true,
              bottomSheetResizable: false,
              bottomSheetTitle: 'BottomSheet With Carousel',
            });
            setIsBsCarouselSheetVisible(true);
          }}>
          With Carousel
        </Button>
        <Button
          variant="primary"
          onPress={() => {
            setBsState({
              ...bsState,
              bottomSheetSize: 'large',
              bottomSheetDismissable: true,
              bottomSheetResizable: false,
              bottomSheetTitle: 'BottomSheet With Icons Grid',
            });
            setIsBsIconsSheetVisible(true);
          }}>
          With Icons Grid
        </Button>
      </Section>
      {isSheetVisible ? (
        <BottomSheet
          onDismiss={closeModals}
          title={bsState.bottomSheetTitle}
          resizable={bsState.bottomSheetResizable}
          size={bsState.bottomSheetSize}
          dismissable={bsState.bottomSheetDismissable}
          onBackPress={bsState.bottomSheetBack ? closeModals : undefined}
          visible={isSheetVisible}
          onResize={handleOnResize}>
          {typeof bsState.bottomSheetContent === 'number' &&
          bsState.bottomSheetContent % 2 === 1 ? (
            <LongBottomSheetContent close={closeModals} />
          ) : (
            <ShortBottomSheetContent close={closeModals} />
          )}
        </BottomSheet>
      ) : null}
      {isBsCarouselSheetVisible ? (
        <BottomSheet
          onDismiss={closeModals}
          title={bsState.bottomSheetTitle}
          resizable={bsState.bottomSheetResizable}
          size={bsState.bottomSheetSize}
          dismissable={bsState.bottomSheetDismissable}
          onBackPress={bsState.bottomSheetBack ? closeModals : undefined}
          visible={isBsCarouselSheetVisible}
          onResize={handleOnResize}>
          <Carousel
            style={styles.carousel}
            header={carouselHeader}
            footer={carouselFooter}
            items={carouselItems}
            onItemPress={() => {}}
            onAddPress={() => {}}
          />
        </BottomSheet>
      ) : null}
      {isBsIconsSheetVisible ? (
        <BottomSheet
          showCloseHandle
          onDismiss={closeModals}
          title={bsState.bottomSheetTitle}
          resizable={bsState.bottomSheetResizable}
          size={bsState.bottomSheetSize}
          dismissable={bsState.bottomSheetDismissable}
          onBackPress={bsState.bottomSheetBack ? closeModals : undefined}
          visible={isBsIconsSheetVisible}
          onResize={handleOnResize}>
          <IconsOverview />
        </BottomSheet>
      ) : null}
    </>
  );
};

const styles = StyleSheet.create({
  carousel: {
    marginHorizontal: -16,
  },
});

export {BottomSheetsLegacy};
