import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import Home from "../screens/Home/Home";
import { Icon } from "react-native-paper";
import Login from "../screens/User/Login";
import Register from "../screens/User/Register";
import JobDetail from "../screens/Home/JobDetail";

const Stack = createNativeStackNavigator();
const StackNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{headerShown: false}}>
      <Stack.Screen name="index" component={Home} />
      <Stack.Screen name="job_detail" component={JobDetail} />
    </Stack.Navigator>
  );
}

const Tab = createBottomTabNavigator();

const TabNavigator = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="home" component={StackNavigator} options={{title: 'Khám phá', tabBarIcon: () => <Icon source="home" size={30} />}} />
      <Tab.Screen name="login" component={Login} options={{title: 'Đăng nhập', tabBarIcon: () => <Icon source="account" size={30} />}} />
      <Tab.Screen name="register" component={Register} options={{title: 'Đăng ký', tabBarIcon: () => <Icon source="account-plus" size={30} />}} />
    </Tab.Navigator>
  );
}

export default TabNavigator