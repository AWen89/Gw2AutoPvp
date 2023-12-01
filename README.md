# Gw2AutoPvp ~ Guild Wars 2 Automatic Pvp Bot
# 一款激战2自动竞技场机器人脚本bot
---
<p align="center">
  <img src="page.jpg" />
</p>

## 写在前面
- **`为什么会有此项目？`** 此项目**不是为了影响国服环境**。众所周知，由于国内某良心代理厂商不作为，导致pvp/wvw脚本泛滥、只封玩家不封工作室、以及取消网页签到活动等操作，严重影响普通玩家的权益。秉着**打不过就加入**的原则，希望能够为国服玩家解放双手，挂出属于自己的一套传奇护甲！*而不是去花费2100RMB当冤种*
- **`此项目会封号吗？`** **会！怕别用，用别怕**。新号尤其是没有购买dlc的账号，基本必封。但对于大号而言，封不封看良心厂商的心情，我两个号至今都没有被封。
- **`收益如何？`** 单账号每天挂14小时(约60~80场)含材料总收益约90金，升华碎片200至300个。
- **`有什么防封秘籍吗？`** 同一ip不要三开以上！尽量每个号放到虚拟机里运行。每天最多挂10个小时。**分段在900分及以下是最稳的，1000分以上会被玩家举报！**
- **`项目适用于美服/欧服吗？`** 不适用。逻辑上是互通的，但是你需要重新对图像识别进行截图，并且找到外服的基址。实际上你没必要这么做，外服多低的分段都没有挂机的，而且匹配时间很长，收益极低。

## 支持功能
- [x] 自动寻路占点
- [x] 自动释放技能
- [x] 支持多开(未测试,推荐在虚拟机多开)
- [x] 组排队长/队员模式(未测试)
- [x] 5V5模式
- [x] 排位模式(自动识别)
- [x] 匹配模式(自动识别)
- [x] 自定义房
- [x] 3V3/2V2模式(不寻路，直线向前走)
- [ ] 交互界面GUI
- [x] 永久免费
- [x] 自动检查更新 

## 视频演示
- [这里这里！](https://www.bilibili.com/video/BV1E8411k7R1/?spm_id_from=333.999.0.0&vd_source=0940bf29b38efba56ccfc6a3cef8182d)

## 如何使用
- 详情请见[使用教程](./%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B/%E6%95%99%E7%A8%8B%E6%95%99%E5%AD%A6.md)
### 1.下载
- 今后只在[这个地址更新-点我下载](https://gitee.com/javier_w/gw2-auto-pvp/releases)
- 或者：下载源代码

### 2.环境设置
- **必须**将目录下的`Driver`文件夹添加到系统环境变量！*此文件夹作用：调用dx11后台截图并进行图像检测。* 本项目使用的是[Aibot](http://www.aibote.net/)自动化框架。如果你对此框架不信任，推荐你自行修改源码，可替换为开源的[op](https://github.com/WallBreaker2/op)框架。
- **如何设置系统环境变量？** 自行百度
- 如果你下载的是源代码，则需要安装相关环境。需求列表懒得一一列出了。最重要的是安装`AiBot.py`。执行`pip install AiBot.py==1.2.5`即可。

### 3.游戏设置
- 系统设置中启用：`使用自由视角`
- 系统设置中**必须关闭**：`双击方向键闪避`
- 快捷键**必须设置**：`W前进`、`S后退`、`A左平移`、`D右平移`、`J左转`、`K右转`
- **强调**：`J左转`、`K右转`**必须设置**！否则寻路时不能自动转动视角

### 4.启动脚本
- 设置好环境后运行`Gw2AutoPvp.exe`
- 或者：安装相关环境后运行`Gw2AutoPvp.py`
- **注意**：必须进入pvp地图-迷雾之心后，开启本脚本

### 5.其他注意事项
- 强烈推荐使用死灵自杀流挂机！！！[bd配置点这里](https://www.bilibili.com/video/BV1JL4y1G78D/?spm_id_from=333.337.search-card.all.click&vd_source=0940bf29b38efba56ccfc6a3cef8182d)，如果不能自杀，可能会出现寻路失效！！！同时注意修改`suicide.txt`中的自动按键
- 右键系统桌面-显示设置，其中的`缩放`必须设置为100%！否则无法识别游戏图像
- 支持自动释放技能，需要更改`config`文件夹下的`suicide.txt`文件！
- **注意**：必须进入pvp地图-迷雾之心后，开启本脚本
- 游戏设置中的`界面大小`需要设置为`普通`，关闭DPI缩放，全屏伽马值为 1
- 如果你不够20级无法进行排位模式，那么使用脚本之前必须在pvp界面的`非排位偏好`里勾选`征服`模式。不能选择所有模式！否则会排到`末日英雄之战`这张图，效率极低，容易被举报

### 6.开发者-如何编译exe
- 强烈推荐使用`nuitka`来编译！
- 安装`nuitka`等编译环境。此处不详细列举，可自行去B站、知乎搜索相关教程！
- 进入项目根目录
- 执行`nuitka --mingw64 --standalone --show-progress --include-module=wmi --output-dir=out --windows-icon-from-ico=logo.png Gw2AutoPvp.py`
- 注意编译完成后，必须将原`config`、`src`文件夹复制到编译输出的文件夹中，否则会导致运行时无法找到相关文件！

### 7.开发者-如何寻找基址
- 所有的基址请修改`utils/Memory.py`文件，以下说明使用CE进行基址查找👇
- *地图相关的两个基址*：狮子拱门搜索4字节int型`50`，迷雾之心搜索4字节int型`350`
- *血量相关的两个基址*：脱换装备搜索单浮点。出来的结果中有一个访问该地址是`+B4`的偏移，继续向下搜索一次即可得出。
- *人物坐标基址*：推荐使用KX读取坐标后搜索。如果没有，可通过传送到以下狮子拱门传送点进行搜索(x,y,z)：`商人广场传送点 -66.32 432.74 25.82`、`避风港传送点 -336.38 69.7 12.75`、`星门广场传送点 117.84 198.9 35.72`
- *人物面向基址*：在上一步搜索的x坐标点，右键浏览相关内存区域，设置成按单浮点查看数据，进入游戏旋转人物视角，有两个连续的变化范围在-1~1之间的即为x、y轴方向的坐标。



## 最后
- 无任何QQ群、交流群。如需远程安装调试，需30RMB。联系QQ：467767967
- 如果问题可提Issues
- 欢迎二次开发
- 每次游戏版本更新后，都需要重新找基址，否则脚本会报错。我不保证对本项目会一直、及时的更新，如果有相关能力的朋友，可参考[使用教程](./%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B/%E6%95%99%E7%A8%8B%E6%95%99%E5%AD%A6.md)中的提示，进行基址更新
- 点个`Star`~
