# simple translater

simple translater 是一个利用在线词典的 API 制作的vim插件，可以帮你在 vim 中翻译单词或语句

目前支持的词典引擎

* [有道翻译](http://dict.youdao.com/)
* [搜狗翻译](https://fanyi.sogou.com/)

## 安装

### pathogen 安装：

如果装有 pathogen 可以 :

    cd ~/.vim/bundle
    git clone git@github.com:FlyingFishBird/simple-translater.git

### vim-plug 安装：

vimrc 中添加如下配置

    Plug 'FlyingFishBird/simple-translator'

##  其他

### 添加快捷键映射到 vimrc 文件：

```vim
vnoremap <silent> <leader>q :<C-u>Stv<CR>
nnoremap <silent> <leader>q :<C-u>Stc<CR>
noremap <leader>Q :<C-u>Ste<CR>
```

在普通模式下，点击引导键再点q， 会翻译当前光标下的单词；

在 `visual` 模式下选中单词或语句，点击引导键再点q，会翻译选择的单词或语句；

点击引导键再点Q，可以在命令行输入要翻译的单词或语句；

译文将会在编辑器底部的命令栏显示。

### 配置查询引擎

默认使用 sogou 的查询引擎。如果需要换成有道。在 vimrc 添加如下配置：

    let g:simple_translator_engine = 'youdao'

### 配置搜狗翻译

搜狗翻译是收费翻译。需要你[自行申请](https://deepi.sogou.com/registered/texttranslate)
然后将 **pid 和 key** 两个字段保存为 json 文件存放在 ~/.sogoufanyi.json 中

### 开源项目参考

项目 fork 并修改自 [vim-youdao-translater](https://github.com/ianva/vim-youdao-translater) 非常感谢原作者的分享。
