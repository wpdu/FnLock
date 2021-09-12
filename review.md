# 复盘
> 程序主要有两部分，按键映射处理和UI控制，开发过程中均出现了比较多的波折，通过回溯开发过程，进行自我审查
-----
## 一、键盘映射逻辑
> 该模块主要使用keyboard库，简单思路：通过记录f1-f12按键触发的组合按键，如果匹配则抑制后触发自定义按键
### 思路线
1. 自己写了一套匹配组合键的mapper，并且可以正常工作，但是不知道如何抑制，然后发现原来库中已经提供了按键映射方法，本着不重复造轮子的理念，便使用`remap_key` `remap_hotkey`两个组合键映射方法，从功能上两者互补，前者覆盖单按键(f1-f6)，后者覆盖组合按键(f9-f12)(f8,f9未找到映射)
2. 使用库中的键映射可以正常触发和抑制，但同时抑制了其他组合键的使用（以`left window`为第一个触发的组合键和单独使用都受到影响）
3. 为了更大的自由度，重新使用自定义按键映射，并找到了抑制组合键方法`on_press(callback, suppress=True)`,在调试过程中发现，fn组合键是按下后触发，因此必须抑制最后一个按键，最后调试下来又在以`left windows`为首的组合键`f10(left windows + tab)`和`f12(left windows + f21)`出问题，因为抑制了最后一个按键后便只剩下单键`left windows`，会在出发目标按键时弹出window菜单
4. 接下来在抑制`left windows`的前提下尝试了很多办法，通过后期判断来填补的方法最终都不理想，都会影响别的组合键，思路陷入僵局，只好妥协用`f9` `printscreen` 来替代 `f10` `f12`这两个我经常用到的按键
5. 峰回路转，第二天意外尝试发现，用无效的windows组合键可以抑制已经触发的windows，这样在press阶段完全匹配后，手动出发一个ctrl，即可不再弹出windows菜单，再加上多媒体的自动触发要比手动快的多，来过滤掉手动出发时的场景，最后完美实现除f7，f8之外的所有多媒体按键

### 未完
1. f7，f8为何没有按键扫描，既然系统已经有反馈说明是有入口，可能是这个库无法识别？
    - 通过查看keyboard底层方法，是否确实有，只不过没有调用回调
    - 用别的库看看

## 二、PyQt5
> 托盘，快捷键，开关状态UI
> 刚开始考虑electron+vue，正好练练手，但是怕是浏览器集成，体积过大，并且UI也不多，于是放弃

### Icon制作
- 通过svg绘制，然后线上转换成png，再用pillow转成ico格式（多分辨率）

## 三、打包问题
1. 使用非虚拟环境打包但是会出现运行的各种错误，还是在虚拟环境打包比较稳妥，
2. 用 -i ipcon_path 的方式增加图标，发现程序窗口左上角并没有被替换，后来发现必须在程序中也添加icon设置
3. 打包后如果设置的icon不在相对目录下，会导致图标丢失，可能打包资源设置有问题还得完善

