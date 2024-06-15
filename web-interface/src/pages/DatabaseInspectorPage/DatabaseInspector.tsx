import { useEffect, useState } from "react";

import SqlTable from "../../widgets/Table/SqlTable";
import { SqlTableScanResult } from "../../API/types";
import { getScanResults, startMasking } from "../../API/API";

export default function DatabaseInspectorPage() {
    const [sqlTables, setSqlTables] = useState<SqlTableScanResult | undefined>()

    const onButtonClick = async () => {
        const response = await startMasking();
        if (response.status === 200) {
            alert('Ok');
        }
        else {
            alert('Error');
        }
    }
    
    useEffect(() => {
        getScanResults()
        .then(result => {setSqlTables(result)});
    }, 
    []);

    return (
        <>
            <div className="database-inspector-page-container">
                <div className="page-header">
                    <h1>Результат сканирования</h1>
                    <p>Найдено {sqlTables?.tables.length || 0} таблиц</p>
                </div>
                <div className="scan-results">
                    { sqlTables?.tables?.map(sqlTable => 
                        <SqlTable 
                            tableName={sqlTable.tableName}
                            columns={sqlTable.columns}
                        />
                    ) }
                </div>
                { sqlTables?.tables.length !== undefined && sqlTables?.tables.length > 0 ? (
                    <button onClick={onButtonClick}>Начать маскирование</button>
                ) : undefined }
            </div>
        </>
    )
}