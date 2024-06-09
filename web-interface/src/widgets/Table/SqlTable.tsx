import { ChangeEvent } from "react";

import { SqlColumn } from "../../API/types";
import { updateScanResult } from "../../API/API";

export interface SqlTableProps {
    tableName: string;
    columns: SqlColumn[];
}

interface SqlTableRowProps {
    tableName: string;
    column: SqlColumn;
}

export default function SqlTable( {tableName, columns}: SqlTableProps ) {
    return (
        <div>
            <h3>{tableName}</h3>
            <table>
                <SqlTableHeader />
                <tbody>
                    { columns.map(column => (
                        <SqlTableRow
                            tableName={tableName}
                            column={column}
                        />
                    )) }
                </tbody>
            </table>
        </div>
    )
}

function SqlTableHeader() {
    return (
        <thead>
            <tr>
                <th>Название столбца</th>
                <th>Чувствительные данные</th>
            </tr>
        </thead>
    )
}

function SqlTableRow({tableName, column}: SqlTableRowProps) {
    const handleCheckboxChange = async (event: ChangeEvent<HTMLInputElement>) => {
        const checked = event.target.checked;
        
        const status = await updateScanResult({
            tables: [{tableName: tableName, columns: [{name: column.name, mask: checked}]}]
        });

        if (status !== 200) {
            event.target.checked = !checked; 
        } 
    }

    return (
        <tr key={column.name}>
            <td>{column.name}</td>
            <td>
                <input type="checkbox" defaultChecked={column.mask} onChange={handleCheckboxChange}/>
            </td>
        </tr>
    )
}