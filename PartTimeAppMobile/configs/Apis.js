import axios from "axios";

export const endpoints = {
    "jobs":"jobs/",
    "categories": "job-categories/"
}

export default axios.create({
    baseURL:"http://192.168.1.4:8000/"
})