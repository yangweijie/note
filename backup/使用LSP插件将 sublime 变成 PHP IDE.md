# 安装LSP
```npm install -g ocaml-language-server```

# st 安装 LSP
```pac install  package ``` 搜 LSP 就行
#  本地composer 安装 php的LSP

修改 ~/.composer/composer.json 设置
```
"minimum-stability": "dev",
"prefer-stable": true,
```
> ps win 在 C:/Users/jay/AppData/Roaming/Composer


run `composer global require felixfbecker/language-server`

run  `composer run-script --working-dir=/PATH-TO-HOME-DIR/.composer/vendor/felixfbecker/language-server parse-stubs`

修改 **LSP.sublime-settings - User**
```
{
  "clients": {
    "phpls": {
      "command": ["php", "/PATH-TO-HOME-DIR/.composer/vendor/felixfbecker/language-server/bin/php-language-server.php"],
      "scopes": ["source.php"],
      "syntaxes": ["Packages/PHP/PHP.sublime-syntax"],
      "languageId": "php"
    }
  }
}
```
Preferences.sublime-settings - User 里添加触发器
```
"auto_complete_triggers":
[
  {
    "characters": "$>:\\",
    "selector": "source.php"
  }
```