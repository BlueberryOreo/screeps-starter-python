# 学习笔记

## 游戏注意点

* 当前tick给一个creep下达指令后，当前tick并不会立刻执行，而是会在当前tick结束后执行。因此在下达改变游戏状态的指令后（例如移动等），不能立即获取变化后的状态，需要等到下一个tick再获取状态查看是否有改变

## Python代码注意点

* 格式化字符串不能使用`f"{}"`的形式，否则无法正常转换成JS语言，可以使用`.format`
* 时间可以使用`Game.time`获取
* 更新字典需要使用`字典.key = value`的形式，否则无法正常转换成JS语言
* 不能直接使用`形参名=参数`的形式传参
* 一个__new__()出来的RoomPosition似乎无法直接使用RoomPosition.isEqualTo和一个creep.pos进行比较

## 建筑

需要在游戏中手动放置`CONSTRUCTION SITE`，然后派遣builder去建造

## 待实现

* 守卫（游走状态，帮助清理room中的入侵者）
* 更好的矿工，一个资源放一个矿工，周围放container，采集完立刻放入container，其他creep不采矿，仅通过container提取资源