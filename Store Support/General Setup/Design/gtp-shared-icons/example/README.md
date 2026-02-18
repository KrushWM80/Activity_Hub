# Example app

The current `example/` folder contains a standalone showcase app.

Before you run the app for the first time, please refer to [README.setup.md](../README.setup.md) for instructions on how to set up your local development environment.

## Run the example app

### Android

- Ensure [Android Studio 3+][1] is installed and an [emulator is set up][2]
- Alternatively, you can run the app on a USB tethered device

  - connect the device via USB
  - run `adb devices` to make sure the device is mounted and visible to adb

    ```sh
    adb devices
    List of devices attached
    R58M404T6DM     device
    ```

  - you can project the device screen on the laptop via `scrcpy`

    ```sh
    brew install scrcpy
    scrcpy -t &
    ```

  - make sure you have accepted all licenses:

    ```sh
    $ANDROID_SDK/tools/bin/sdkmanager --licenses
    ```

    where $ANDROID_SDK is a variable that points to your SDK installation e.g. `/Users/a0b0ccc/Library/Android/sdk`

  - Install dependencies

    ```sh
    yarn
    cd example
    yarn
    cd ..
    ```

  - `yarn android` - OR - open the [android](./android) folder in Android Studio (`studio android/`)

![README_android](https://gecgithub01.walmart.com/storage/user/67415/files/d1ade887-097a-4fc7-83da-d232d87317bb)

### iOS

- Ensure [Xcode 12+][3] is installed
- Install dependencies

  ```sh
  yarn
  cd example
  yarn
  pod install
  cd ..
  ```

- `yarn ios` - OR - open the [ios](./ios) folder in Xcode (`xed ios/`)

![README_ios](https://gecgithub01.walmart.com/storage/user/67415/files/4750494b-4e8b-429e-8d11-45a04c01e732)

[1]: https://developer.android.com/studio/index.html#downloads
[2]: https://developer.android.com/studio/run/emulator.html
[3]: https://developer.apple.com/xcode/
