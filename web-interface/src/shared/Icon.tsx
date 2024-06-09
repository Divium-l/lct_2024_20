import { ImgHTMLAttributes } from "react";

export interface IconProps extends ImgHTMLAttributes<HTMLImageElement> {
    src: string,
    alt: string,
}

export default function Icon(props: IconProps) {
    const {src, alt} = props;

    return (
        <img 
            height={props.height || "45px"}
            width ={props.width  || "auto"}
            src={src}
            alt={alt}
        ></img>
    )
}