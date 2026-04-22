import { StyleSheet } from "react-native";

export default StyleSheet.create({
  container: {
    flex:1,
    backgroundColor: "#f5f6fa",
    margin: 10,
  },
  jobCard: {
    marginHorizontal: 12,
    marginTop: 12,
    backgroundColor: "#fff",
    marginBottom: 6,
  },
  jobTitle: {
    fontWeight: "bold",
    fontSize: 16,
  },
  subtitleContainer: {
    marginTop: 6,
  },
  infoRow: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 4,
  },
  salaryRow: {
    flexDirection: "row",
    alignItems: "center",
  },
  infoText: {
    marginLeft: 6,
    fontSize: 13,
    color: "#666",
  },
  salaryText: {
    marginLeft: 6,
    fontSize: 14,
    color: "#27ae60",
    fontWeight: "bold",
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 8,
    backgroundColor: "#f0f0f0",
  },
  loading: {
    marginVertical: 20,
  },
  finderContainer: {
    backgroundColor: "#9DB2F3",
    paddingTop: 20,
    paddingBottom: 14,
    paddingHorizontal: 16,
    flexDirection: "row",
    alignItems: "center",
  },
  searchbar: {
    flex: 1,
    height: 46,
    borderRadius: 25,
    backgroundColor: "#F5F5F5",
    elevation: 0,
    marginRight: 10,
  },
  bellButton: {
    width: 40,
    height: 40,
  },
  requirementTitle: {
    fontWeight: "bold",
    marginBottom: 15,
  },
  requirement: {
    lineHeight: 24,
    color: "#424242",
    marginLeft: 30,
  },
  companyTitle: {
    fontWeight: "bold",
    marginLeft: 20,
  },
  descriptionText: {
    lineHeight: 24,
    color: "#424242",
  },
  surface: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    padding: 16,
    backgroundColor: "white",
    elevation: 10,
  },
});
