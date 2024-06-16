import { useEffect, useRef, useState } from "react";

import SqlTable from "../../widgets/Table/SqlTable";
import { SqlTableScanResult } from "../../API/types";
import { getScanResults, startMasking } from "../../API/API";

export default function DatabaseInspectorPage() {
    const [sqlTables, setSqlTables] = useState<SqlTableScanResult | undefined>();
    const intervalRef = useRef<number>(0);

    const onButtonClick = async () => {
        const response = await startMasking();
        if (response.status === 200) {
            alert('Ok');
        }
        else {
            alert('Error');
        }
    }

    if (sqlTables !== undefined && sqlTables?.tables.length > 0) {
        clearInterval(intervalRef.current);
        intervalRef.current = -1;
    }

    if (intervalRef.current !== -1) {
        intervalRef.current = setInterval(() => {
            getScanResults().then(result => {setSqlTables(result)});
        }, 5000);
    }

    return (
        <>
            <div className="database-inspector-page-container">
                <div className="page-header">
                    <h1>Результат сканирования</h1>
                    {
                        sqlTables?.tables.length !== undefined && sqlTables.tables.length > 0 ?
                        <p>Найдено {sqlTables?.tables.length} таблиц</p> :
                        <p>Загрузка...</p>
                    }
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