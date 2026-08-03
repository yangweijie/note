## 术语定义

### 文档对象

“文档对象”是指PDF文档中的文档对象，共有三种类型的“文档对象”，他们分别是“页面对象”，“封面对象”和“目录对象”。

### 页面对象

“页面对象”是指以页面的形式在PDF文档中呈现的对象，这个是相对于“封面对象”和“目录对象”来讲的。此类对象会成为PDF文档中内容。

### 封面对象

“封面对象”是指以封面的形式在PDF文档中呈现的对象。这类对象会成为PDF文档中的封面。

### 目录对象

“目录对象”是以目录的形式在PDF文档中呈现的对象，又叫“TOC对象”。这类对象会成为PDF文档中的目录。

### 大纲

“大纲”是指阅读PDF文档时的书签导航。

### 外链

“外链”是指所有在这个页面中且不指向它自身页面中锚点的超链接。

### 内链

“内链”是指在这个页面中且指向的目标页面是这个页面本身中的一个锚点的超链接。

## 命令格式

~~~ shell
wkhtmltopdf [GLOBAL OPTION]... [OBJECT]... <output file>
~~~

上述代码就是 wkhtmltopdf 的命令行格式，看似简单，其实在 `[GLOBAL OPTION]` 和 `[OBJECT]` 中还别有洞天。预知详情，且听我慢慢道来。

## 文档对象简介

wkhtmltopdf 能够把多个“对象”合并生成一个pdf文档，这些“对象”可以是“页面对象”、“封面对象”、或是“目录对象”。这些对象在pdf文档中的顺序可以通过命令行参数来指定。命令行参数包括两部分，一种是针对某一特定“对象”的命令行参数，另一种是全局的命令行参数。并且全局的命令行参数只能放在全局参数区([GLOBAL OPTION])中指定。

### 页面对象简介

“页面对象”作用是用来把一个网页作为内容输出到PDF文档中。

~~~
(page)? <input url/file name> [PAGE OPTION]...

~~~

“页面对象”的参数可以放在“全局参数域([GLOBAL OPTIONS])”和“页面参数域([PAGE OPTIONS])”。程序会根据实际情况在所有参数中找到合适的参数应用到页面、页眉和页脚。

### 封面对象简介

“封面对象”用来把一个网页作为封面输出到PDF文档中，输出的页面不会在TOC中出现，并且不会包含页眉和页脚。

~~~ shell
cover <input url/file name> [PAGE OPTION]...
~~~

所有能够在“页面对象”中使用的参数都可以用到“封面对象”

### 目录对象简介

“目录对象”的作用是输出一个目录到PDF文件中。

~~~ shell
toc [TOC OPTION]...
~~~

所有能够在“页面对象”中使用的参数都可以用到“TOC对象”，并且还有许多的针对“TOC对象”的参数可以应用到“TOC对象”中。目录是通过 XSLT 生成的，这就意味着它可以被定义成任何你想看到的样子。你可以通过命令行参数 `--dump-default-toc-xsl` 输出默认的 XSLT 文档，通过 `--dump-outline` 命令行参数 可指定以XML格式输出当前处理文档的目录到指定文件。更多详细内容请查看后面介绍的 目录对象参数

## 命令参数

命令参数包含五部分，分别是“全局参数”，“大纲参数选项”，“页面对象参数”，“页眉和页脚参数选项”和“目录对象参数”。

### 全局参数

~~~ shell
    --collate             当输出多个副本时进行校验(这是默认设置)
    --no-collate          当输出多个副本时不进行校验
    --cookie-jar <path>   从提供的JAR文件中读写cookie数据
    --copies <number>     设置输出副本的数量(默认主1)，其实为1就够了
-d, --dpi <dpi>           指定一个要分辨率(这在 X11 系统中并没有什么卵用)
-H, --extended-help       相对 -h 参数，显示更详细的说明文档
-g, --grayscale           指定以灰度图生成PDF文档。占用的空间更小
-h, --help                显示帮助信息  
    --htmldoc             输出程序的html帮助文档
    --image-dpi <integer> 当页面中有内嵌的图片时，
                          会下载此命令行参数指定尺寸的图片(默认值是 600)
    --image-quality <interger> 当使用 jpeg 算法压缩图片时使用这个参数指定的质量(默认为 94)
    --license             输出授权信息并退出
-l, --lowquality          生成低质量的 PDF/PS ,能够很好的节约最终生成文档所占存储空间
    --manpage             输出程序的手册页
