if !exists("g:simple_translator_engine")
    let g:simple_translator_engine = "sogou"
endif

let s:translator_file = expand('<sfile>:p:h') . "/../run.py"
let s:translator = {'stdout_buffered': v:true, 'stderr_buffered': v:true}

function! s:translator.on_stdout(jobid, data, event)
    if !empty(a:data) | echo join(a:data) | endif
endfunction
let s:translator.on_stderr = function(s:translator.on_stdout)

function! s:translator.start(lines)
    let python_cmd = st#GetAvailablePythonCmd()
    if empty(python_cmd)
        echoerr "[SimpleTranslator] [Error]: Python package neeeds to be installed!"
        return -1
    endif

    let cmd = printf("%s %s %s %s", python_cmd, s:translator_file, g:simple_translator_engine, a:lines)
    if exists('*jobstart')
        return jobstart(cmd, self)
    elseif exists('*job_start') && ! has("gui_macvim")
        return job_start(cmd, {'out_cb': "st#VimOutCallback"})
    else
        echo system(cmd)
    endif
endfunction

function! s:SimpleVisualTranslate()
    call s:translator.start(st#GetVisualSelection())
endfunction

function! s:SimpleCursorTranslate()
    call s:translator.start(expand("<cword>"))
endfunction

function! s:SimpleEnterTranslate()
    let word = input("Please enter the word: ")
    redraw!
    call s:translator.start(word)
endfunction

command! Stv call <SID>SimpleVisualTranslate()
command! Stc call <SID>SimpleCursorTranslate()
command! Ste call <SID>SimpleEnterTranslate()
