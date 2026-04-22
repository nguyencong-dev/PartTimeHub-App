import { Image, ScrollView, Text, View } from "react-native";
import Styles from "../../styles/Styles";
import HomeStyles from "../Home/Styles";
import { use, useEffect, useState } from "react";
import Apis, { endpoints } from "../../configs/Apis";
import {
  ActivityIndicator,
  Appbar,
  Button,
  Card,
  Divider,
  List,
  Surface,
} from "react-native-paper";
import { useNavigation } from "@react-navigation/native";

const JobDetail = ({ route }) => {
  const jobId = route.params?.jobId;
  const [loading, setLoading] = useState(false);
  const [job, setJob] = useState(null);
  const nav = useNavigation();
  const loadDetailJob = async () => {
    try {
      setLoading(true);
      let url = `${endpoints["jobs"]}${jobId}/`;
      console.log(url);
      let res = await Apis.get(url);

      setJob(res.data);
      console.log("Chi tiết công việc:", res.data);
    } catch (ex) {
      console.error("Lỗi khi tải công việc:", ex);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDetailJob();
  }, [jobId]);

  if (loading || !job) {
    return (
      <View>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <View style={HomeStyles.container}>
      <ScrollView contentContainerStyle={{ paddingBottom: 100 }}>
        <Appbar>
          <Appbar.BackAction onPress={() => nav.goBack()} />
          <Appbar.Content title="Chi tiết công việc" />
        </Appbar>
        <Card.Title
          titleStyle={HomeStyles.companyTitle}
          title={job.company.name}
          left={() => (
            <Image style={Styles.avatar} source={{ uri: job.company.avatar }} />
          )}
        />
        <Text style={Styles.bigTitle}>{job.title}</Text>
        <List.Item
          titleStyle={HomeStyles.infoText}
          title={job.location}
          left={(props) => <List.Icon {...props} icon="map-marker-circle" />}
        />
        <List.Item
          titleStyle={HomeStyles.infoText}
          title={job.working_time}
          left={(props) => (
            <List.Icon {...props} icon="clock-time-ten-outline" />
          )}
        />
        <List.Item
          titleStyle={HomeStyles.salaryText}
          title={`${Number(job.salary).toLocaleString("vi-VN")} VND`}
          left={(props) => <List.Icon {...props} icon="cash" />}
        />
        <Divider style={Styles.divider} />

        <View style={HomeStyles.container}>
          <Text variant="titleMedium" style={HomeStyles.requirementTitle}>
            Mô tả công việc:
          </Text>
          <Text variant="bodyMedium" style={HomeStyles.descriptionText}>
            {job.description}
          </Text>
        </View>

        <View style={HomeStyles.container}>
          <Text variant="titleMedium" style={HomeStyles.requirementTitle}>
            Yêu cầu công việc:
          </Text>
          {job.requirements.map((item) => (
            <Text style={HomeStyles.requirement} key={item.id}>
              • {item.subject}
            </Text>
          ))}
        </View>

        <View style={HomeStyles.container}>
          <Text variant="titleMedium" style={HomeStyles.requirementTitle}>
            Quyền lợi:
          </Text>
          {job.benefits.map((item) => (
            <Text style={HomeStyles.requirement} key={item.id}>
              • {item.subject}
            </Text>
          ))}
        </View>
      </ScrollView>

      <Surface style={HomeStyles.surface}>
        <Button
          mode="contained"
          buttonColor="#6200ee"
          contentStyle={{ height: 50 }}
          onPress={() => alert("Gửi CV cho công việc: " + job.id)}
        >
          Ứng tuyển ngay
        </Button>
      </Surface>
    </View>
  );
};

export default JobDetail;