-B, --margin-bottom <unitreal> 设置页面的 底边距
-L, --margin-left <unitreal>   设置页面的 左边距 (默认是 10mm)
-R, --margin-right <unitreal>  设置页面的 右边距 (默认是 10mm)
-T, --margin-top <unitreal>    设置页面的 上边距
-O, --orientation <orientation> 设置为“风景(Landscape)”或“肖像(Portrait)”模式,
                                默认是肖像模块(Portrait)
    --page-height <unitreal>   页面高度
-s, --page-size <Size>         设置页面的尺寸，如：A4,Letter等，默认是：A4
    --page-width <unitreal>    页面宽度
    --no-pdf-compression       不对PDF对象使用丢失少量信息的压缩算法，不建议使用些参数，
                               因为生成的PDF文件会非常大。
-q, --quiet                    静态模式，不在标准输出中打印任何信息
    --read-args-from-stdin     从标准输入中读取命令行参数，后续会有针对此指令的详细介绍，
                               请参见 **从标准输入获取参数**
    --readme                   输出程序的 readme 文档
    --title <text>             生成的PDF文档的标题，如果不指定则使用第一个文档的标题
-V, --version                  输出版本信息后退出
~~~

上述代码区是所有全局参数及注释，下面简单说一下个别参数的意义及用法。

#### --copies N

N 是一个正整数。

这个选项可以先不用关心了，因为你这辈子可能都用不到。他的作用是在生成的PDF文档中，把内容重复输出 N 份。也就是说，你将得到一个PDF文档，这个文档中的大小、内容量都将是不使用此参数时的 N 倍。然而重复的内容对你来说并没有什么卵用。

如果不使用 `--copies` 参数，那么 `--collate` 和 `--no-collate` 参数就不用了解了，因为他们只在 `--copies` 参数中的 N 大于 1 时才有意义。

#### -g, --grayscale

这个参数非常有用，使用这个参数可以有效压缩生成的PDF所占用的存储空间。当然这个压缩是要付出一定代价的，那就是最终生成的PDF文档将是灰度的，没有任何色彩。如果你能接受灰度PDF文档，并不影响实际使用，那就请使用这个参数吧。生成的PDF文档越大，使用此参数获得的惊喜就越大。

#### -l, --lowquality

这个参数与 `-g` 参数有异曲同工之妙， `-l` 参数也会大大压缩PDF文档所占用的存储空间。只是它是通过降低PDF文档的质量来完成这一任务的。这个参数也值得推荐，你最好先尝试一下，看看使用此参数后生成的PDF文档与不使用此参数的区别再做决定。我可以告诉你的是，在纯文字的情况下他们的差别不大，此参数只是降低了PDF文档的质量，看上去是糙了一些，但不会影响阅读。如果你是一个追求感官享受，或是你生成的PDF文档中有大量图片，那就不要使用此参数了。

#### --no-pdf-compression

这个参数强烈建议不要使用，最好这辈子都不要去了解他的好，因为对于你来说肯定用不到。它的作用就是在输出PDF文档时，不使用任何的压缩。这将会导致输出的PDF文档特别的大，质量是无损的，但是对于人类来说从感观上根本察觉不到压缩前后的质量变化的。如果你的感观超乎于常人，压缩之后的体验对你来说无法接受，那我收回前面的话，你就尽情使用此参数吧。

#### -q, --quiet

使用这个参数后，你将得到一个干净的命令行输出，就连程序处理的进度和状态都没有。这个参数会抑制所有命令行输出，在程序的工作过程中，你看不到任何输出。建议不会使用此参数，因为程序输出一些进度和状态信息还是非常有用的。万一程序工作到某处死了呢(嘿嘿)，在 `-q` 模式下你是无法分辨是否程序死掉了的。

### 大纲参数选项

~~~ shell
--dump-default-toc-xsl     输出默认的 TOC xsl 样式表到标准输出
--dump-outline <file>      输出“大纲”到指定的文件(文件内容为xml)
--outline                  在生成的PDF文档中输出“大纲”(这是默认设置)
--no-outline               不在pdf文档中输出大纲
--outline-depth <level>    设置生成大纲的深度(默认为 4)
~~~

大纲参数中唯一需要特别说一下的是 `--outline-depth` ，其他参数默认就好了。

#### 何为大纲

