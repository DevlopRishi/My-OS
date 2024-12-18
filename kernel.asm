; kernel.asm
bits 16
org 0x0

kernelStart:

    jmp short start_kernel

;Function to print a string
printStr:
    pusha
    mov ah, 0x0e
    printLoop:
        mov al, [si]
        cmp al, 0
        je printEnd
        int 0x10
        inc si
        jmp printLoop
    printEnd:
    popa
    ret

;Function to clear the screen
clearScreen:
    pusha
    mov ah, 0x00
    mov al, 0x03
    int 0x10
    mov ah, 0x02
    mov dh, 0x00
    mov dl, 0x00
    mov bh, 0x00
    int 0x10
    popa
    ret

;Function to read a char
readChar:
    pusha
    mov ah, 0x00
    int 0x16
    movzx bx, al
    popa
    mov al, bl
    ret

start_kernel:
    call clearScreen
promptLoop:
    mov si, promptStr
    call printStr

inputLoop:
    call readChar
    mov [inputBuffer], al
    mov si, inputBuffer
    call printStr
    cmp al, 0x0D
    jne inputLoop
    mov si, newLine
    call printStr
    jmp promptLoop

;data section
promptStr db "os> ", 0
newLine db 0xA,0xD, 0
inputBuffer db 0
kernelEnd: