![ilovebasketball](ilovebasketball.svg)

# ZHIN

:basketball: 一个基于 django5+vue3 的 AI 应用平台。

[TOC]

## :rocket: 写在前面

:airplane: 不断完善、不断更新、不断学习。

- 后端：python=3.12

  ```
  django=5.2.3
  django-ninja=1.4.3
  django-ninja-jwt=5.3.7
  ldap3=2.9.1
  ```

- 前端：在 [vue-vben-admin（v5.5.7）](www.vben.pro) 项目上进行的修改

## :open_book: 使用手册



---

:ocean: 下面是一些碎碎念，不看也罢~

## :calendar: 开发计划

:palm_tree: [项目面板](https://github.com/users/TinyHandsome/projects/2)

:deer: **设计思路**

- **请求统一返回逻辑设计**，设计 `response=OutCommonResponse`，返回的内容仅有三个字段，同时实际了正产返回和错误返回的模板。注意，返回的 `status_code `都是默认的 `200`，这代表无论成功还是失败，都在我们的控制范围内。

  - `status`：1/0，正常/异常
  - `msg`：返回的描述内容
  - `data`：返回的数据内容

- `utils` 和 `operations` **文件夹的区别**：前者可以独立运行，后者需要导入django的models相关类进行操作。原因：前者可以不起服务就测试，后者不行。

- **节流 throttling**

  从源码看，除开抽象类，一共有四个类可以用。我选用户id+匿名ip，比如login用 `AnonRateThrottle` 即可，其他的需要认证权限的可以考虑 `AuthRateThrottle`

  - `SimpleRateThrottle`：基于内存的实现，感觉意义不大。

    > A simple cache implementation, that only requires `.get_cache_key()` to be overridden.

  - `AnonRateThrottle`：针对匿名用户的限制，基于IP地址。仅限制未经身份验证的用户。

    > Limits the rate of API calls that may be made by a anonymous users.
    >
    > The IP address of the request will be used as the unique cache key.

  - `AuthRateThrottle`：用户+匿名都限制，匿名还是基于IP。基于 `django-ninja` 的身份验证来搞，选这个好。

    > Limits the rate of API calls that may be made by a given user.
    >
    > The string representation of `request.auth` object will be used as a unique cache key.
    > If you use custom auth objects make sure to implement __str__ method. For anonymous requests, the IP address of the request will be used.

  - `UserRateThrottle`：跟上面的区别，这里用户限制是根据用户的id来的，匿名还是基于IP。这里需要使用django内置用户身份验证，基本也没啥用。

    > Limits the rate of API calls that may be made by a given user.
    >
    > The `user id` will be used as a unique cache key if the user is
    > authenticated.  For anonymous requests, the IP address of the request will
    > be used.

  使用的范围也分 `global`、`router`、`operation`，节流对于恶意攻击也不太好使，毕竟IP可以欺骗，有就行了~ 暂定：

  - 全局：5/1m
  - 登录 `/usermanage/login`：3/1m
  - 获取用户信息 `/usermanage/info`：30/1m，老是刷新可以理解一下
  - 超过之后会触发 WARNING 警告，返回 `429`，报错信息：*Too many requests.*







## :taco: 一些经验

1. **关于SSE**

   之前做 sse 的时候用的 `django_eventstream`，感觉配置十分复杂，并且这个库用的人也不是很多。我的实际场景其实是希望 *大模型在流输出的时候，一方面可以流输出给前端，一方面能够在流输出结束后把大模型的总输出保存到数据库，并做一些其他的操作。* 所以不能直接用Django自带的 `StreamingHttpResponse` 直接包装生成器返回。并且，用前面这个库实现的时候，一个比较大的问题是有时候用户第一次发请求的时候，会阻塞/等待好久，后续再问就没有这个问题了，原因一直没找到，很烦~ :sweat:
   
2. **为什么要用 django-ninja**

   之前开发 django 都是用的原生，自己写了一套规范，其实返回的还是json，`drf` 用不习惯（好吧，还是我懒得学），`ninja` 的设计就很击中我的设计美学，跟 `fastapi` 很像，学吧，学一下试试看。
   
3. **关于python-ldap和ldap3**

   前者之前用过，需要系统安装一堆玩意儿，跑起来还挺麻烦的。这次想试试后者。（后者的 :star: 也多呀~）

4. **关于节流**

   之前用的 `django_ratelimit` 的库做节流，看到 [django-ninja](https://django-ninja.dev/guides/throttling/) 里面也有自带的节流，感觉可以直接用，并且封装的很好，没必要自己写，还是希望不要引入新的架构，能少一个是一个。