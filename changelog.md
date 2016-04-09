# 更新历史

## 实验阶段

### WIP

- [add] 增加了 `ZhihuClient.from_url` 方法，传入合法的知乎网址，就能生成对应的对象
- [add] 给 `BaseGenerator` 增加了 `add_params` 和 `set_params`  方法
- [fix] 修复了 `BaseGenerator` 在 Python 2 下有问题的情况。
- [fix] 修复了当用户的 `locations`，`educations`，`business`，`employments` 等属性值不存在强行获取会出错的 bug
- [add] 写完了文档
- [change] 改变了好多内部类名和变量名，不过对外部接口没有影响

### 0.0.2 - 2016.04.07

- [fix] 修复错误的 BASE_HTML_HEADER 值。原值会导致 html 文件在 Firefox 中打开时，由于没有编码信息显示而不正确的问题。
- [add] 完善文档，用户文档基本写完。

### 0.0.1 - 2016.04.07

首次发布，提供基础功能。
