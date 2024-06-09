import { ReactElement, useState } from "react";

import { IconProps } from "../../shared/Icon";

import "./DatabaseSelcetButoon.scss";

export interface DatabaseSelcetButtonProps {
    icon: ReactElement<IconProps>;
    text: string;
    onClickCallback: () => void;
}

export default function DatabaseSelcetButton({icon, text, onClickCallback}: DatabaseSelcetButtonProps) {
    const [selected, setSelected] = useState(false);

    const onClick = () => {
        setSelected(!selected);
        onClickCallback();
    }
    
    return (
        <div 
            className={`database-select-button-container ${selected ? 'selected' : ''}`}
            onClick={onClick}
        >
            <div className='icon-container'>{icon}</div>
            <div className='text-container'>
                <h3>{text}</h3>
            </div>
      </div>
    )
}