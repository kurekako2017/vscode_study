import { Transform } from 'class-transformer'
import { IsInt, IsNumber, IsOptional, IsPositive, IsString, Min, MinLength } from 'class-validator'

// Update DTO 保持和 Create DTO 相似，但字段全部可选。
// 这样 PUT /products/:id 可以只提交需要修改的字段，和 Express 中部分更新的语义接近。
export class UpdateProductDto {
    @IsOptional()
    @IsString()
    @MinLength(2)
    name?: string

    @IsOptional()
    @IsString()
    image?: string

    @IsOptional()
    @Transform(({ value }) => Number(value))
    @IsNumber()
    @IsPositive()
    price?: number

    @IsOptional()
    @Transform(({ value }) => Number(value))
    @IsNumber()
    @Min(0)
    weight?: number

    @IsOptional()
    @Transform(({ value }) => Number(value))
    @IsInt()
    @Min(0)
    quantity?: number

    @IsOptional()
    @IsString()
    description?: string

    @IsOptional()
    @Transform(({ value }) => Number(value))
    @IsInt()
    @IsPositive()
    categoryId?: number
}
