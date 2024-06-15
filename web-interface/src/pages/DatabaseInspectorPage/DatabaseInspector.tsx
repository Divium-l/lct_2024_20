import { useEffect, useState } from "react";

import SqlTable from "../../widgets/Table/SqlTable";
import { SqlTableScanResult } from "../../API/types";
import { getScanResults } from "../../API/API";

export default function DatabaseInspectorPage() {
    const [sqlTables, setSqlTables] = useState<SqlTableScanResult>()
    
    useEffect(() => {
        getScanResults()
        .then(result => {setSqlTables(result)});
    }, 
    []);

    return (
        <>
            <div className="database-inspector-page-container">
                <div className="scan-results">
                    { sqlTables?.tables?.map(sqlTable => 
                        <SqlTable 
                            tableName={sqlTable.tableName}
                            columns={sqlTable.columns}
                        />
                    ) }
                </div>
            </div>
        </>
    )
}