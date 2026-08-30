import { Transform } from 'class-transformer'
import { IsInt, IsNotEmpty, IsNumber, IsPositive, IsString, Min, MinLength } from 'class-validator'

// DTO 相当于 Java 里的请求对象/表单对象。
// Express 里直接用 request.body，NestJS 则推荐把请求体约束成类。
export class CreateProductDto {
    @IsString()
    @IsNotEmpty()
    @MinLength(2)
    name!: string

    @IsString()
    @IsNotEmpty()
    image!: string

    @Transform(({ value }) => Number(value))
    @IsNumber()
    @IsPositive()
    price!: number

    @Transform(({ value }) => Number(value))
    @IsNumber()
    @Min(0)
    weight!: number

    @Transform(({ value }) => Number(value))
    @IsInt()
    @Min(0)
    quantity!: number

    @IsString()
    @IsNotEmpty()
    description!: string

    @Transform(({ value }) => Number(value))
    @IsInt()
    @IsPositive()
    categoryId!: number
}
