# TG群聊土狗交易总结机器人

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

