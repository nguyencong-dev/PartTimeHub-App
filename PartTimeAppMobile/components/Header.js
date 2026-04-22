import { Text, TouchableOpacity, View } from "react-native";
import Styles from "../styles/Styles";
import { useEffect, useState } from "react";
import Apis, { endpoints } from "../configs/Apis";
import { Chip } from "react-native-paper";

const Header = ({cateId, setCateId}) => {
    const [categories, setCategories] = useState([]);

    const loadCategories = async () => {
        let res = await Apis.get(endpoints['categories']);
        setCategories(res.data);
    }

    useEffect(() => {
        loadCategories();
    }, []);

    return (
        <View style={[Styles.row, Styles.wrap]}>
            <TouchableOpacity onPress={() => setCateId(null)}>
                <Chip mode={!cateId ? "outlined":"flat"} style={Styles.margin} icon="label" >Tất cả</Chip>
            </TouchableOpacity>

            {categories.map(c => <TouchableOpacity key={c.id} onPress={() => setCateId(c.id)}>
                <Chip mode={c.id == cateId ? "outlined":"flat"} style={Styles.margin} icon="label" >{c.name}</Chip>
            </TouchableOpacity>)}
        </View>
    );
}

export default Header;