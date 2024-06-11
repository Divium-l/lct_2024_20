import axios from "axios";

import { 
    DatabaseAuthData, 
    SqlTableScanResult 
} from "./types";

import { API_URL } from "./constants";

axios.defaults.baseURL = API_URL;

export async function connectToDatabase(data: DatabaseAuthData): Promise<number> {
    console.log(axios.defaults.baseURL)
    const response = await axios.post('connect/', data);
    return response.status;
}

export async function getScanResults(): Promise<SqlTableScanResult | undefined> {
    const response = await axios.get('scanResult');

    if (response.status === 200) {
        return response.data;
    }
    else {
        return undefined;
    }
}

export async function updateScanResult(sqlTableScanResult: SqlTableScanResult): Promise<number> {
    const response = await axios.put('updateScanResult', sqlTableScanResult);

    return response.status;
}