![](http://upload-images.jianshu.io/upload_images/3060014-05914583ee52091d.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

大纲

如上图所示，其实我更喜欢称之为目录或导航。大纲是根据你HTML中的标题(Hn标签)自动生成的。

#### --outline-depth

`--outline-depth` 用来指定生成的大纲的深度。默认值为 4。你可以指定一个大一些的数字，以保证所有在HTML中指定的H标签都能在大纲中生成对应的项，方便阅读时快速跳转。

当指定了 `--no-outline` 参数时， 将不会输出大纲到PDF文档，所以再指定 `--outline-depth` 也就没有意义了。

### 页面对象参数

~~~ shell
    --allow <path>                指定加载HTML中相对路径文件的目录(可重复使用此参数指定多个
                                  目录)，这个参数会在后面进行更详细的讲解
    --background                  输出页面背景到PDF文档(这是默认设置)
    --no-background               不输出页面背景到PDF文档
    --cache-dir <path>            网页的缓存目录
    --checkbox-checked-svg <path> 使用指定的SVG文件渲染选中的复选框
    --checkbox-svg <path>         使用指定的SVG文件渲染未选中的筛选框
    --cookie <name> <value>       设置访问网页时的cookie,value 需要进行url编码
                                  (可重复使用此参数指定多个cookie)
    --custom-header <name> <value> 设置访问网页时的HTTP头(可重复使用此参数指定多个HTTP头)
    --custom-header-propagation   为每个要加载的资源添加由 --custom-header 指定的HTTP头
    --no-custom-header-propagation 不为每个要加载的资源添加由 --custom-header 指定的HTTP头
    --debug-javascript            显示javascript调试输出的信息
    --no-debug-javascript         不显示javascript调试输出的信息(这是默认设置)
    --default-header              添加一个默认的“头”，在页面的左头显示页面的名字，
                                  在页面的右头显示页码，这相对于进行了如下设置：
                                  --header-left='[webpage]'
                                  --header-right='[page]/[toPage]'
                                  --top 2cm
                                  --header-line
    --encoding <encoding>         为输入的文本设置默认的编码方式
    --disable-external-links      禁止页面中的外链生成超链接
    --enable-external-links       允许页面中的外链生成超链接(这是默认设置)
    --disable-forms               不转换HTML表单为PDF表单(这是默认设置)
    --enable-forms                转换HTML表单为PDF表单
    --images                      加载图片并输出到PDF文档(这是默认设置)
    --no-images                   在生成的PDF文档中过滤掉图片
    --disable-internal-links      禁止页面中的内链生成超链接
    --enable-internal-links       允许页面中的内链生成超连接(这是默认设置)
-n, --disable-javascript          禁止WEB页面执行 javascript
    --enable-javascript           允许WEB页面执行 javascript(这是默认设置)
    --javascript-delay <msec>     延迟一定的毫秒等待javascript 执行完成(默认值是200)
    --load-error-handling <handler> 指定当页面加载失败后的动作，可以指定为：abort(中止)、
                                    ignore(忽略)、skip(跳过)；(默认值是：abort)
    --load-media-error-handling <handler> 指定当媒体文件加载失败后的动作，可以指定为：
                                          abort(中止)、ignore(忽略)、skip(跳过)；
                                          (默认值是：ignore)
    --disable-local-file-access   不允许一个本地文件加载其他的本地文件，使用命令行参数
                                   `--allow` 指定的目录除外。
    --enable-local-file-access    允许本地文件加载其他的本地文件(这是默认设置)
    --minimum-font-size <int>     设置最小的字号，除非必要不推荐使用该参数
    --exclude-from-outline        拒绝加载当前页面到PDF文档的目录和大纲中
    --include-in-outline          加载当前页面到PDF文档的目录和大纲中(这是默认设置)
    --page-offset <offset>        设置页码的起始值(默认值为0)
    --password <password>         HTTP身份认证的密码
    --disable-plugins             禁止使用插件(这是默认设置)
    --enable-plugins              允许使用插件，但插件可能并不工作
    --post <name> <value>         添加一个POST字段，可以重复使用该参数添加多个POST字段。
    --post-file <name> <value>    添加一个POST文件，可以重复使用该参数添加多个文件。
    --print-media-type            用显示媒体类型代替屏幕
    --no-print-media-type         不用显示媒体类型代替屏幕
-p, --proxy <proxy>               使用代理
--radiobutton-checked-svg <path>  使用指定的SVG文件渲染选中的单选框
--radiobutton-svg <path>          使用指定的SVG文件渲染未选中的单选框
--run-sript <js>                  页面加载完成后执行一个附加的JS文件，可以重复使用此参数指定
                                  多个要在页面加载完成后要执行的JS文件。
--disable-smart-shrinking         不使用智能收缩策略
--enable-smart-shrinking          使用智能收缩策略(这是默认设置)
--stop-slow-scripts               停止运行缓慢的javascript代码(这是默认设置)
--no-stop-slow-scripts            不停止运行缓慢的javascript代码
--disable-toc-back-links          禁止从标题链接到目录(这是默认设置)
--enable-toc-back-links           允许从标题链接到目录
--user-style-sheet <url>          设置一个在每个页面都加载的用户自定义样式表
--username <username>             HTTP身谁的用户名
--viewport-size <>                设置窗口大小,需要你自定义滚动条或css属性来自适应窗口大小。
--window-status <windowStatus>    Wait until window.status is equal to
                                  this string before rendering page
--zoom <float>                    设置转换成PDF时页面的缩放比例(默认为1)

~~~

上面代码段中只是对所有 页面对象参数 做了个大概的说明，下面针对个别主要参数做更详细的讲解。

#### --allow

这个参数只在“页面对象”是一个文件时有效，在“页面对象”是一个url时此参数无效。

这个参数的作用是为HTML页面中使用相对路径引用的文件指定一个加载文件的基目录。也就是说HTML文件中所有以相对路径指定的文件都会从 `--allow` 参数指定的目录进行加载。其实在HTML中指定 `base` 标签可以达到同样的目的。如果两者(`--allow`参数和`base`标签)都没有指定，则使用当前处理的HTML文件所在的目录作为基目录加载当前处理的HTML中相对路径指定的文件。

#### --background AND --no-background

这两个参数是一对，用来指定是否在生成的PDF中应用网页的背景，默认 `--background`参数是开启的，也就是说默认生成的PDF文档中是带有HTML页面的背景图片或背景色的。如果开启 `--no-backgroupd` 参数，则生成的PDF文档中不会有HTML页面中的背景图片和背景色。

#### --debug-javascript ADN --no-debug-javascript

这两个参数用来指定是否在标准输出中输出javascript的调试信息，默认 `--no-debug-javasript` 参数是开启的，也就是说默认不会输出javascript的调试信息。下图是打开 `--debug-javascript` 参数的演示。

![](http://upload-images.jianshu.io/upload_images/3060014-c9a2fdee76719829.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

--debug-javascript

#### --disable-external-links AND --enable-external-links

这两个参数是用来设置在页面中的外链是否以超链接的形式出现在PDF文档中。关于“外链”的定义请移架 术语定义 。默认 `--enable-external-links` 参数被打开，所以默认情况是页面中的外链是以超链接的形式出现的PDF文档中的，点击可以打开指定的网页。

#### --exclude-from-outline AND --include-in-outline

这两个参数用来设置当前页面对象是否包含到目录和大纲中。 默认情况下 `--include-in-outline` 参数是打开的。也就是说默认情况下生成的PDF文档目录和大纲中是包含当前页面的，如果你不想让当前页面加到目录和大纲中可以打开 `--exclude-from-outline` 参数。

#### --post AND --post-file

当目标页面需要接受POST表单才能正确得到响应时，可以用这两个参数。这两个参数都是可以重复使用的。

还有一个应用场景是，用于自动化的WEB应用测试中。可以得到PDF文档作为测试报告。

`--post-file` 也可以用于自动批量上传文件的场景。

#### --run-sript

当需要对页面进行一定的预处理后再生成PDF文档的场景，使用该参数再合适不过了。这个参数可以重复使用指定多个需要在页面加载完成后执行的JS代码。你可以在这些JS中对页面的结构和内容进处理，JS执行完成后才会把对应的页面生成PDF文档。

#### --disable-internal-links AND --enable-internal-links

这两个参数是用来设置在页面中的内链是否以超链接的形式出现在PDF文档中。关于“内链”的定义请移架 术语定义 。默认 `--enable-internal-links` 参数被打开，所以默认情况是页面中的内链是以超链接的形式出现的PDF文档中的，点击在当前PDF中跳转到指定锚点。

#### --enable-toc-back-links AND --disable-toc-back-links

这组参数用来设置，是否在PDF内容中的H标签处生成超链接。生成的超链接点击后会跳转到目录和大纲中该H标签对应的锚点位置。默认情况下 `--disable-toc-back-links` 参数被打开，不会在PDF文档的H标签处生成超链接。

如果你需要在阅读PDF文档的内容时快速回到目录，你可以打开 `--enable-toc-back-links`参数。

#### --user-style-sheet

这个参数用来加载一个用户自定义的样式表，用来改变HTML页面原有的样式。需要高度自定义页面新式的同学可以尝试使用这个参数达到目的。

### 页眉和页脚参数选项

~~~ shell
    --footer-center <text>        在页脚的居中部分显示页脚文本 <text>
    --footer-font-name <name>     设置页脚的字体 (默认为 Arial)
    --footer-font-size <size>     设置页脚的字体大小 (默认为 12)
    --footer-html <url>           添加一个html作为页脚
    --footer-left <text>          在页脚的居左部分显示页脚文本 <text>
    --footer-line                 在页脚上方显示一条直线分隔正文
    --no-footer-line              不使用直线分隔页脚与正文(这是默认设置)
    --footer-right <text>         在页脚的居右部分显示页脚文本 <text>
    --footer-spacing <real>       页脚与正文之间的距离(默认为零)

    --header-center <text>        在页眉的居中部分显示页眉文本 <text>
    --header-font-name <name>     设置页眉的字体 (默认为 Arial)
    --header-font-size <size>     设置页眉的字体大小 (默认为 12)
    --header-html <url>           添加一个html作为页眉
    --header-left <text>          在页眉的居左部分显示页眉文本 <text>
    --header-line                 在页眉下方显示一条直线分隔正文
    --no-header-line              不使用直线分隔页眉与正文(这是默认设置)
    --header-right <text>         在页眉的居右部分显示页眉文本 <text>
    --header-spacing <real>       页眉与正文之间的距离(默认为零)
~~~

页眉页脚的设置比较简单，看上述代码段中的解释已经非常明了，所以不再赘述。后面还有针对页眉与页脚的其他相关介绍。

### 目录对象参数

~~~ shell
    --disable-dotted-lines        在目录中不使用虚线
    --toc-header-text <text>      设置目录的页眉文本
    --toc-level-indentation <width> 第级标题在目录中的缩进宽度(默认为1em)
    --disable-toc-links           在目录中不生成指向内容锚点的超链接
    --toc-text-size-shrink <real> 在目录中每级标题的缩放比例(默认为0.8)
    --xsl-style-sheet <file>      使用自定义的 XSL 样式表显示目录内容
~~~

“目录对象”我们一般用不到，上述代码段中的讲解也不难懂，所以不针对每一个具体参数再做详细的讲解。

## 关于页面尺寸说明

默认的页面尺寸是 A4，你可以使用 `--page-size` 参数指定你想要的页面尺寸，如：A3，Letter 和 Legal等。想要查看本程序支持的所有页面尺寸，请访问 [http://qt-project.org/doc/qt-4.8/qprinter.html#PaperSize-enum](http://qt-project.org/doc/qt-4.8/qprinter.html#PaperSize-enum)

你还可以使用 `--page-height` 和 `--page-width` 对页面尺寸进行更精细的控制。

## 从标准输入获取参数

如果你需要对许多页面进行批量的处理，并且感觉 wkhtmltopdf 开启比较慢，你可以尝试使用 `--read-args-from-stdin` 参数。

wkhtmltopdf 命令会为 `--read-args-from-stdin` 参数发送过来的每一行进行一次单独命令调用。也就是说此参数每读取一行都会执行一次 wkhtmltopdf 命令。而最终执行的命令中的参数是命令行中参数与此参数读取的标准输入流中参数的结合。

下面的代码段是一个例子:

~~~ shell
echo "http://qt-project.org/doc/qt-4.8/qapplication.html qapplication.pdf" >> cmds
echo "cover google.com http://en.wikipedia.org/wiki/Qt_(software) qt.pdf" >> cmds
wkhtmltopdf --read-args-from-stdin --book < cmds
~~~

## 指令一个代理

默认情况下代理信息将读取环境变量:proxy、all_proxy 和 http_proxy,代理选项还可以通过指定 `-p` 参数开启。

使用 BNF 对代理的定义如下：

~~~
<type> := "http://" | "socks5://"
<serif> := <username> (":" <password>)? "@"
<proxy> := "None" | <type>? <serif>? <host> (":" <port>)?
~~~

如果你不熟悉 BNF 的话，下面的代码段中是三个例子:

~~~
http://user:password@myproxyserver:8080
socks5://myproxyserver
None
~~~

## 页眉和页脚

页眉和页脚可以使用参数 `--header-*` 和 `--footer-*` 添加到文件中。有些参数(如 `--footer-left`)需要提供一个字符串`text`作为参数值。你可以在 `text`中插入下述变量，他们将会被替换成对应的值。

~~~ ini
[page]       当前正在被输出页面的页码
[frompage]   第一页在文档中的页码
[topage]     最后一面在文档中的页码
[webpage]    当前正在被输出页面的URL
[section]    当前正在被输出的章节的名字
[subsection] 当前正在被输出的小节的名字
[date]       本地系统格式的当前日期
[isodate]    ISO 8601 格式的当前日期
[time]       本地系统格式的当前时间
[title]      当前对象的标题
[doctitle]   输出文档的标题
[sitepage]   当前正在处理的对象中当前页面的页码
[sitepages]  当前正在处理的对象中的总页数

~~~

举一个例子来说明吧，`--header-right "Page [page] of [toPage]"`, 会在页面的右上角生成一个类似 `Page x of y` 的字符串，其中 `x` 是当前页面的页码， `y` 是当前文档最后一页的页码。

页眉和页脚也可以通过 HTML文档来提供。 同样举一个例子，使用命令行参数 `--header-html header.html` 来生成页眉，而 header.html 的内容如下:

~~~ html
<html><head><script>
function subst() {
  var vars={};
  var x=window.location.search.substring(1).split('&');
  for (var i in x) {var z=x[i].split('=',2);vars[z[0]] = unescape(z[1]);}
  var x=['frompage','topage','page','webpage','section','subsection','subsubsection'];
  for (var i in x) {
    var y = document.getElementsByClassName(x[i]);
    for (var j=0; j<y.length; ++j) y[j].textContent = vars[x[i]];
  }
}
</script></head><body style="border:0; margin: 0;" onload="subst()">
<table style="border-bottom: 1px solid black; width: 100%">
  <tr>
    <td class="section"></td>
    <td style="text-align:right">
      Page <span class="page"></span> of <span class="topage"></span>
    </td>
  </tr>
</table>
</body></html>
~~~

## 大纲(Outlines)

wkhtmltopdf 可以使用 `--outline` 命令行参数来指定在PDF就要中输出像书本中目录一样的“大纲”，“大纲”是基本HTML文档中H标签生成的，具体的大纲的层级和尝试请移步 目录

如果HTML文档中的H标签等级比较多，就可以生成深层级树形结构的“大纲”，而生成“大纲”的真实深度是通过 `--outline-depth` 参数来控制。

## 目录

通过在命令行中添加 TOC对象 可以把一个目录添加到生成的PDF文档中，例如下面的代码段：

~~~ shell
wkhtmltopdf toc http://qt-project.org/doc/qt-4.8/qstring.html qstring.pdf
~~~

生成的目录也是基于HTML文档的H标签。过程是首先生成一个XML文档,然后使用XSLT转换为HTML。 生成的 XML 文档可以通过 `--dump-outline` 参数查看。

~~~ shell
wkhtmltopdf --dump-outline toc.xml http://qt-project.org/doc/qt-4.8/qstring.html qstring.pdf
~~~

你如果想要使用自定义的XSLT文档可以通过 `--xsl-style-sheet` 参数指定

~~~ shell
wkhtmltopdf toc --xsl-style-sheet my.xsl http://qt-project.org/doc/qt-4.8/qstring.html qstring.pdf
~~~

你可以使用 `--dump-default-toc-xsl` 参数把默认的 XSLT 文档打印到标准输出，然后基于它创建你的自定义 XSLT 文档。

~~~ shell
wkhtmltopdf --dump-default-toc-xsl
~~~

## 总结

以上就是有关 wkhtmltopdf 工具的所有内容，这些内容中的大部分是通过阅读 wkhtmltopdf 的 `-H` 参数输出的英文文档获取的。水平有限，如有不足请指正。

## 相关文章

[HTML 转 PDF 之 wkhtmltopdf 工具简介]([http://www.jianshu.com/p/559c594678b6](http://www.jianshu.com/p/559c594678b6)

转自

~~~
http://www.jianshu.com/p/4d65857ffe5e