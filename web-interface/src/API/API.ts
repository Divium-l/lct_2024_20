import axios from "axios";

import { 
    DatabaseAuthData, 
    SqlTableScanResult 
} from "./types";

export async function connectToDatabase(data: DatabaseAuthData): Promise<number> {
    //const response = await axios.post('authDB', database);
    //return response.status;
    console.log(data);

    if (data.url == '' || data.port == '' || data.user == '' || data.password == '') {
        return 404;
    } else {
        return 200;
    }
}

export async function getScanResults(): Promise<SqlTableScanResult | undefined> {
    //const response = await axios.get('scanResult');

    // if (response.status === 200) {
    //     return response.data;
    // }
    // else {
    //     return undefined;
    // }

    return {
        tables: [{
            tableName: "Sample Table",
            columns: [
                {name: "id", mask: false},
                {name: "name", mask: true},
                {name: "phone", mask: true},
                {name: "fio", mask: false},
            ]
        }]
    }
}

export async function updateScanResult(sqlTableScanResult: SqlTableScanResult): Promise<number> {
    const response = await axios.put('updateScanResult', sqlTableScanResult);

    return response.status;
}