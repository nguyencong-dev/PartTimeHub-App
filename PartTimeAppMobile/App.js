import { View } from "react-native"
import { useFonts } from 'expo-font';
import Header from "./components/Header"
import Home from "./screens/Home/Home"
import { useState } from "react";
import Styles from "./styles/Styles";
import { NavigationContainer } from "@react-navigation/native";
import TabNavigator from "./components/TabNavigator";

const App = () =>{

  const [cateId, setCateId] = useState();

  return(
    <NavigationContainer>
      <TabNavigator />
    </NavigationContainer>

    // <View style={[Styles.container, Styles.padding]}>
    //   <Header cateId={cateId} setCateId={setCateId} />
    //   <Home cateId={cateId} />
    // </View>
  )
}
export default App