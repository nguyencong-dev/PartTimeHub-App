import { StyleSheet } from "react-native";

export default StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 50,
  },
  row: {
    flexDirection: "row",
  },
  wrap: {
    flexWrap: "wrap",
  },
  padding: {
    padding: 5,
  },
  margin: {
    margin: 5,
  },
  subject: {
    fontSize: 30,
    fontWeight: "bold",
    color: "blue",
  },
  avatar: {
    width: 60,
    height: 60,
    borderRadius: 50,
  },
  title: {
    fontWeight: "bold", 
    marginBottom: 12
  },
  bigTitle: {
    fontSize: 22,
    alignItems: "center",
    textAlign: "center",
  },
  divider:{
    height: 8, 
    backgroundColor: "#F5F5F5"
  }
});
