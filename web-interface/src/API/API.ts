import axios from "axios";

import { 
    ApiResponse,
    DatabaseAuthData, 
    SqlTableScanResult
} from "./types";

import { API_URL } from "./constants";

axios.defaults.baseURL = API_URL;

export async function connectToDatabase(data: DatabaseAuthData): Promise<ApiResponse<void>> {
    const response = await axios.post('connect/', data);
    const status = response.status;

    if (status === 200) {
        return {status: 200}
    }
    
    return {status: status, errorMessage: response.data.message};
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

export async function updateScanResult(sqlTableScanResult: SqlTableScanResult): Promise<ApiResponse<void>> {
    const response = await axios.put('updateScanResult', sqlTableScanResult);
    const status = response.status;

    if (status === 200) {
        return {status: 200}
    }
    
    return {status: status, errorMessage: response.data.message};
}