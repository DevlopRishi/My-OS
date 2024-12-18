; boot.asm

bits 16

org 0x7c00        ; BIOS loads boot sector at 0x7c00

start:
    jmp short start2   ; jump to code

; Setup segment registers
start2:
    mov ax, 0x07e0    ; Data segment starts at 0x07e0
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0xFFFF   ; stack top

    ; load kernel (assume kernel at 10000:0)
    mov si, kernelStart
    mov di, 0x10000 ; Target address of kernel
    mov cx, kernelEnd-kernelStart ;kernel size
    mov bx, 0x0020 ;kernel sector size
    loadLoop:
        mov ah, 0x02
        mov al, 0x01
        mov dl, 0x80
        mov dh, 0x00
        int 0x13
        jc error    ;if carry set then error
        inc si      ;next sector
        add di, 0x200 ;next address
        loop loadLoop ;loop until all the sectors read

    jmp 0x1000:0000 ; jump to kernel address

error:
    mov si, msg
    call printStr
    hlt ;if anything goes wrong

;print string function
printStr:
    mov ah, 0x0e
printLoop:
    mov al, [si]
    cmp al, 0
    je printEnd
    int 0x10
    inc si
    jmp printLoop
printEnd:
    ret

msg db "Error loading kernel!", 0
times 510 - ($ - $$) db 0  ; pad with 0
dw 0xaa55 ; Boot signature