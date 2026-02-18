### Badge

```js
import {Badge} from '@walmart/gtp-shared-components';
const Spacer = () => <View style={{height: 8}} />;

<>
<View style={{justifyContent:"space-around", flexDirection:"row"}}>
  <Badge color="blue"/>
  <Badge color="gray"/>
  <Badge color="green"/>
  <Badge color="purple"/>
  <Badge color="red"/>
  <Badge color="spark"/>
  <Badge color="white"/>
  </View><Spacer/>
  <View style={{justifyContent:"space-around", flexDirection:"row"}}>
  <Badge color="blue">1</Badge>
  <Badge color="gray">2</Badge>
  <Badge color="green">3</Badge>
  <Badge color="purple">4</Badge>
  <Badge color="red">5</Badge>
  <Badge color="spark">6</Badge>
  <Badge color="white">7</Badge>
  </View>
  <Spacer/>
  <View style={{justifyContent:"space-around", flexDirection:"row"}}>
  <Badge color="blue">10</Badge>
  <Badge color="gray">20</Badge>
  <Badge color="green">30</Badge>
  <Badge color="purple">40</Badge>
  <Badge color="red">50</Badge>
  <Badge color="spark">60</Badge>
  <Badge color="white">70</Badge>
  </View>
</>;
```
