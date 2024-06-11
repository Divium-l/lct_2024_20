export type DatabaseAuthData = {
    databaseType: "postgresql";
    url: string;
    port: string;
    user: string;
    password: string;
    copy: boolean;
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