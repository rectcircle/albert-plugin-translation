## albert python插件

### 安装

1. 安装albert最新版
参考 https://albertlauncher.github.io/docs/installing/

2. 执行以下命令
```bash
git clone https://github.com/rectcircle/albert-plugins.git
mv albert-plugins/* ~/.local/share/albert/org.albert.extension.python/modules/
```


### 介绍

#### 中英翻译

* 触发字符串 `tr `
* 支持google翻译、百度翻译
* 自动检测输入文本语言

例子
```
tr hello world!
tr 你好 世界
```