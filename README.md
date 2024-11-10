# TG群聊土狗交易总结机器人

## 重要提示（对不起本项目失败了）

在 Telegram 中，一个 bot 默认是无法接收来自其他 bot 的消息的。Telegram 的 API 设计限制了 bot 与 bot 之间的直接交互，以防止滥用或恶意自动化。不过，你可以考虑以下几种方法来间接实现：

1. **用户转发**：可以让用户手动将其他 bot 的信息转发给你的 bot，你的 bot 就可以处理用户转发的消息。

2. **利用中间服务器**：如果你有控制某些群成员（非 bot）的权限，可以让这些成员（例如一个服务账号）监听群里的消息，将其他 bot 的消息转发或处理并发送给你的 bot。不过这需要用户配合并非完全自动化。

3. **Webhook / 轮询**：如果你可以在群聊的所有消息中筛选文本内容，可以通过 Webhook 或轮询方式实时获取信息并处理，尽管这是不完全获取其他 bot 信息的方式，但可用于简化信息的整合与分析。

如果 Telegram API 未来对 bot 与 bot 的交互有更新，这样的功能可能会直接实现。

> 所以我将下一步自己完整开发一个聪明钱监控+总结bot而不是开发一个bot来总结其他聪明钱监控bot的发言

## 功能

- 自动总结群消息
- 自动回复

## 具体要求

1. 总结tg群聊历史发送消息中同名代币累计买入的次数，最早买入价格，最迟买入价格
2. 检测到某代币第一次卖出发起提醒，卖出价格和总金额

## 技术栈

- 使用 `python` 和 `go` 开发
- 使用 `go-cqhttp` 开发 `go` 后端
- 使用 `python` 开发 `python` 后端
- 使用 `redis` 缓存数据

## 群内消息实例

```
交易买入通知
监控分组名：Sol小V
标签：宝灵灯
钱包地址：
查看solana钱包（GQva3..biRW9K） (https://solscan.io/address/GQva3CGJNAiBxzPYjNaamHeyQ2shnCmPpwp2bbiRW9K)
查看solana交易（4zmdk..fup8kq） (https://solscan.io/tx/4zmdkKFBNUtpc4L1z22hmmsxDq1DAtougGAoQ32UQUDzAhyyGELsrstauSdmZVBbevjLvxjVXet15xoi4rfup8kq)
时间：2024-11-09 20:38:26
钱包里交易买入:LILLIAN
合约：6y7rDiGywn3pxyZYD6LY17A5Fmi7CSzyTWVymScXpump
数量：41817509.04
单价：$0.00001433
总金额：$599.3095
查看行情 (https://pc.diting.ai/api/market/token?chain=solana&token=6y7rDiGywn3pxyZYD6LY17A5Fmi7CSzyTWVymScXpump)

Support by www.diting.ai (https://www.diting.ai/)

交易卖出通知
监控分组名：Sol小V
标签：宝灵灯
钱包地址：
查看solana钱包（GQva3..biRW9K） (https://solscan.io/address/GQva3CGJNAiBxzPYjNaamHeyQ2shnCmPpwp2bbiRW9K)
查看solana交易（39B5d..Mv8P4a） (https://solscan.io/tx/39B5d1dhzMMTmxTV7t3q5v5LgpwWL4wjxgMEpoyDVkWG5nUehkTc8ZUGrhmMr7GoprwgBJcvyXUr4awVDvMv8P4a)
时间：2024-11-09 20:38:11
钱包里交易卖出:LILLIAN
合约：6y7rDiGywn3pxyZYD6LY17A5Fmi7CSzyTWVymScXpump
数量：92033050.60
单价：$0.00001387
总金额：$1276.8054
查看行情 (https://pc.diting.ai/api/market/token?chain=solana&token=6y7rDiGywn3pxyZYD6LY17A5Fmi7CSzyTWVymScXpump)

Support by www.diting.ai (https://www.diting.ai/)
```

