![ikun](ikun.svg)

# ZHIN

一个基于 django5+vue3 的 AI 应用平台。

[TOC]

## 写在前面

- 后端：python=3.12

  ```
  django=5.2.3
  django-ninja=1.4.3
  django-ninja-jwt=5.3.7
  ```

- 前端：在 [vue-vben-admin（v5.5.7）](www.vben.pro) 项目上进行的修改









## 一些经验

1. **关于SSE**

   之前做 sse 的时候用的 ==django_eventstream==，感觉配置十分复杂，并且这个库用的人也不是很多。我的实际场景其实是希望 *大模型在流输出的时候，一方面可以流输出给前端，一方面能够在流输出结束后把大模型的总输出保存到数据库，并做一些其他的操作。* 所以不能直接用Django自带的 **StreamingHttpResponse** 直接包装生成器返回。并且，用前面这个库实现的时候，一个比较大的问题是有时候用户第一次发请求的时候，会阻塞/等待好久，后续再问就没有这个问题了，原因一直没找到，很烦~ :sweat:
   
2. 