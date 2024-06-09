export type DatabaseAuthData = {
    database: "postgresql";
    url: string;
    port: string;
    user: string;
    password: string;
    copyDatabase: boolean;
}

export interface SqlColumn {
    name: string;
    mask: boolean;
}

export interface SqlTable {
    tableName: string;
    columns: SqlColumn[];
}

export interface SqlTableScanResult {
    tables: SqlTable[];
}