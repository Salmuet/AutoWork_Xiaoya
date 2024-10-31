# 用不了了别看了【
新系统各种东西一直在调整，改起来还挺麻烦的

其实实现简单来说就是css匹配，但学校网页每次改版css定位信息也跟着变，还有各种大框套小框，子元素不给定位信息自适应啥的，号称几百万的管理系统，不知道谁写的前端，蛮难评的。

脚本思路是各种定位匹配，然后用`video.run_js(f'this.playbackRate = {RATE}')`调用json脚本来倍速播放视频，实现方法还是挺简单的。

## 其他办法
+ 可以直接F12，然后在Elements里面选中元素，右键复制css地址或者XPath地址，再去Console里面粘贴替换掉`this`: `this.playbackRate = RATE`。

+ 或者直接油猴下载网页倍速插件或许才是最优解【

+ 具体还有没有用，以及pdf任务那边判定有没有变就不知道了

用的包是DrissionPage不是Selenium是因为，Selenium需要用户下Chrome驱动内核，而DrissionPage可以直接调用Chrome，好用一点。
