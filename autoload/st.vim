function! st#VimOutCallback(chan, msg)
    echo a:msg
endfunction

" This function taken from the lh-vim repository
function! st#GetVisualSelection()
    try
        let a_save = @a
        normal! gv"ay
        return @a
    finally
        let @a = a_save
    endtry
endfunction

function! st#GetAvailablePythonCmd()
    for cmd in ['python', 'python2', 'python3']
        if executable(cmd)
            return cmd
        endif
    endfor

    return ""
endfunction
