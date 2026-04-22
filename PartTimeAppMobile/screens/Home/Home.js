import React, { useEffect, useState } from "react";
import {
  View,
  Text,
  ActivityIndicator,
  Image,
  TouchableOpacity,
  FlatList,
} from "react-native";
import { Button, Card, IconButton, Searchbar } from "react-native-paper";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import Apis, { endpoints } from "../../configs/Apis";
import HomeStyles from "../Home/Styles";
import { useNavigation } from "@react-navigation/native";

const Home = ({ cateId }) => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [q, setQ] = useState("");
  const navigate = useNavigation();

  const loadJobs = async () => {
    try {
      setLoading(true);
      let url = `${endpoints["jobs"]}?page=${page}`;
      if (q) {
        url = `${url}&q=${q}`;
      }
      if (cateId) {
        url = `${url}&category_id=${cateId}`;
      }

      let res = await Apis.get(url);

      if (res.data.next === null) setPage(0);

      if (page === 1) setJobs(res.data.results);
      else if (page > 1)
        setJobs((prev) => [...prev, ...res.data.results]);
    } catch (ex) {
      console.error("Lỗi khi tải công việc:", ex);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let timer = setTimeout(() => {
      if (page > 0) loadJobs();
    }, 500);
    return () => clearTimeout(timer);
  }, [page, q, cateId]);

  useEffect(() => {
    setJobs([]);
    setPage(1);
  }, [q, cateId]);

  const formatSalary = (salary) => {
    return Number(salary).toLocaleString("vi-VN");
  };

  const loadMore = () => {
    if (loading || page <= 0 || jobs.length === 0) return;
    setPage((prev) => prev + 1);
  };

  return (
    <View style={{ flex: 1 }}>
      <View>
        <View style={HomeStyles.finderContainer}>
          <Searchbar
            value={q}
            onChangeText={setQ}
            style={HomeStyles.searchbar}
            placeholder="Tìm công việc tại đây..."
          />
          <Button style={HomeStyles.bellButton} icon="bell" />
        </View>
      </View>

      <FlatList
        data={jobs}
        keyExtractor={(item) => item.id.toString()}
        onEndReached={loadMore}
        renderItem={({ item: job }) => (
          <Card
            style={HomeStyles.jobCard}
            onPress={() => navigate.navigate("job_detail", { jobId: job.id })}
          >
            <Card.Title
              title={job.title}
              titleStyle={HomeStyles.jobTitle}
              subtitle={
                <View style={HomeStyles.subtitleContainer}>
                  <View style={HomeStyles.infoRow}>
                    <MaterialCommunityIcons
                      name="domain"
                      size={14}
                      color="#666"
                    />
                    <Text style={HomeStyles.infoText}>{job.company.name}</Text>
                  </View>

                  <View style={HomeStyles.infoRow}>
                    <MaterialCommunityIcons
                      name="map-marker-circle"
                      size={14}
                      color="#666"
                    />
                    <Text style={HomeStyles.infoText}>{job.location}</Text>
                  </View>

                  <View style={HomeStyles.infoRow}>
                    <MaterialCommunityIcons
                      name="clock-time-ten-outline"
                      size={14}
                      color="#666"
                    />
                    <Text style={HomeStyles.infoText}>{job.working_time}</Text>
                  </View>

                  <View style={HomeStyles.salaryRow}>
                    <MaterialCommunityIcons
                      name="cash"
                      size={14}
                      color="#27ae60"
                    />
                    <Text style={HomeStyles.salaryText}>
                      {formatSalary(job.salary)} VND
                    </Text>
                  </View>
                </View>
              }
              left={() => (
                <Image
                  source={{ uri: job.company.avatar }}
                  style={HomeStyles.avatar}
                />
              )}
              right={(props) => (
                <IconButton
                  {...props}
                  icon="cards-heart-outline"
                  onPress={() => {}}
                />
              )}
            />
          </Card>
        )}
        ListFooterComponent={
          loading ? (
            <ActivityIndicator style={HomeStyles.loading} size="large" />
          ) : null
        }
      />
    </View>
  );
};

export default Home;