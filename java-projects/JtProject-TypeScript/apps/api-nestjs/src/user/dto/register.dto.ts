import { IsEmail, IsNotEmpty, IsString, MinLength } from 'class-validator'

// RegisterDto 与 Express 的 RegisterBody 保持一致，属于同一个前后端合同。
export class RegisterDto {
    @IsString()
    @IsNotEmpty()
    @MinLength(2)
    username!: string

    @IsEmail()
    @IsNotEmpty()
    email!: string

    @IsString()
    @IsNotEmpty()
    @MinLength(4)
    password!: string

    @IsString()
    @IsNotEmpty()
    address!: string
}
