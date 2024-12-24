# 学习笔记

## Python代码注意点

* 格式化字符串不能使用`f"{}"`的形式，否则无法正常转换成JS语言，可以使用`.format`
* 时间可以使用`Game.time`获取

## 建筑

需要在游戏中手动放置`CONSTRUCTION SITE`，然后派遣builder去建造

## 待实现

* 守卫（游走状态，帮助清理room中的入侵者）
* 更好的矿工，根据情况选择合适的资源采集
* 考虑如何提升效率
* 代码架构的完善